"""
LPRW Trojan core — original implementation.
Path-based auth: /trojan-ws/{password}
"""
from __future__ import annotations

import asyncio
import logging
import socket
from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect

from protocol.vless import RELAY_BUF, WRITE_HIGH_WATER, tune_socket

logger = logging.getLogger("LPRW.trojan")


def parse_trojan_header(data: bytes):
    """password\\r\\n + CMD ATYP ADDR PORT + payload"""
    if b"\r\n" not in data:
        raise ValueError("no crlf")
    pw_b, rest = data.split(b"\r\n", 1)
    password = pw_b.decode("utf-8", "ignore").strip()
    if rest.startswith(b"\r\n"):
        rest = rest[2:]
    if len(rest) < 7:
        raise ValueError("short request")
    cmd = rest[0]
    atyp = rest[1]
    pos = 2
    if atyp == 0x01:
        address = socket.inet_ntop(socket.AF_INET, rest[pos : pos + 4])
        pos += 4
    elif atyp == 0x03:
        n = rest[pos]
        pos += 1
        address = rest[pos : pos + n].decode("utf-8", "ignore")
        pos += n
    elif atyp == 0x04:
        address = socket.inet_ntop(socket.AF_INET6, rest[pos : pos + 16])
        pos += 16
    else:
        raise ValueError(f"bad atyp {atyp}")
    port = int.from_bytes(rest[pos : pos + 2], "big")
    pos += 2
    return password, cmd, address, port, rest[pos:]


async def relay_ws_to_tcp(ws: WebSocket, writer: asyncio.StreamWriter, on_bytes):
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


async def relay_tcp_to_ws(ws: WebSocket, reader: asyncio.StreamReader, on_bytes):
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if on_bytes:
                await on_bytes(len(data))
            await ws.send_bytes(data)
    except Exception:
        pass


async def handle_trojan_ws(
    ws: WebSocket,
    password: str,
    is_allowed,
    on_usage,
    register_conn,
    unregister_conn,
):
    await ws.accept()
    link = is_allowed(password)
    if not link:
        await ws.close(code=1008, reason="not authorized")
        return

    conn_id = register_conn(password)
    writer = None
    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        # password may also be in header; path is authoritative
        _, cmd, address, port, payload = parse_trojan_header(first_chunk)
        await on_usage(password, len(first_chunk))

        if cmd != 0x01:
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
            await on_usage(password, len(payload))

        async def _usage(n: int):
            await on_usage(password, n)

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, _usage)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, _usage)),
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
    except Exception as e:
        logger.debug("trojan error: %s", e)
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        unregister_conn(conn_id)
