"""
LPRW VLESS core — original implementation.
Path-based auth: /ws/{uuid}
"""
from __future__ import annotations

import asyncio
import logging
import socket
import time
from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger("LPRW.vless")

RELAY_BUF = 1024 * 1024
SOCK_BUF = 4 * 1024 * 1024
WRITE_HIGH_WATER = 512 * 1024


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
    except Exception as e:
        logger.debug("tune_socket: %s", e)


def parse_vless_header(chunk: bytes):
    """Parse VLESS request. Returns (command, address, port, payload)."""
    if len(chunk) < 24:
        raise ValueError("chunk too small")
    pos = 1  # skip version
    pos += 16  # skip UUID (auth via URL path)
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
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr type: {addr_type}")
    return command, address, port, chunk[pos:]


async def relay_ws_to_tcp(
    ws: WebSocket,
    writer: asyncio.StreamWriter,
    on_bytes,
):
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            if on_bytes:
                await on_bytes(len(data))
            writer.write(data)
            if writer.transport.get_write_buffer_size() > WRITE_HIGH_WATER:
                await writer.drain()
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass


async def relay_tcp_to_ws(
    ws: WebSocket,
    reader: asyncio.StreamReader,
    on_bytes,
    vless_prefix: bool = True,
):
    first = True
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if on_bytes:
                await on_bytes(len(data))
            if vless_prefix and first:
                payload = b"\x00\x00" + data
                first = False
            else:
                payload = data
            await ws.send_bytes(payload)
    except Exception:
        pass


async def handle_vless_ws(
    ws: WebSocket,
    uuid: str,
    is_allowed,
    on_usage,
    register_conn,
    unregister_conn,
):
    """
    is_allowed(uuid) -> link dict or None
    on_usage(uuid, nbytes) -> awaitable
    """
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
        await on_usage(uuid, len(first_chunk))

        if command != 0x01:  # TCP only
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
            await on_usage(uuid, len(payload))

        async def _usage(n: int):
            await on_usage(uuid, n)

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, _usage)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, _usage, True)),
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
        logger.debug("vless timeout uuid=%s", uuid[:8])
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
