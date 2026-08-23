"""
LPRW — Leviko Panel Railway v4.0
Multi-protocol gateway with Inbound management, SS, optimized relays.
Networks: ws / httpupgrade / xhttp (link generation + WS backend)
Protocols: vless / trojan / ss
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import io
import json
import logging
import os
import secrets
import time
import uuid as uuidlib
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote

import aiofiles
import qrcode
from fastapi import Depends, FastAPI, HTTPException, Request, Response, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, StreamingResponse
from pydantic import BaseModel, Field

from protocol.vless import handle_vless_ws
from protocol.trojan import handle_trojan_ws
from protocol.ss import handle_ss_ws

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("LPRW")

VERSION = "4.0.0"
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "lprw.json"
SECRET_FILE = DATA_DIR / ".secret"
TZ = timezone(timedelta(hours=3, minutes=30))
COOKIE = "lprw_sid"
TTL = 86400 * 7

def _secret() -> str:
    if os.environ.get("SECRET_KEY"):
        return os.environ["SECRET_KEY"]
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if SECRET_FILE.exists():
            v = SECRET_FILE.read_text().strip()
            if v:
                return v
        n = secrets.token_urlsafe(40)
        SECRET_FILE.write_text(n)
        return n
    except Exception:
        return secrets.token_urlsafe(40)

SECRET = _secret()
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PW = os.environ.get("ADMIN_PASSWORD", "12345")
PORT = int(os.environ.get("PORT", 8000))

def host(request: Optional[Request] = None) -> str:
    candidates = []
    for key in ("RAILWAY_PUBLIC_DOMAIN", "RAILWAY_STATIC_URL", "PUBLIC_HOST", "HOST", "DOMAIN"):
        v = (os.environ.get(key) or "").strip()
        if v:
            candidates.append(v)
    ph = (SETTINGS.get("public_host") or "").strip()
    if ph:
        candidates.append(ph)
    if request is not None:
        for hk in ("x-forwarded-host", "x-original-host", "host"):
            raw = (request.headers.get(hk) or "").split(",")[0].strip()
            if raw:
                candidates.append(raw)
        try:
            if request.url.hostname:
                candidates.append(request.url.hostname)
        except Exception:
            pass
    cleaned = []
    for h in candidates:
        h = (h or "").replace("https://", "").replace("http://", "").split("/")[0].strip()
        if not h:
            continue
        if ":" in h and not h.startswith("["):
            host_part, _, port = h.rpartition(":")
            if port.isdigit() and port in ("80", "443"):
                h = host_part
        if h and h not in cleaned:
            cleaned.append(h)
    for h in cleaned:
        if h not in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            return h
    return cleaned[0] if cleaned else "localhost"


def status_line(link: dict, h: str) -> str:
    used = int(link.get("used", 0) or 0)
    vol = int(link.get("vol", 0) or 0)
    if vol <= 0:
        left_h = "نامحدود"
    else:
        left_h = bh(max(0, vol - used))
    days = "نامحدود"
    exp = link.get("exp")
    if exp:
        try:
            delta = datetime.fromisoformat(exp) - now()
            days = f"{max(0, delta.days)} روز"
        except Exception:
            days = str(exp)[:10]
    used_h = bh(used)
    vol_h = "نامحدود" if vol <= 0 else bh(vol)
    label = link.get("label") or "LPRW"
    remark = quote(f"📊 {label} | باقیمانده {left_h} از {vol_h} | {days}")
    return (
        f"vless://00000000-0000-0000-0000-000000000001@127.0.0.1:80"
        f"?encryption=none&security=none&type=tcp&headerType=none#{remark}"
    )

def now() -> datetime:
    return datetime.now(TZ)

def hp(p: str) -> str:
    return hashlib.sha256(f"{p}{SECRET}".encode()).hexdigest()

def bh(n: float) -> str:
    for u in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024:
            return f"{n:.2f} {u}"
        n /= 1024
    return f"{n:.2f} PB"

_admin = hp(ADMIN_PW)
LINKS: dict = {}
SUBS: dict = {}
INBOUNDS: dict = {}
SESS: dict = {}
CONNECTIONS: dict = {}
STATS = {"bytes": 0, "reqs": 0, "errors": 0, "start": time.time()}
ACT: deque = deque(maxlen=500)
HOURLY: dict = defaultdict(int)
SETTINGS = {
    "panel_name": os.environ.get("PANEL_NAME", "LPRW"),
    "announce": "",
    "support_url": "",
}
LLOCK = asyncio.Lock()
SLOCK = asyncio.Lock()
XLOCK = asyncio.Lock()
ILOCK = asyncio.Lock()
SAVE_LOCK = asyncio.Lock()
_pending = False

def act(msg: str, level: str = "info"):
    ACT.append({"msg": msg, "level": level, "t": now().isoformat()})

def allowed(l: Optional[dict]) -> bool:
    if not l or not l.get("active", True):
        return False
    if l.get("vol", 0) > 0 and l.get("used", 0) >= l["vol"]:
        return False
    exp = l.get("exp")
    if exp:
        try:
            if datetime.fromisoformat(exp) < now():
                return False
        except Exception:
            pass
    return True

async def load():
    global _admin
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            # seed default inbound
            await _ensure_default_inbound()
            return
        async with aiofiles.open(DATA_FILE) as f:
            d = json.loads(await f.read())
        LINKS.update(d.get("links", {}))
        SUBS.update(d.get("subs", {}))
        INBOUNDS.update(d.get("inbounds", {}))
        if "ah" in d:
            _admin = d["ah"]
        if "settings" in d:
            SETTINGS.update(d["settings"])
        STATS["bytes"] = d.get("bytes", 0)
        STATS["reqs"] = d.get("reqs", 0)
        if not INBOUNDS:
            await _ensure_default_inbound()
        log.info("loaded %s links %s subs %s inbounds", len(LINKS), len(SUBS), len(INBOUNDS))
    except Exception as e:
        log.warning("load %s", e)
        await _ensure_default_inbound()

async def _ensure_default_inbound():
    if INBOUNDS:
        return
    iid = "default-vless-ws"
    INBOUNDS[iid] = {
        "id": iid,
        "name": "VLESS-WS-TLS",
        "proto": "vless",
        "network": "ws",
        "security": "tls",
        "path": "/ws",
        "active": True,
        "created": now().isoformat(),
    }
    iid2 = "default-trojan-ws"
    INBOUNDS[iid2] = {
        "id": iid2,
        "name": "Trojan-WS-TLS",
        "proto": "trojan",
        "network": "ws",
        "security": "tls",
        "path": "/trojan-ws",
        "active": True,
        "created": now().isoformat(),
    }

async def save():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            d = {
                "links": dict(LINKS), "subs": dict(SUBS), "inbounds": dict(INBOUNDS),
                "ah": _admin, "settings": SETTINGS,
                "bytes": STATS["bytes"], "reqs": STATS["reqs"],
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w") as f:
                await f.write(json.dumps(d, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            log.warning("save %s", e)

async def schedule_save():
    global _pending
    if _pending:
        return
    _pending = True
    try:
        await asyncio.sleep(1.5)
        await save()
    finally:
        _pending = False

async def new_sess() -> str:
    t = secrets.token_urlsafe(32)
    async with XLOCK:
        SESS[t] = time.time() + TTL
    return t

async def ok_sess(t: Optional[str]) -> bool:
    if not t:
        return False
    async with XLOCK:
        exp = SESS.get(t)
        if not exp or exp < time.time():
            SESS.pop(t, None)
            return False
        return True

async def auth(req: Request):
    if not await ok_sess(req.cookies.get(COOKIE)):
        raise HTTPException(401, "unauthorized")
    return True

def _path_for(inbound: dict, uid: str) -> str:
    net = inbound.get("network", "ws")
    proto = inbound.get("proto", "vless")
    base = inbound.get("path") or ""
    if proto == "trojan":
        if net == "ws":
            return f"/trojan-ws/{uid}"
        if net == "httpupgrade":
            return f"/trojan-hu/{uid}"
        if net == "xhttp":
            return f"/trojan-xhttp/{uid}"
        return f"/trojan-ws/{uid}"
    if proto == "ss":
        return f"/ss-ws/{uid}"
    # vless
    if net == "ws":
        return f"/ws/{uid}"
    if net == "httpupgrade":
        return f"/hu/{uid}"
    if net == "xhttp":
        return f"/xhttp/{uid}"
    return f"/ws/{uid}"

def share(link: dict, h: Optional[str] = None) -> str:
    """Generate client share link according to inbound settings."""
    h = h or host()
    lab = quote(link.get("label") or "LPRW")
    uid = link["id"]
    inbound_id = link.get("inbound_id")
    inbound = INBOUNDS.get(inbound_id) if inbound_id else None
    if not inbound:
        # fallback from legacy proto field
        proto = link.get("proto", "vless")
        network = "ws"
        security = "tls"
    else:
        proto = inbound.get("proto", "vless")
        network = inbound.get("network", "ws")
        security = inbound.get("security", "tls")

    path = _path_for(inbound or {"proto": proto, "network": network, "path": ""}, uid)

    # map network name for client
    type_map = {"ws": "ws", "httpupgrade": "httpupgrade", "xhttp": "xhttp"}
    net_type = type_map.get(network, "ws")

    if proto == "ss":
        # ss://method:password@host:port?params#remark
        method = "aes-256-gcm"
        password = link.get("ss_password") or uid
        userinfo = base64.urlsafe_b64encode(f"{method}:{password}".encode()).decode().rstrip("=")
        q = f"type={net_type}&path={quote(path)}&host={h}&security={security}&sni={h}&fp=chrome"
        if security == "tls":
            q += "&alpn=h2"
        return f"ss://{userinfo}@{h}:443?{q}#{lab}"

    if proto == "trojan":
        params = {
            "security": security if security != "none" else "none",
            "type": net_type,
            "host": h,
            "path": path,
            "sni": h,
            "fp": "chrome",
        }
        if security == "tls":
            params["alpn"] = "h2"
        q = "&".join(f"{k}={quote(str(v), safe='')}" for k, v in params.items())
        return f"trojan://{uid}@{h}:443?{q}#{lab}"

    # vless
    params = {
        "encryption": "none",
        "security": security if security != "none" else "none",
        "type": net_type,
        "host": h,
        "path": path,
        "sni": h,
        "fp": "chrome",
    }
    if security == "tls":
        params["alpn"] = "h2"
    if net_type == "xhttp":
        params["mode"] = "auto"
    q = "&".join(f"{k}={quote(str(v), safe='')}" for k, v in params.items())
    return f"vless://{uid}@{h}:443?{q}#{lab}"

def enrich(l: dict, h: str) -> dict:
    o = dict(l)
    o["used_h"] = bh(l.get("used", 0))
    vol = l.get("vol", 0)
    o["vol_h"] = "نامحدود" if vol <= 0 else bh(vol)
    o["pct"] = min(100, int(l.get("used", 0) / vol * 100)) if vol > 0 else 0
    o["ok"] = allowed(l)
    o["share"] = share(l, h)
    o["online"] = sum(1 for c in CONNECTIONS.values() if c.get("uuid") == l["id"])
    o["user_url"] = f"https://{h}/u/{l['id']}"
    o["qr_url"] = f"https://{h}/qr/{l['id']}"
    o["sub_url"] = f"https://{h}/sub/{l['id']}"
    iid = l.get("inbound_id")
    if iid and iid in INBOUNDS:
        o["inbound_name"] = INBOUNDS[iid].get("name", iid)
        o["proto"] = INBOUNDS[iid].get("proto", l.get("proto", "vless"))
        o["network"] = INBOUNDS[iid].get("network", "ws")
    else:
        o["inbound_name"] = "—"
        o["proto"] = l.get("proto", "vless")
        o["network"] = "ws"
    return o

def find_link(uid: str) -> Optional[dict]:
    if uid in LINKS and allowed(LINKS[uid]):
        return LINKS[uid]
    compact = uid.replace("-", "").lower()
    for lid, lk in LINKS.items():
        if lid.replace("-", "").lower() == compact and allowed(lk):
            return lk
    return None

def on_usage(uid: str, n: int) -> bool:
    STATS["bytes"] += n
    STATS["reqs"] += 1
    HOURLY[time.strftime("%H:00")] += n
    link = LINKS.get(uid)
    if link is None:
        compact = uid.replace("-", "").lower()
        for lid, lk in LINKS.items():
            if lid.replace("-", "").lower() == compact:
                link = lk
                break
    if link is None:
        return False
    if not link.get("active", True):
        return False
    link["used"] = link.get("used", 0) + n
    vol = link.get("vol", 0)
    if vol > 0 and link["used"] >= vol:
        return False
    return True

def reg_conn(uid: str) -> str:
    cid = secrets.token_urlsafe(6)
    CONNECTIONS[cid] = {"uuid": uid, "at": time.time(), "bytes": 0}
    return cid

def unreg_conn(cid: str):
    CONNECTIONS.pop(cid, None)

# ── models ──
class LoginIn(BaseModel):
    username: str = "admin"
    password: str

class InboundIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    proto: str = Field(..., pattern="^(vless|trojan|ss)$")
    network: str = Field(..., pattern="^(ws|xhttp|httpupgrade)$")
    security: str = Field(default="tls", pattern="^(tls|none)$")
    path: str = Field(default="", max_length=120)

class InboundPatch(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None
    path: Optional[str] = None

class LinkIn(BaseModel):
    label: str = Field(..., min_length=1, max_length=80)
    inbound_id: str = Field(..., min_length=1)
    volume_gb: float = Field(default=0, ge=0)
    days: int = Field(default=0, ge=0)
    max_conn: int = Field(default=0, ge=0)
    remark: str = Field(default="", max_length=200)

class LinkPatch(BaseModel):
    label: Optional[str] = None
    volume_gb: Optional[float] = None
    days: Optional[int] = None
    max_conn: Optional[int] = None
    active: Optional[bool] = None
    remark: Optional[str] = None
    reset_usage: Optional[bool] = None
    inbound_id: Optional[str] = None

class SubIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    link_ids: list[str] = Field(default_factory=list)
    volume_gb: float = Field(default=0, ge=0)
    days: int = Field(default=0, ge=0)

class SettingsIn(BaseModel):
    panel_name: Optional[str] = None
    announce: Optional[str] = None
    support_url: Optional[str] = None

class PasswordIn(BaseModel):
    current: str
    new_password: str = Field(..., min_length=4)

app = FastAPI(title="LPRW", docs_url=None, redoc_url=None)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def capture_host(request: Request, call_next):
    try:
        xf = (request.headers.get("x-forwarded-host") or "").split(",")[0].strip()
        hdr = (request.headers.get("host") or "").split(",")[0].strip()
        for raw in (xf, hdr):
            if not raw:
                continue
            h = raw.replace("https://", "").replace("http://", "").split("/")[0].strip()
            if ":" in h and not h.startswith("["):
                host_part, _, port = h.rpartition(":")
                if port in ("80", "443"):
                    h = host_part
            if h and h not in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
                os.environ["PUBLIC_HOST"] = h
                SETTINGS["public_host"] = h
                break
    except Exception:
        pass
    return await call_next(request)

@app.on_event("startup")
async def startup():
    await load()
    act(f"LPRW {VERSION} started", "ok")
    log.info("LPRW %s host=%s inbounds=%s", VERSION, host(), len(INBOUNDS))

@app.on_event("shutdown")
async def shutdown():
    await save()

@app.get("/")
async def root():
    return RedirectResponse("/dashboard")

@app.get("/health")
async def health():
    return {"ok": True, "online": len(CONNECTIONS), "links": len(LINKS), "inbounds": len(INBOUNDS), "uptime": int(time.time()-STATS["start"]), "version": VERSION}

@app.post("/api/login")
async def login(body: LoginIn, response: Response):
    user_ok = (body.username or "").strip().lower() == ADMIN_USER.lower()
    if not user_ok or hp(body.password) != _admin:
        raise HTTPException(401, "wrong username or password")
    tok = await new_sess()
    response.set_cookie(COOKIE, tok, httponly=True, max_age=TTL, samesite="lax")
    act(f"admin login ({body.username})", "ok")
    return {"ok": True, "user": ADMIN_USER}

@app.post("/api/logout")
async def logout(request: Request, response: Response):
    t = request.cookies.get(COOKIE)
    if t:
        async with XLOCK:
            SESS.pop(t, None)
    response.delete_cookie(COOKIE)
    return {"ok": True}

@app.get("/api/me")
async def me(_: bool = Depends(auth)):
    return {"ok": True, "version": VERSION, "name": SETTINGS.get("panel_name", "LPRW")}

@app.get("/api/stats")
async def stats(request: Request, _: bool = Depends(auth)):
    h = host(request)
    return {
        "bytes": STATS["bytes"], "bytes_h": bh(STATS["bytes"]), "reqs": STATS["reqs"],
        "online": len(CONNECTIONS),
        "links": len(LINKS), "active_links": sum(1 for l in LINKS.values() if allowed(l)),
        "subs": len(SUBS), "inbounds": len(INBOUNDS),
        "uptime": int(time.time()-STATS["start"]),
        "uptime_h": (lambda s: f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}")(int(time.time()-STATS["start"])),
        "hourly": dict(sorted(HOURLY.items())[-24:]), "host": h,
        "public_host": h, "version": VERSION, "announce": SETTINGS.get("announce", ""),
        "connections": [
            {"id": k, "uuid": v.get("uuid", "")[:8], "sec": int(time.time()-v.get("at", time.time()))}
            for k, v in list(CONNECTIONS.items())[:50]
        ],
    }

@app.get("/api/activity")
async def activity(_: bool = Depends(auth)):
    return list(ACT)[::-1][:150]

# ── Inbounds ──
@app.get("/api/inbounds")
async def list_inbounds(_: bool = Depends(auth)):
    async with ILOCK:
        rows = list(INBOUNDS.values())
    rows.sort(key=lambda x: x.get("created", ""), reverse=True)
    return rows

@app.post("/api/inbounds")
async def create_inbound(body: InboundIn, _: bool = Depends(auth)):
    iid = secrets.token_urlsafe(8)
    path = (body.path or "").strip()
    if not path:
        if body.proto == "trojan":
            path = "/trojan-ws" if body.network == "ws" else f"/trojan-{body.network}"
        elif body.proto == "ss":
            path = "/ss-ws"
        else:
            path = "/ws" if body.network == "ws" else f"/{body.network}"
    row = {
        "id": iid,
        "name": body.name.strip(),
        "proto": body.proto,
        "network": body.network,
        "security": body.security,
        "path": path,
        "active": True,
        "created": now().isoformat(),
    }
    async with ILOCK:
        INBOUNDS[iid] = row
    await schedule_save()
    act(f"inbound created: {body.name}", "ok")
    return row

@app.patch("/api/inbounds/{iid}")
async def patch_inbound(iid: str, body: InboundPatch, _: bool = Depends(auth)):
    async with ILOCK:
        if iid not in INBOUNDS:
            raise HTTPException(404)
        row = INBOUNDS[iid]
        if body.name is not None:
            row["name"] = body.name.strip()
        if body.active is not None:
            row["active"] = body.active
        if body.path is not None:
            row["path"] = body.path.strip()
    await schedule_save()
    return INBOUNDS[iid]

@app.delete("/api/inbounds/{iid}")
async def delete_inbound(iid: str, _: bool = Depends(auth)):
    async with ILOCK:
        if iid not in INBOUNDS:
            raise HTTPException(404)
        # prevent delete if links use it
        used = any(l.get("inbound_id") == iid for l in LINKS.values())
        if used:
            raise HTTPException(400, "inbound is used by links")
        INBOUNDS.pop(iid)
    await schedule_save()
    act(f"inbound deleted: {iid}", "warn")
    return {"ok": True}

# ── Links ──
@app.get("/api/links")
async def list_links(request: Request, _: bool = Depends(auth)):
    h = host(request)
    async with LLOCK:
        rows = [enrich(l, h) for l in LINKS.values()]
    rows.sort(key=lambda x: x.get("created", ""), reverse=True)
    return rows

@app.post("/api/links")
async def create_link(body: LinkIn, request: Request, _: bool = Depends(auth)):
    if body.inbound_id not in INBOUNDS:
        raise HTTPException(400, "invalid inbound_id")
    inbound = INBOUNDS[body.inbound_id]
    if not inbound.get("active", True):
        raise HTTPException(400, "inbound is disabled")
    lid = str(uuidlib.uuid4())
    vol = int(body.volume_gb * 1024**3) if body.volume_gb > 0 else 0
    exp = (now() + timedelta(days=body.days)).isoformat() if body.days > 0 else None
    row = {
        "id": lid,
        "label": body.label.strip(),
        "inbound_id": body.inbound_id,
        "proto": inbound["proto"],
        "vol": vol,
        "used": 0,
        "exp": exp,
        "max_conn": body.max_conn,
        "active": True,
        "remark": body.remark or "",
        "created": now().isoformat(),
    }
    if inbound["proto"] == "ss":
        row["ss_password"] = secrets.token_urlsafe(16)
    async with LLOCK:
        LINKS[lid] = row
    await schedule_save()
    act(f"link created: {body.label}", "ok")
    return enrich(row, host(request))

@app.patch("/api/links/{lid}")
async def patch_link(lid: str, body: LinkPatch, request: Request, _: bool = Depends(auth)):
    async with LLOCK:
        if lid not in LINKS:
            raise HTTPException(404)
        lk = LINKS[lid]
        if body.label is not None:
            lk["label"] = body.label.strip()
        if body.volume_gb is not None:
            lk["vol"] = int(body.volume_gb * 1024**3) if body.volume_gb > 0 else 0
        if body.days is not None:
            lk["exp"] = (now() + timedelta(days=body.days)).isoformat() if body.days > 0 else None
        if body.max_conn is not None:
            lk["max_conn"] = body.max_conn
        if body.active is not None:
            lk["active"] = body.active
        if body.remark is not None:
            lk["remark"] = body.remark
        if body.reset_usage:
            lk["used"] = 0
        if body.inbound_id is not None:
            if body.inbound_id not in INBOUNDS:
                raise HTTPException(400, "invalid inbound")
            lk["inbound_id"] = body.inbound_id
            lk["proto"] = INBOUNDS[body.inbound_id]["proto"]
    await schedule_save()
    return enrich(LINKS[lid], host(request))

@app.delete("/api/links/{lid}")
async def delete_link(lid: str, _: bool = Depends(auth)):
    async with LLOCK:
        if lid not in LINKS:
            raise HTTPException(404)
        LINKS.pop(lid)
    await schedule_save()
    act(f"link deleted: {lid[:8]}", "warn")
    return {"ok": True}

# ── Subs ──
@app.get("/api/subs")
async def list_subs(request: Request, _: bool = Depends(auth)):
    h = host(request)
    out = []
    for sid, s in SUBS.items():
        o = dict(s)
        o["sub_url"] = f"https://{h}/sub-group/{sid}"
        o["count"] = len(s.get("link_ids", []))
        out.append(o)
    return out

@app.post("/api/subs")
async def create_sub(body: SubIn, request: Request, _: bool = Depends(auth)):
    sid = secrets.token_urlsafe(10)
    vol = int(body.volume_gb * 1024**3) if body.volume_gb > 0 else 0
    exp = (now() + timedelta(days=body.days)).isoformat() if body.days > 0 else None
    row = {
        "id": sid,
        "name": body.name.strip(),
        "link_ids": body.link_ids,
        "vol": vol,
        "exp": exp,
        "created": now().isoformat(),
    }
    async with SLOCK:
        SUBS[sid] = row
    await schedule_save()
    return {**row, "sub_url": f"https://{host(request)}/sub-group/{sid}"}

@app.delete("/api/subs/{sid}")
async def delete_sub(sid: str, _: bool = Depends(auth)):
    async with SLOCK:
        if sid not in SUBS:
            raise HTTPException(404)
        SUBS.pop(sid)
    await schedule_save()
    return {"ok": True}

@app.get("/api/settings")
async def get_settings(_: bool = Depends(auth)):
    return SETTINGS

@app.post("/api/settings")
async def set_settings(body: SettingsIn, _: bool = Depends(auth)):
    if body.panel_name is not None:
        SETTINGS["panel_name"] = body.panel_name
    if body.announce is not None:
        SETTINGS["announce"] = body.announce
    if body.support_url is not None:
        SETTINGS["support_url"] = body.support_url
    await schedule_save()
    return SETTINGS

@app.post("/api/password")
async def change_password(body: PasswordIn, _: bool = Depends(auth)):
    global _admin
    if hp(body.current) != _admin:
        raise HTTPException(400, "current password wrong")
    _admin = hp(body.new_password)
    await schedule_save()
    act("admin password changed", "ok")
    return {"ok": True}

# ── Subscription endpoints ──
@app.get("/sub/{uid}")
async def sub_one(uid: str, request: Request):
    lk = find_link(uid)
    if not lk:
        raise HTTPException(404)
    h = host(request)
    lines = [status_line(lk, h), share(lk, h)]
    raw = "\n".join(lines)
    b64 = base64.b64encode(raw.encode()).decode()
    headers = {
        "profile-title": "base64:" + base64.b64encode((lk.get("label") or "LPRW").encode()).decode(),
        "subscription-userinfo": f"upload=0; download={int(lk.get('used',0))}; total={int(lk.get('vol',0))}; expire={int(datetime.fromisoformat(lk['exp']).timestamp()) if lk.get('exp') else 0}",
        "profile-update-interval": "6",
    }
    return PlainTextResponse(b64, headers=headers)

@app.get("/sub-group/{sid}")
async def sub_group(sid: str, request: Request):
    s = SUBS.get(sid)
    if not s:
        raise HTTPException(404)
    h = host(request)
    lines = []
    for lid in s.get("link_ids", []):
        lk = LINKS.get(lid)
        if lk and allowed(lk):
            lines.append(share(lk, h))
    if not lines:
        lines = [status_line({"label": s.get("name", "LPRW"), "used": 0, "vol": 0}, h)]
    raw = "\n".join(lines)
    b64 = base64.b64encode(raw.encode()).decode()
    return PlainTextResponse(b64)

@app.get("/qr/{uid}")
async def qr(uid: str, request: Request):
    lk = find_link(uid)
    if not lk:
        raise HTTPException(404)
    conf = share(lk, host(request))
    img = qrcode.make(conf)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/u/{uid}", response_class=HTMLResponse)
async def user_portal(uid: str, request: Request):
    async with LLOCK:
        lk = LINKS.get(uid)
        if not lk:
            raise HTTPException(404)
        d = enrich(lk, host(request))
    from pages import USER_PORTAL
    exp = (d.get("exp") or "—")
    if exp and exp != "—":
        exp = exp[:19].replace("T", " ")
    html = (
        USER_PORTAL
        .replace("{{LABEL}}", d.get("label") or "LPRW")
        .replace("{{STATUS}}", "فعال" if d["ok"] else "غیرفعال")
        .replace("{{STATUS_CLASS}}", "ok" if d["ok"] else "bad")
        .replace("{{USED}}", d["used_h"])
        .replace("{{VOL}}", d["vol_h"])
        .replace("{{PCT}}", str(d["pct"]))
        .replace("{{PROTO}}", (d.get("proto") or "vless").upper())
        .replace("{{ONLINE}}", str(d["online"]))
        .replace("{{EXP}}", exp)
        .replace("{{SHARE}}", d["share"])
        .replace("{{SUB}}", d["sub_url"])
        .replace("{{QR}}", d["qr_url"])
        .replace("{{REMARK}}", d.get("remark") or "")
        .replace("{{HOST}}", host(request))
        .replace("{{VERSION}}", VERSION)
    )
    return HTMLResponse(html)

# ── WebSocket / tunnel routes ──
# All networks currently terminate as optimized WS on the server side.
# Client share links advertise the chosen network (ws / httpupgrade / xhttp).
# This is the practical approach for pure-Python Railway gateways.

@app.websocket("/ws/{uid}")
async def ws_vless(ws: WebSocket, uid: str):
    def is_ok(u):
        return find_link(u)
    await handle_vless_ws(ws, uid, is_ok, on_usage, reg_conn, unreg_conn)
    asyncio.create_task(schedule_save())

@app.websocket("/hu/{uid}")
async def hu_vless(ws: WebSocket, uid: str):
    """HTTPUpgrade path — handled as optimized WS for compatibility."""
    def is_ok(u):
        return find_link(u)
    await handle_vless_ws(ws, uid, is_ok, on_usage, reg_conn, unreg_conn)
    asyncio.create_task(schedule_save())

@app.websocket("/xhttp/{uid}")
async def xhttp_vless(ws: WebSocket, uid: str):
    """xHTTP path — handled as optimized WS for compatibility on Railway."""
    def is_ok(u):
        return find_link(u)
    await handle_vless_ws(ws, uid, is_ok, on_usage, reg_conn, unreg_conn)
    asyncio.create_task(schedule_save())

@app.websocket("/trojan-ws/{uid}")
async def ws_trojan(ws: WebSocket, uid: str):
    def is_ok(u):
        lk = find_link(u)
        return lk if lk and lk.get("proto") == "trojan" else None
    await handle_trojan_ws(ws, uid, is_ok, on_usage, reg_conn, unreg_conn)
    asyncio.create_task(schedule_save())

@app.websocket("/trojan-hu/{uid}")
async def hu_trojan(ws: WebSocket, uid: str):
    def is_ok(u):
        lk = find_link(u)
        return lk if lk and lk.get("proto") == "trojan" else None
    await handle_trojan_ws(ws, uid, is_ok, on_usage, reg_conn, unreg_conn)
    asyncio.create_task(schedule_save())

@app.websocket("/trojan-xhttp/{uid}")
async def xhttp_trojan(ws: WebSocket, uid: str):
    def is_ok(u):
        lk = find_link(u)
        return lk if lk and lk.get("proto") == "trojan" else None
    await handle_trojan_ws(ws, uid, is_ok, on_usage, reg_conn, unreg_conn)
    asyncio.create_task(schedule_save())

@app.websocket("/ss-ws/{uid}")
async def ws_ss(ws: WebSocket, uid: str):
    def is_ok(u):
        lk = find_link(u)
        return lk if lk and lk.get("proto") == "ss" else None
    await handle_ss_ws(ws, uid, is_ok, on_usage, reg_conn, unreg_conn)
    asyncio.create_task(schedule_save())

from pages import DASHBOARD, USER_PORTAL  # noqa: E402

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(DASHBOARD)

@app.get("/panel")
async def panel():
    return RedirectResponse("/dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")
