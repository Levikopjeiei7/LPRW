"""
Real XHTTP for LPRW — Xray client path rules:
  config path:  /xhttp/stream-up/{uuid}/
  client hits:  /xhttp/stream-up/{uuid}/{sessionId}
            or: /xhttp/stream-up/{uuid}/{sessionId}/{seq}
"""
from __future__ import annotations

import asyncio
import logging
import re
import time
from typing import Callable, Optional

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import StreamingResponse

from protocol.common import RELAY_BUF, open_tcp, tune_socket
from protocol.trojan import parse_trojan_header
from protocol.vless import parse_vless_header

logger = logging.getLogger("LPRW.xhttp")
router = APIRouter()

SESSIONS: dict = {}
SLOCK = asyncio.Lock()
_reaper_on = False
IDLE = 120.0
RESP_H = {
    "content-type": "application/grpc",
    "cache-control": "no-cache, no-store",
    "x-accel-buffering": "no",
}


async def _reaper():
    while True:
        await asyncio.sleep(20)
        now = time.time()
        async with SLOCK:
            dead = [k for k, s in SESSIONS.items() if now - s["last"] > IDLE]
        for k in dead:
            await close_session(k, "idle")


def ensure_reaper():
    global _reaper_on
    if not _reaper_on:
        _reaper_on = True
        asyncio.create_task(_reaper())


async def close_session(sid: str, reason: str = ""):
    async with SLOCK:
        sess = SESSIONS.pop(sid, None)
    if not sess:
        return
    sess["closed"] = True
    t = sess.get("down_task")
    if t:
        t.cancel()
        try:
            await t
        except Exception:
            pass
    w = sess.get("writer")
    if w:
        try:
            w.close()
            await w.wait_closed()
        except Exception:
            pass
    q = sess.get("q")
    if q:
        try:
            q.put_nowait(None)
        except Exception:
            pass
    if sess.get("unreg") and sess.get("cid"):
        try:
            sess["unreg"](sess["cid"])
        except Exception:
            pass
    logger.info("xhttp close %s %s", sid[:12], reason)


async def get_sess(key, uuid, mode, is_allowed, reg, unreg) -> dict:
    async with SLOCK:
        s = SESSIONS.get(key)
        if s:
            s["last"] = time.time()
            return s
        link = is_allowed(uuid)
        if not link:
            raise HTTPException(403, "forbidden")
        cid = reg(uuid)
        s = {
            "uuid": uuid,
            "mode": mode,
            "writer": None,
            "q": asyncio.Queue(maxsize=512),
            "last": time.time(),
            "cid": cid,
            "unreg": unreg,
            "closed": False,
            "vless": True,
        }
        SESSIONS[key] = s
        return s


async def _pump(reader, sess, on_usage, uuid, key):
    first = True
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            sess["last"] = time.time()
            if on_usage and not on_usage(uuid, len(data)):
                break
            if sess.get("vless") and first:
                await sess["q"].put(b"\x00\x00" + data)
                first = False
            else:
                await sess["q"].put(data)
    except Exception:
        pass
    finally:
        try:
            await sess["q"].put(None)
        except Exception:
            pass
        await close_session(key, "tcp_done")


async def _open_remote(sess, first, proto, on_usage, key):
    if proto == "trojan":
        _, cmd, address, port, payload = parse_trojan_header(first)
        if cmd != 0x01:
            raise ValueError("udp")
        sess["vless"] = False
    else:
        cmd, address, port, payload = parse_vless_header(first)
        if cmd != 0x01:
            raise ValueError("udp")
        sess["vless"] = True
    reader, writer = await open_tcp(address, port, timeout=10.0)
    tune_socket(writer)
    if payload:
        writer.write(payload)
        await writer.drain()
    sess["writer"] = writer
    if sess["vless"]:
        try:
            sess["q"].put_nowait(b"\x00\x00")
        except Exception:
            pass
    sess["down_task"] = asyncio.create_task(_pump(reader, sess, on_usage, sess["uuid"], key))
    logger.info("xhttp tcp %s:%s", address, port)


def _parse_xhttp_path(path: str):
    path = path.split("?")[0]
    m = re.match(
        r"^/(?:xhttp|xhttp-siz10)/(stream-up|stream-one|packet-up|auto)/"
        r"([^/]+)/([^/]+)(?:/(\d+))?/?$",
        path,
    )
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3), m.group(4)


def bind_handlers(is_allowed, on_usage, register_conn, unregister_conn, get_proto: Callable):
    @router.api_route("/xhttp/{path:path}", methods=["GET", "POST", "PUT", "HEAD", "OPTIONS"])
    @router.api_route("/xhttp-siz10/{path:path}", methods=["GET", "POST", "PUT", "HEAD", "OPTIONS"])
    async def xhttp_any(path: str, request: Request):
        ensure_reaper()
        if request.method == "OPTIONS":
            return Response(status_code=204, headers=RESP_H)

        full = request.url.path
        parsed = _parse_xhttp_path(full)
        if not parsed:
            raise HTTPException(404, "bad xhttp path")

        mode, uuid, session, seq = parsed
        key = f"{uuid}:{session}"
        proto = get_proto(uuid)

        if request.method in ("GET", "HEAD"):
            sess = await get_sess(key, uuid, mode, is_allowed, register_conn, unregister_conn)

            async def gen():
                try:
                    while True:
                        chunk = await sess["q"].get()
                        if chunk is None:
                            break
                        sess["last"] = time.time()
                        yield chunk
                except asyncio.CancelledError:
                    pass

            return StreamingResponse(
                gen(),
                media_type="application/grpc",
                headers={k: v for k, v in RESP_H.items() if k != "content-type"},
            )

        sess = await get_sess(key, uuid, mode, is_allowed, register_conn, unregister_conn)
        writer = sess.get("writer")
        try:
            async for chunk in request.stream():
                if not chunk:
                    continue
                sess["last"] = time.time()
                if on_usage and not on_usage(uuid, len(chunk)):
                    raise HTTPException(403, "quota")
                if writer is None:
                    await _open_remote(sess, chunk, proto, on_usage, key)
                    writer = sess["writer"]
                    continue
                if writer.is_closing():
                    break
                writer.write(chunk)
                if writer.transport.get_write_buffer_size() > 256 * 1024:
                    await writer.drain()
        except HTTPException:
            raise
        except Exception as e:
            logger.warning("xhttp uplink %s", e)
            await close_session(key, str(e))
            return Response(status_code=502)
        return Response(status_code=200, headers=RESP_H)

    return router
