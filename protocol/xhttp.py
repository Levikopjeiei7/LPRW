"""
Real XHTTP transport for LPRW (HTTP uplink + HTTP downlink sessions).
Compatible with Xray/v2rayNG type=xhttp modes: stream-up, packet-up, stream-one.
Independent implementation — not a copy of any third-party panel.
"""
from __future__ import annotations

import asyncio
import logging
import secrets
import socket
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response, StreamingResponse

from protocol.vless import parse_vless_header
from protocol.trojan import parse_trojan_header
from protocol.common import open_tcp, tune_socket, RELAY_BUF

logger = logging.getLogger("LPRW.xhttp")

router = APIRouter()

SESSIONS: dict = {}
SLOCK = asyncio.Lock()
REAPER_STARTED = False

DOWN_Q_MAX = 256
IDLE_SEC = 90
CONNECT_TIMEOUT = 10.0

RESP_HDR = {
    "content-type": "application/grpc",
    "cache-control": "no-cache, no-store",
    "x-accel-buffering": "no",
}


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "?"


async def _ensure_reaper():
    global REAPER_STARTED
    if REAPER_STARTED:
        return
    REAPER_STARTED = True

    async def reaper():
        while True:
            await asyncio.sleep(15)
            now = time.time()
            async with SLOCK:
                dead = [sid for sid, s in SESSIONS.items() if now - s.get("last", 0) > IDLE_SEC]
            for sid in dead:
                await teardown(sid, "idle")

    asyncio.create_task(reaper())


async def teardown(session_id: str, reason: str = ""):
    async with SLOCK:
        sess = SESSIONS.pop(session_id, None)
    if not sess:
        return
    sess["closed"] = True
    for key in ("up_task", "down_task"):
        t = sess.get(key)
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
    q = sess.get("down_q")
    if q:
        try:
            q.put_nowait(None)
        except Exception:
            pass
    unreg = sess.get("unreg")
    if unreg and sess.get("conn_id"):
        try:
            unreg(sess["conn_id"])
        except Exception:
            pass
    logger.debug("xhttp session closed %s %s", session_id[:8], reason)


async def get_session(
    uuid: str,
    mode: str,
    session_id: str,
    ip: str,
    is_allowed,
    register_conn,
    unregister_conn,
) -> dict:
    async with SLOCK:
        sess = SESSIONS.get(session_id)
        if sess is not None:
            sess["last"] = time.time()
            return sess
        link = is_allowed(uuid)
        if not link:
            raise HTTPException(403, "not authorized")
        conn_id = register_conn(uuid)
        sess = {
            "uuid": uuid,
            "mode": mode,
            "writer": None,
            "reader": None,
            "down_q": asyncio.Queue(maxsize=DOWN_Q_MAX),
            "last": time.time(),
            "conn_id": conn_id,
            "tcp_open": False,
            "closed": False,
            "unreg": unregister_conn,
            "link": link,
            "seq_buf": {},
            "next_seq": 0,
        }
        SESSIONS[session_id] = sess
        logger.info("xhttp[%s] new session %s uuid=%s", mode, session_id[:8], uuid[:8])
        return sess


async def open_tcp_from_chunk(first: bytes, proto: str):
    if proto == "trojan":
        _, cmd, address, port, payload = parse_trojan_header(first)
        if cmd != 0x01:
            raise ValueError("udp not supported")
    else:
        command, address, port, payload = parse_vless_header(first)
        if command != 0x01:
            raise ValueError("udp not supported")
    reader, writer = await open_tcp(address, port, timeout=CONNECT_TIMEOUT)
    tune_socket(writer)
    if payload:
        writer.write(payload)
        await writer.drain()
    return reader, writer, address, port


async def pump_tcp_to_q(sess: dict, reader: asyncio.StreamReader, on_usage, vless_ack: bool):
    first = True
    uid = sess["uuid"]
    q = sess["down_q"]
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            sess["last"] = time.time()
            if on_usage and not on_usage(uid, len(data)):
                break
            if vless_ack and first:
                await q.put(b"\x00\x00" + data)
                first = False
            else:
                await q.put(data)
    except Exception:
        pass
    finally:
        try:
            await q.put(None)
        except Exception:
            pass
        await teardown(sess.get("sid") or "", "tcp_eof")


async def open_tcp_session(sess: dict, first_chunk: bytes, proto: str, on_usage):
    reader, writer, addr, port = await open_tcp_from_chunk(first_chunk, proto)
    sess["writer"] = writer
    sess["reader"] = reader
    sess["tcp_open"] = True
    logger.info("xhttp tcp -> %s:%s", addr, port)
    # immediate vless ack into queue
    if proto != "trojan":
        try:
            sess["down_q"].put_nowait(b"\x00\x00")
        except Exception:
            pass
    sess["down_task"] = asyncio.create_task(
        pump_tcp_to_q(sess, reader, on_usage, vless_ack=False)
    )


def bind_handlers(is_allowed, on_usage, register_conn, unregister_conn, get_proto):
    """Attach route handlers closed over panel callbacks."""

    @router.api_route(
        "/xhttp/{mode}/{uuid}/{session_id}",
        methods=["GET", "POST", "PUT", "HEAD", "OPTIONS"],
    )
    @router.api_route(
        "/xhttp-siz10/{mode}/{uuid}/{session_id}",
        methods=["GET", "POST", "PUT", "HEAD", "OPTIONS"],
    )
    async def xhttp_session(mode: str, uuid: str, session_id: str, request: Request):
        await _ensure_reaper()
        mode = (mode or "stream-up").lower()
        if mode not in ("stream-up", "packet-up", "stream-one", "auto"):
            mode = "stream-up"

        if request.method == "OPTIONS":
            return Response(status_code=204, headers=RESP_HDR)

        if request.method in ("GET", "HEAD"):
            # downlink stream
            try:
                sess = await get_session(
                    uuid, mode, session_id, _client_ip(request),
                    is_allowed, register_conn, unregister_conn,
                )
            except HTTPException:
                raise
            sess["sid"] = session_id
            if sess.get("closed"):
                raise HTTPException(404, "session closed")

            async def gen():
                q = sess["down_q"]
                try:
                    while True:
                        chunk = await q.get()
                        if chunk is None:
                            break
                        sess["last"] = time.time()
                        yield chunk
                except asyncio.CancelledError:
                    pass

            return StreamingResponse(
                gen(),
                media_type=RESP_HDR["content-type"],
                headers={k: v for k, v in RESP_HDR.items() if k != "content-type"},
            )

        # POST/PUT uplink
        try:
            sess = await get_session(
                uuid, mode, session_id, _client_ip(request),
                is_allowed, register_conn, unregister_conn,
            )
        except HTTPException:
            raise
        sess["sid"] = session_id
        if sess.get("closed"):
            raise HTTPException(404, "session closed")

        proto = get_proto(uuid)
        writer = sess.get("writer")

        try:
            async for chunk in request.stream():
                if not chunk:
                    continue
                sess["last"] = time.time()
                if on_usage and not on_usage(uuid, len(chunk)):
                    raise HTTPException(403, "quota")

                if writer is None:
                    await open_tcp_session(sess, chunk, proto, on_usage)
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
            logger.debug("xhttp uplink error: %s", e)
            await teardown(session_id, str(e))
            raise HTTPException(502, "uplink failed")

        return Response(status_code=200, headers=RESP_HDR)

    # stream-one shorthand: single path without session in template — client still sends session
    @router.api_route("/xhttp/{uuid}", methods=["GET", "POST"])
    async def xhttp_short(uuid: str, request: Request):
        # fallback session id from header or generate per-request (weak)
        sid = request.headers.get("x-session-id") or secrets.token_urlsafe(8)
        return await xhttp_session("stream-up", uuid, sid, request)

    return router
