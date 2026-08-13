"""
LPRW VLESS — high-throughput relay (batched quota, large buffers).
Path auth: /ws/{uuid}
"""
from __future__ import annotations

import asyncio
import logging
import socket
import time

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger("LPRW.vless")

# Match production gateway tuning
RELAY_BUF = 1024 * 1024          # 1 MB read chunks
SOCK_BUF = 4 * 1024 * 1024       # 4 MB OS socket buffers
WRITE_HIGH_WATER = 512 * 1024    # drain only when > 512 KB pending

QUOTA_MIN_BATCH = 32 * 1024
QUOTA_MAX_BATCH = 2 * 1024 * 1024
QUOTA_START_BATCH = 128 * 1024
QUOTA_CHECK_INTERVAL = 0.25


def tune_socket(writer: asyncio.StreamWriter):
    try:
        sock = writer.transport.get_extra_info("socket")
        if sock is None:
            return
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SOCK_BUF)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, SOCK_BUF)
        if hasattr(socket, "TCP_QUICKACK"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
    except Exception:
        pass


class QuotaGate:
    """
    Batch usage accounting so we don't take a global lock on every WS frame.
    Flushes every ~128KB–2MB or every 0.25s (adaptive).
    """
    __slots__ = ("uuid", "pending", "last_check", "ok", "batch_bytes", "rate_ewma", "on_usage")

    def __init__(self, uuid: str, on_usage):
        self.uuid = uuid
        self.on_usage = on_usage
        self.pending = 0
        self.last_check = time.monotonic()
        self.ok = True
        self.batch_bytes = QUOTA_START_BATCH
        self.rate_ewma = 0.0

    async def add(self, nbytes: int) -> bool:
        if not self.ok:
            return False
        self.pending += nbytes
        now = time.monotonic()
        elapsed = now - self.last_check
        if self.pending >= self.batch_bytes or elapsed >= QUOTA_CHECK_INTERVAL:
            flush, self.pending = self.pending, 0
            if elapsed > 0:
                inst = flush / elapsed
                self.rate_ewma = inst if self.rate_ewma == 0 else (0.7 * self.rate_ewma + 0.3 * inst)
                target = int(self.rate_ewma * QUOTA_CHECK_INTERVAL)
                self.batch_bytes = max(QUOTA_MIN_BATCH, min(QUOTA_MAX_BATCH, target or QUOTA_MIN_BATCH))
            self.last_check = now
            try:
                self.ok = await self.on_usage(self.uuid, flush)
            except Exception:
                self.ok = False
            return self.ok
        return True

    async def flush(self) -> bool:
        if self.pending:
            flush, self.pending = self.pending, 0
            try:
                self.ok = self.ok and await self.on_usage(self.uuid, flush)
            except Exception:
                self.ok = False
        return self.ok


def parse_vless_header(chunk: bytes):
    if len(chunk) < 24:
        raise ValueError("chunk too small")
    pos = 1
    pos += 16
    addon_len = chunk[pos]
    pos += 1 + addon_len
    command = chunk[pos]
    pos += 1
    port = int.from_bytes(chunk[pos : pos + 2], "big")
    pos += 2
    addr_type = chunk[pos]
    pos += 1
    if addr_type == 1:
        address = ".".join(str(b) for b in chunk[pos : pos + 4])
        pos += 4
    elif addr_type == 2:
        dlen = chunk[pos]
        pos += 1
        address = chunk[pos : pos + dlen].decode("utf-8", errors="ignore")
        pos += dlen
    elif addr_type == 3:
        ab = chunk[pos : pos + 16]
        pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i + 1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr type: {addr_type}")
    return command, address, port, chunk[pos:]


async def relay_ws_to_tcp(ws: WebSocket, writer: asyncio.StreamWriter, gate: QuotaGate):
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            if not await gate.add(len(data)):
                try:
                    await ws.close(code=1008, reason="quota")
                except Exception:
                    pass
                break
            writer.write(data)
            if writer.transport.get_write_buffer_size() > WRITE_HIGH_WATER:
                await writer.drain()
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        await gate.flush()
        try:
            writer.write_eof()
        except Exception:
            pass


async def relay_tcp_to_ws(
    ws: WebSocket,
    reader: asyncio.StreamReader,
    gate: QuotaGate,
    vless_prefix: bool = True,
):
    first = True
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await gate.add(len(data)):
                try:
                    await ws.close(code=1008, reason="quota")
                except Exception:
                    pass
                break
            if vless_prefix and first:
                payload = b"\x00\x00" + data
                first = False
            else:
                payload = data
            await ws.send_bytes(payload)
    except Exception:
        pass
    finally:
        await gate.flush()


async def handle_vless_ws(
    ws: WebSocket,
    uuid: str,
    is_allowed,
    on_usage,
    register_conn,
    unregister_conn,
):
    await ws.accept()
    link = is_allowed(uuid)
    if not link:
        await ws.close(code=1008, reason="not authorized")
        return

    conn_id = register_conn(uuid)
    writer = None
    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        command, address, port, payload = parse_vless_header(first_chunk)

        async def _account(uid: str, n: int) -> bool:
            return await on_usage(uid, n)

        gate = QuotaGate(uuid, _account)
        await gate.add(len(first_chunk))

        if command != 0x01:
            await ws.close(code=1008, reason="udp not supported")
            return

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port),
            timeout=12.0,
        )
        tune_socket(writer)

        if payload:
            writer.write(payload)
            await writer.drain()
            await gate.add(len(payload))

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, gate)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, gate, True)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass
    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        pass
    except Exception as e:
        logger.debug("vless: %s", e)
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        unregister_conn(conn_id)
