"""Trojan over WebSocket — auth + SOCKS-like request + TCP relay."""
from __future__ import annotations

import asyncio
import logging
import socket
import struct
import uuid
from typing import Awaitable, Callable, Optional

logger = logging.getLogger("LPRW.trojan")


def parse_header(data: bytes) -> Optional[dict]:
    """password\\r\\n + CMD ATYP ADDR PORT + payload"""
    try:
        if b"\r\n" not in data:
            return None
        pw_b, rest = data.split(b"\r\n", 1)
        password = pw_b.decode("utf-8", "ignore").strip()
        if rest.startswith(b"\r\n"):
            rest = rest[2:]
        if len(rest) < 7:
            return None
        cmd = rest[0]
        atyp = rest[1]
        pos = 2
        if atyp == 0x01:
            addr = socket.inet_ntop(socket.AF_INET, rest[pos : pos + 4])
            pos += 4
        elif atyp == 0x03:
            n = rest[pos]
            pos += 1
            addr = rest[pos : pos + n].decode("utf-8", "ignore")
            pos += n
        elif atyp == 0x04:
            addr = socket.inet_ntop(socket.AF_INET6, rest[pos : pos + 16])
            pos += 16
        else:
            return None
        port = struct.unpack("!H", rest[pos : pos + 2])[0]
        pos += 2
        return {
            "password": password,
            "cmd": cmd,
            "port": port,
            "addr": addr,
            "payload": rest[pos:],
        }
    except Exception as e:
        logger.debug("trojan parse: %s", e)
        return None


async def _open(addr: str, port: int, timeout: float = 12.0):
    try:
        return await asyncio.wait_for(asyncio.open_connection(addr, port), timeout=timeout)
    except Exception as e:
        logger.debug("connect %s:%s %s", addr, port, e)
        return None, None


async def handle_trojan_ws(
    websocket,
    find_link: Callable[[str], Optional[dict]],
    on_usage: Callable[[str, int], Awaitable[None]],
    register_online: Callable[[str, str], None],
    unregister_online: Callable[[str, str], None],
):
    conn_id = uuid.uuid4().hex[:12]
    link_id = None
    try:
        first = await asyncio.wait_for(websocket.receive_bytes(), timeout=20)
        hdr = parse_header(first)
        if not hdr:
            await websocket.close(code=1008)
            return
        link = find_link(hdr["password"])
        if not link:
            await websocket.close(code=1008)
            return
        link_id = link["id"]
        register_online(link_id, conn_id)
        if hdr["cmd"] != 0x01:
            return
        reader, writer = await _open(hdr["addr"], hdr["port"])
        if reader is None:
            return

        async def pump_tcp_to_ws():
            try:
                payload = hdr.get("payload") or b""
                if payload:
                    await websocket.send_bytes(payload)
                    await on_usage(link_id, len(payload))
                while True:
                    chunk = await reader.read(32 * 1024)
                    if not chunk:
                        break
                    await websocket.send_bytes(chunk)
                    await on_usage(link_id, len(chunk))
            except Exception:
                pass
            finally:
                try:
                    writer.close()
                    await writer.wait_closed()
                except Exception:
                    pass

        async def pump_ws_to_tcp():
            try:
                while True:
                    chunk = await websocket.receive_bytes()
                    writer.write(chunk)
                    await writer.drain()
                    await on_usage(link_id, len(chunk))
            except Exception:
                pass
            finally:
                try:
                    writer.close()
                except Exception:
                    pass

        await asyncio.gather(pump_tcp_to_ws(), pump_ws_to_tcp())
    except Exception as e:
        logger.debug("trojan handler: %s", e)
    finally:
        if link_id:
            unregister_online(link_id, conn_id)
