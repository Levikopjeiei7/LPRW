"""
LPRW VLESS relay — high-performance WS gateway (v4).
Optimized buffers, early response, TCP tuning for lower latency.
"""
from __future__ import annotations

import asyncio
import logging
import socket
import time

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger("LPRW.vless")

RELAY_BUF = 2 * 1024 * 1024
SOCK_BUF = 8 * 1024 * 1024
WRITE_HIGH_WATER = 1024 * 1024

QUOTA_MIN_BATCH = 64 * 1024
QUOTA_MAX_BATCH = 4 * 1024 * 1024
QUOTA_START_BATCH = 256 * 1024
QUOTA_CHECK_INTERVAL = 0.2


def tune_socket(writer: asyncio.StreamWriter):
    try:
        sock = writer.transport.get_extra_info("socket")
        if not sock:
            return
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SOCK_BUF)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, SOCK_BUF)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if hasattr(socket, "TCP_QUICKACK"):
            try:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            except OSError:
                pass
        if hasattr(socket, "TCP_KEEPIDLE"):
            try:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
            except OSError:
                pass
    except OSError:
        pass


class QuotaGate:
    __slots__ = ("uuid", "pending", "last_check", "ok", "batch_bytes", "rate_ewma", "on_usage")

    def __init__(self, uuid: str, on_usage):
        self.uuid = uuid
        self.on_usage = on_usage
        self.pending = 0
        self.last_check = time.monotonic()
        self.ok = True
        self.batch_bytes = QUOTA_START_BATCH
        self.rate_ewma = 0.0

    def _call(self, n: int) -> bool:
        return bool(self.on_usage(self.uuid, n))

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
                self.rate_ewma = inst if not self.rate_ewma else (0.75 * self.rate_ewma + 0.25 * inst)
                target = int(self.rate_ewma * QUOTA_CHECK_INTERVAL)
                self.batch_bytes = max(QUOTA_MIN_BATCH, min(QUOTA_MAX_BATCH, target or QUOTA_MIN_BATCH))
            self.last_check = now
            try:
                self.ok = self._call(flush)
            except Exception:
                self.ok = False
            return self.ok
        return True

    async def flush(self) -> bool:
        if self.pending:
            flush, self.pending = self.pending, 0
            try:
                self.ok = self.ok and self._call(flush)
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
    port = int.from_bytes(chunk[pos:pos + 2], "big")
    pos += 2
    addr_type = chunk[pos]
    pos += 1
    if addr_type == 1:
        address = ".".join(str(b) for b in chunk[pos:pos + 4])
        pos += 4
    elif addr_type == 2:
        dlen = chunk[pos]
        pos += 1
        address = chunk[pos:pos + dlen].decode("utf-8", errors="ignore")
        pos += dlen
    elif addr_type == 3:
        ab = chunk[pos:pos + 16]
        pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr type: {addr_type}")
    return command, address, port, chunk[pos:]


async def open_tcp(address: str, port: int, timeout: float = 8.0):
    loop = asyncio.get_running_loop()
    try:
        infos = await loop.getaddrinfo(
            address, port, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )
    except Exception as e:
        raise OSError(f"dns failed {address}: {e}") from e

    infos = sorted(infos, key=lambda x: 0 if x[0] == socket.AF_INET else 1)
    for family, type_, proto, _, sockaddr in infos:
        sock = None
        try:
            sock = socket.socket(family, type_, proto)
            sock.setblocking(False)
            await asyncio.wait_for(loop.sock_connect(sock, sockaddr), timeout=timeout)
            reader, writer = await asyncio.open_connection(sock=sock)
            return reader, writer
        except Exception:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
    return await asyncio.wait_for(asyncio.open_connection(address, port), timeout=timeout)


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
                    await ws.close(code=1008)
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


async def relay_tcp_to_ws(ws: WebSocket, reader: asyncio.StreamReader, gate: QuotaGate, vless_prefix: bool = True):
    first = True
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await gate.add(len(data)):
                try:
                    await ws.close(code=1008)
                except Exception:
                    pass
                break
            if vless_prefix and first:
                await ws.send_bytes(b"\x00\x00" + data)
                first = False
            else:
                await ws.send_bytes(data)
    except Exception:
        pass
    finally:
        await gate.flush()


async def handle_vless_ws(ws, uuid, is_allowed, on_usage, register_conn, unregister_conn):
    await ws.accept()
    link = is_allowed(uuid)
    if not link:
        await ws.close(code=1008, reason="not authorized")
        return

    conn_id = register_conn(uuid)
    writer = None
    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=12.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        command, address, port, payload = parse_vless_header(first_chunk)

        gate = QuotaGate(uuid, on_usage)
        if not await gate.add(len(first_chunk)):
            await ws.close(code=1008, reason="quota")
            return

        if command != 0x01:
            await ws.close(code=1008, reason="udp not supported")
            return

        reader, writer = await open_tcp(address, port, timeout=8.0)
        tune_socket(writer)

        await ws.send_bytes(b"\x00\x00")

        if payload:
            writer.write(payload)
            await writer.drain()
            await gate.add(len(payload))

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, gate)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, gate, vless_prefix=False)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass
    except (WebSocketDisconnect, asyncio.TimeoutError):
        pass
    except Exception as e:
        logger.debug("vless error: %s", e)
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        unregister_conn(conn_id)
