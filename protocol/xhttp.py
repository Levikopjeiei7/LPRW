"""
LPRW XHTTP — Railway-compatible routes matching Xray client layout.

Share path: /xhttp-siz10/stream-up/{uuid}  or  /xhttp-siz10/packet-up/{uuid}
Client adds: /{sessionId}  (+ /{seq} for packet-up)

Critical fixes vs earlier versions:
- buffer uplink until full VLESS/Trojan header is available
- scan for UUID if padding precedes header
- packet-up uses request.body() (proxy-friendly)
- both /xhttp-siz10 and /xhttp prefixes
"""
from __future__ import annotations

import asyncio
import logging
import time
import uuid as uuidlib
from typing import Callable, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response, StreamingResponse

from protocol.common import open_tcp, tune_socket
from protocol.trojan import parse_trojan_header
from protocol.vless import parse_vless_header

logger = logging.getLogger("LPRW.xhttp")
router = APIRouter()

XHTTP_BUF = 1024 * 1024
SESSIONS: dict = {}
LOCK = asyncio.Lock()
_reaper = False
IDLE_NEW = 45
IDLE_ACTIVE = 120

HDR = {
    "content-type": "application/grpc",
    "cache-control": "no-cache, no-store",
    "x-accel-buffering": "no",
    "server": "cloudflare",
}


def ensure_reaper():
    global _reaper
    if _reaper:
        return
    _reaper = True

    async def loop():
        while True:
            await asyncio.sleep(12)
            now = time.time()
            async with LOCK:
                stale = [
                    sid
                    for sid, s in SESSIONS.items()
                    if now - s["last"] > (IDLE_ACTIVE if s.get("tcp") else IDLE_NEW)
                ]
            for sid in stale:
                await teardown(sid, "idle")

    asyncio.create_task(loop())


async def teardown(sid: str, reason: str = ""):
    async with LOCK:
        sess = SESSIONS.pop(sid, None)
    if not sess:
        return
    sess["closed"] = True
    t = sess.get("down_task")
    if t:
        t.cancel()
        try:
            await t
        except (asyncio.CancelledError, Exception):
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
    logger.info("xhttp teardown %s %s", sid[:8], reason)


async def get_or_create(sid, uuid, mode, is_allowed, reg, unreg, ip: str):
    async with LOCK:
        sess = SESSIONS.get(sid)
        if sess is not None:
            # A session id belongs to exactly one credential/mode.  Reusing it
            # with a different link must never attach to an existing tunnel.
            if sess.get("uuid") != uuid:
                raise HTTPException(403, "session credential mismatch")
            if sess.get("mode") != mode:
                raise HTTPException(400, "session mode mismatch")
            if sess.get("closed"):
                raise HTTPException(404, "session closed")
            sess["last"] = time.time()
            return sess
        link = is_allowed(uuid)
        if not link:
            raise HTTPException(403, "not authorized")
        cid = reg(uuid)
        sess = {
            "uuid": uuid,
            "mode": mode,
            "writer": None,
            "q": asyncio.Queue(maxsize=512),
            "last": time.time(),
            "cid": cid,
            "unreg": unreg,
            "closed": False,
            "tcp": False,
            "seq_buf": {},
            "next_seq": 0,
            "buf": bytearray(),
            "ip": ip,
        }
        SESSIONS[sid] = sess
        logger.info("xhttp[%s] new %s uuid=%s ip=%s", mode, sid[:8], uuid[:8], ip)
        return sess


def _uuid_bytes(uid: str) -> Optional[bytes]:
    try:
        return uuidlib.UUID(uid).bytes
    except Exception:
        return None


def _locate_header(data: bytes, uid: str, is_trojan: bool) -> int:
    """Return offset of protocol header inside data (0 if at start). Handles padding."""
    if not data:
        return 0
    if is_trojan:
        # trojan: 56 hex + \r\n
        if len(data) >= 58 and data[56:58] == b"\r\n":
            return 0
        idx = data.find(b"\r\n")
        if idx == 56:
            return 0
        # search for \r\n at position that makes 56-byte hex before it
        pos = 0
        while True:
            idx = data.find(b"\r\n", pos)
            if idx < 0:
                return 0
            if idx >= 56:
                return idx - 56
            pos = idx + 1
        return 0
    ub = _uuid_bytes(uid)
    if ub and len(data) >= 17:
        # version(1) + uuid(16)
        for i in range(0, min(len(data) - 17, 512)):
            if data[i + 1 : i + 17] == ub:
                return i
    return 0


def _try_parse(data: bytes, uid: str, is_trojan: bool):
    off = _locate_header(data, uid, is_trojan)
    chunk = data[off:]
    if is_trojan:
        if len(chunk) < 58:
            return None  # need more
        _, cmd, address, port, payload = parse_trojan_header(chunk)
        return cmd, address, port, payload, False
    if len(chunk) < 24:
        return None
    try:
        cmd, address, port, payload = parse_vless_header(chunk)
        return cmd, address, port, payload, True
    except Exception:
        return None


async def pump(reader, sess, on_usage, sid, vless_prefix: bool):
    first = True
    uuid = sess["uuid"]
    try:
        while True:
            try:
                data = await reader.read(XHTTP_BUF)
            except Exception:
                break
            if not data:
                break
            sess["last"] = time.time()
            if on_usage and not on_usage(uuid, len(data)):
                break
            if vless_prefix and first:
                await sess["q"].put(b"\x00\x00" + data)
                first = False
            else:
                await sess["q"].put(data)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.debug("pump %s", e)
    finally:
        try:
            await sess["q"].put(None)
        except Exception:
            pass
        await teardown(sid, "remote-eof")


async def open_tcp_session(sid, uuid, sess, header_bytes, get_proto, on_usage):
    proto = get_proto(uuid)
    is_trojan = proto == "trojan"
    parsed = _try_parse(header_bytes, uuid, is_trojan)
    if parsed is None:
        raise ValueError("incomplete header")
    cmd, address, port, payload, vless_prefix = parsed
    if cmd != 0x01:
        raise ValueError("udp not supported")
    reader, writer = await open_tcp(address, port, timeout=10.0)
    tune_socket(writer)
    if payload:
        writer.write(payload)
        await writer.drain()
    sess["writer"] = writer
    sess["tcp"] = True
    if vless_prefix:
        try:
            sess["q"].put_nowait(b"\x00\x00")
        except Exception:
            pass
    sess["down_task"] = asyncio.create_task(
        pump(reader, sess, on_usage, sid, vless_prefix)
    )
    logger.info("xhttp tcp -> %s:%s", address, port)


def _client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "?"


async def _handle_uplink_stream(sess, sid, uuid, request, get_proto, on_usage):
    """Accumulate until header parses, then relay rest to TCP."""
    writer = sess.get("writer")
    async for chunk in request.stream():
        if not chunk:
            continue
        sess["last"] = time.time()
        if on_usage and not on_usage(uuid, len(chunk)):
            raise HTTPException(403, "quota")
        if writer is None:
            sess["buf"].extend(chunk)
            try:
                await open_tcp_session(sid, uuid, sess, bytes(sess["buf"]), get_proto, on_usage)
                sess["buf"].clear()
                writer = sess["writer"]
            except ValueError as e:
                if "incomplete" in str(e):
                    if len(sess["buf"]) > 65536:
                        raise HTTPException(400, "bad header")
                    continue
                raise
            continue
        if writer.is_closing():
            raise ConnectionError("closing")
        writer.write(chunk)
        if writer.transport.get_write_buffer_size() > 512 * 1024:
            await writer.drain()


def bind_handlers(is_allowed, on_usage, register_conn, unregister_conn, get_proto: Callable):
    @router.get("/xhttp-siz10/{mode}/{uuid}/{session_id}")
    @router.get("/xhttp-siz10/{mode}/{uuid}/{session_id}/")
    @router.get("/xhttp/{mode}/{uuid}/{session_id}")
    @router.get("/xhttp/{mode}/{uuid}/{session_id}/")
    async def downlink(mode: str, uuid: str, session_id: str, request: Request):
        ensure_reaper()
        if mode not in ("packet-up", "stream-up"):
            raise HTTPException(404, "unknown xhttp mode")
        sess = await get_or_create(
            session_id, uuid, mode, is_allowed, register_conn, unregister_conn, _client_ip(request)
        )
        if sess.get("closed"):
            raise HTTPException(404, "session closed")

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
            headers={k: v for k, v in HDR.items() if k != "content-type"},
        )

    @router.post("/xhttp-siz10/stream-up/{uuid}/{session_id}")
    @router.post("/xhttp-siz10/stream-up/{uuid}/{session_id}/")
    @router.post("/xhttp/stream-up/{uuid}/{session_id}")
    @router.put("/xhttp-siz10/stream-up/{uuid}/{session_id}")
    async def stream_up(uuid: str, session_id: str, request: Request):
        ensure_reaper()
        sess = await get_or_create(
            session_id, uuid, "stream-up", is_allowed, register_conn, unregister_conn, _client_ip(request)
        )
        if sess.get("closed"):
            raise HTTPException(404, "session closed")
        try:
            await _handle_uplink_stream(sess, session_id, uuid, request, get_proto, on_usage)
        except HTTPException:
            raise
        except Exception as e:
            logger.warning("stream-up fail: %s", e)
            await teardown(session_id, str(e))
            raise HTTPException(502, "write failed")
        return Response(status_code=200, headers={k: v for k, v in HDR.items() if k != "content-type"})

    @router.post("/xhttp-siz10/packet-up/{uuid}/{session_id}/{seq}")
    @router.post("/xhttp-siz10/packet-up/{uuid}/{session_id}/{seq}/")
    @router.post("/xhttp/packet-up/{uuid}/{session_id}/{seq}")
    @router.post("/xhttp/packet-up/{uuid}/{session_id}/{seq}/")
    @router.put("/xhttp-siz10/packet-up/{uuid}/{session_id}/{seq}")
    @router.put("/xhttp/packet-up/{uuid}/{session_id}/{seq}")
    async def packet_up(uuid: str, session_id: str, seq: int, request: Request):
        """Xray XHTTP packet-up uplink.

        Xray may split the VLESS header across multiple POSTs and POSTs may
        arrive out of order.  The old implementation only retried parsing
        seq=0, so if the header crossed a POST boundary the tunnel never
        connected.  Keep an ordered packet window and consume it strictly in
        sequence; before TCP exists, concatenate contiguous packets into the
        handshake buffer and retry parsing after every packet.
        """
        ensure_reaper()
        if seq < 0 or seq > 0xFFFFFFFFFFFFFFFF:
            raise HTTPException(400, "invalid sequence")

        sess = await get_or_create(
            session_id, uuid, "packet-up", is_allowed, register_conn, unregister_conn, _client_ip(request)
        )
        if sess.get("closed"):
            raise HTTPException(404, "session closed")

        body = await request.body()
        sess["last"] = time.time()

        if body and on_usage and not on_usage(uuid, len(body)):
            await teardown(session_id, "quota")
            raise HTTPException(403, "quota")

        # Duplicate POSTs are harmless.  Xray uses monotonically increasing
        # sequence numbers; retaining only the first copy also prevents a
        # retransmission from being written twice to the target TCP socket.
        if seq < sess["next_seq"]:
            return Response(status_code=200, headers={k: v for k, v in HDR.items() if k != "content-type"})
        if seq in sess["seq_buf"]:
            return Response(status_code=200, headers={k: v for k, v in HDR.items() if k != "content-type"})
        if len(sess["seq_buf"]) >= 512:
            await teardown(session_id, "sequence window full")
            raise HTTPException(409, "too many buffered packets")

        sess["seq_buf"][seq] = body

        try:
            # Consume only a contiguous sequence.  This is important for
            # packet-up because seq=1 can arrive before seq=0.
            while sess["next_seq"] in sess["seq_buf"]:
                current = sess["seq_buf"].pop(sess["next_seq"])
                current_seq = sess["next_seq"]
                sess["next_seq"] += 1

                if sess["writer"] is None:
                    # The VLESS/Trojan handshake can span several POSTs.
                    # Never discard an incomplete packet: append it and retry
                    # after the next contiguous sequence arrives.
                    if current:
                        sess["buf"].extend(current)
                    if len(sess["buf"]) > 128 * 1024:
                        raise ValueError("bad header")

                    try:
                        await open_tcp_session(
                            session_id, uuid, sess, bytes(sess["buf"]), get_proto, on_usage
                        )
                        # open_tcp_session consumes the complete protocol
                        # header and writes its initial payload.  Therefore the
                        # accumulated buffer must not be sent again.
                        sess["buf"].clear()
                    except ValueError as e:
                        if "incomplete" in str(e):
                            continue
                        raise

                    # TCP is now ready. Any bytes after the handshake were
                    # already delivered by open_tcp_session; subsequent
                    # packets are plain application data.
                    continue

                if current:
                    writer = sess["writer"]
                    if writer is None or writer.is_closing():
                        raise ConnectionError("target connection closed")
                    writer.write(current)
                    if writer.transport.get_write_buffer_size() > 2 * 1024 * 1024:
                        await writer.drain()

        except HTTPException:
            raise
        except ValueError as e:
            logger.warning("packet-up header fail sid=%s seq=%s: %s", session_id[:8], seq, e)
            await teardown(session_id, str(e))
            raise HTTPException(400, "invalid xhttp handshake")
        except Exception as e:
            logger.warning("packet-up fail sid=%s seq=%s: %s", session_id[:8], seq, e)
            await teardown(session_id, str(e))
            raise HTTPException(502, "write failed")

        # Xray only needs a successful HTTP status for each uplink POST.
        # Keep the response body empty; this matches Xray's packet-up server
        # behavior and avoids JSON/content-length surprises through proxies.
        return Response(status_code=200, headers={k: v for k, v in HDR.items() if k != "content-type"})

    @router.get("/debug/xhttp-routes")
    async def debug_routes():
        return {
            "ok": True,
            "sessions": len(SESSIONS),
            "version": "4.7",
            "paths": [
                "GET /xhttp-siz10/{mode}/{uuid}/{session}",
                "POST /xhttp-siz10/stream-up/{uuid}/{session}",
                "POST /xhttp-siz10/packet-up/{uuid}/{session}/{seq}",
            ],
        }

    return router
