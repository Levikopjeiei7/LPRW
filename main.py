"""
LPRW — Leviko Panel Railway v3.0
Original multi-protocol gateway for Railway.
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("LPRW")

VERSION = "3.0.0"
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
    """Resolve public panel host. Prefer env / learned host / request headers. Never stick on localhost."""
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
    """Display-only config: remaining volume + days in the remark (fragment)."""
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
    # Non-routable display entry (clients show name; connection is not used)
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
SESS: dict = {}
CONNECTIONS: dict = {}  # conn_id -> info
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
            return
        async with aiofiles.open(DATA_FILE) as f:
            d = json.loads(await f.read())
        LINKS.update(d.get("links", {}))
        SUBS.update(d.get("subs", {}))
        if "ah" in d:
            _admin = d["ah"]
        if "settings" in d:
            SETTINGS.update(d["settings"])
        STATS["bytes"] = d.get("bytes", 0)
        STATS["reqs"] = d.get("reqs", 0)
        log.info("loaded %s links %s subs", len(LINKS), len(SUBS))
    except Exception as e:
        log.warning("load %s", e)

async def save():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            d = {
                "links": dict(LINKS), "subs": dict(SUBS), "ah": _admin,
                "settings": SETTINGS, "bytes": STATS["bytes"], "reqs": STATS["reqs"],
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

def share(link: dict, h: Optional[str] = None) -> str:
    """Share link — params encoded like production gateways (alpn=h2)."""
    h = h or host()
    lab = quote(link.get("label") or "LPRW")
    uid = link["id"]
    proto = link.get("proto", "vless")
    if proto == "trojan":
        path = f"/trojan-ws/{uid}"
        q = "&".join(
            f"{k}={quote(str(v), safe='')}"
            for k, v in {
                "security": "tls", "type": "ws", "host": h,
                "path": path, "sni": h, "fp": "chrome", "alpn": "h2",
            }.items()
        )
        return f"trojan://{uid}@{h}:443?{q}#{lab}"
    path = f"/ws/{uid}"
    q = "&".join(
        f"{k}={quote(str(v), safe='')}"
        for k, v in {
            "encryption": "none", "security": "tls", "type": "ws", "host": h,
            "path": path, "sni": h, "fp": "chrome", "alpn": "h2",
        }.items()
    )
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
    """SYNC lock-free traffic account. Safe under asyncio single-thread."""
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

# models
class LoginIn(BaseModel):
    username: str = "admin"
    password: str

class LinkIn(BaseModel):
    label: str = Field(..., min_length=1, max_length=80)
    proto: str = Field(default="vless", pattern="^(vless|trojan)$")
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
    # Always learn public host from real inbound requests (Railway / reverse proxy)
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
    log.info("LPRW %s host=%s", VERSION, host())

@app.on_event("shutdown")
async def shutdown():
    await save()

@app.get("/")
async def root():
    return {"service": "LPRW", "version": VERSION, "host": host(), "status": "active"}

@app.get("/health")
async def health():
    return {"ok": True, "online": len(CONNECTIONS), "links": len(LINKS), "uptime": int(time.time()-STATS["start"])}

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
        "subs": len(SUBS), "uptime": int(time.time()-STATS["start"]),
        "uptime_h": (lambda s: f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}")(int(time.time()-STATS["start"])),
        "hourly": dict(sorted(HOURLY.items())[-24:]), "host": h,
        "public_host": h,
        "version": VERSION, "announce": SETTINGS.get("announce", ""),
        "connections": [
            {"id": k, "uuid": v.get("uuid", "")[:8], "sec": int(time.time()-v.get("at", time.time()))}
            for k, v in list(CONNECTIONS.items())[:50]
        ],
    }

@app.get("/api/activity")
async def activity(_: bool = Depends(auth)):
    return list(ACT)[::-1][:150]

@app.get("/api/links")
async def list_links(request: Request, _: bool = Depends(auth)):
    h = host(request)
    async with LLOCK:
        rows = [enrich(l, h) for l in LINKS.values()]
    rows.sort(key=lambda x: x.get("created", ""), reverse=True)
    return rows

@app.post("/api/links")
async def create_link(body: LinkIn, request: Request, _: bool = Depends(auth)):
    lid = str(uuidlib.uuid4())
    vol = int(body.volume_gb * 1024**3) if body.volume_gb > 0 else 0
    exp = (now() + timedelta(days=body.days)).isoformat() if body.days > 0 else None
    link = {
        "id": lid, "label": body.label, "proto": body.proto, "vol": vol, "used": 0,
        "exp": exp, "max_conn": body.max_conn, "active": True, "remark": body.remark,
        "created": now().isoformat(),
    }
    async with LLOCK:
        LINKS[lid] = link
    await schedule_save()
    act(f"link created: {body.label}", "ok")
    return {"ok": True, "link": enrich(link, host(request))}

@app.patch("/api/links/{lid}")
async def patch_link(lid: str, body: LinkPatch, _: bool = Depends(auth)):
    async with LLOCK:
        if lid not in LINKS:
            raise HTTPException(404)
        l = LINKS[lid]
        if body.label is not None: l["label"] = body.label
        if body.volume_gb is not None: l["vol"] = int(body.volume_gb * 1024**3) if body.volume_gb > 0 else 0
        if body.days is not None: l["exp"] = (now() + timedelta(days=body.days)).isoformat() if body.days > 0 else None
        if body.max_conn is not None: l["max_conn"] = body.max_conn
        if body.active is not None: l["active"] = body.active
        if body.remark is not None: l["remark"] = body.remark
        if body.reset_usage: l["used"] = 0
    await schedule_save()
    return {"ok": True}

@app.delete("/api/links/{lid}")
async def del_link(lid: str, _: bool = Depends(auth)):
    async with LLOCK:
        if lid not in LINKS:
            raise HTTPException(404)
        lab = LINKS[lid].get("label", "")
        del LINKS[lid]
    await schedule_save()
    act(f"link deleted: {lab}", "warn")
    return {"ok": True}

@app.get("/api/subs")
async def list_subs(request: Request, _: bool = Depends(auth)):
    h = host(request)
    async with SLOCK:
        out = []
        for s in SUBS.values():
            o = dict(s)
            o["url"] = f"https://{h}/sub-group/{s['id']}"
            o["used_h"] = bh(s.get("used", 0))
            vol = s.get("vol", 0)
            o["vol_h"] = "نامحدود" if vol <= 0 else bh(vol)
            out.append(o)
    return out

@app.post("/api/subs")
async def create_sub(body: SubIn, request: Request, _: bool = Depends(auth)):
    sid = secrets.token_urlsafe(14)
    vol = int(body.volume_gb * 1024**3) if body.volume_gb > 0 else 0
    exp = (now() + timedelta(days=body.days)).isoformat() if body.days > 0 else None
    sub = {"id": sid, "name": body.name, "link_ids": body.link_ids, "vol": vol, "used": 0, "exp": exp, "created": now().isoformat()}
    async with SLOCK:
        SUBS[sid] = sub
    await schedule_save()
    act(f"sub created: {body.name}", "ok")
    return {"ok": True, "sub": sub, "url": f"https://{host(request)}/sub-group/{sid}"}

@app.delete("/api/subs/{sid}")
async def del_sub(sid: str, _: bool = Depends(auth)):
    async with SLOCK:
        if sid not in SUBS:
            raise HTTPException(404)
        del SUBS[sid]
    await schedule_save()
    return {"ok": True}

@app.get("/api/settings")
async def get_set(_: bool = Depends(auth)):
    return SETTINGS

@app.post("/api/settings")
async def set_set(body: SettingsIn, _: bool = Depends(auth)):
    SETTINGS.update(body.model_dump(exclude_none=True))
    await schedule_save()
    return {"ok": True, "settings": SETTINGS}

@app.post("/api/password")
async def chg_pw(body: PasswordIn, _: bool = Depends(auth)):
    global _admin
    if hp(body.current) != _admin:
        raise HTTPException(400, "wrong current password")
    _admin = hp(body.new_password)
    await schedule_save()
    act("password changed", "ok")
    return {"ok": True}

@app.get("/api/backup")
async def backup(_: bool = Depends(auth)):
    return {"links": dict(LINKS), "subs": dict(SUBS), "settings": SETTINGS, "version": VERSION}

# Public sub single (base64 like many clients expect)
@app.get("/sub/{lid}")
async def pub_sub_one(lid: str, request: Request):
    async with LLOCK:
        lk = LINKS.get(lid)
        if not lk or not allowed(lk):
            raise HTTPException(404)
        h = host(request)
        lines = [status_line(lk, h), share(lk, h)]
        used = lk.get("used", 0)
        total = lk.get("vol", 0)
        exp = lk.get("exp")
        label = lk.get("label") or "LPRW"
    expire_ts = 0
    if exp:
        try:
            expire_ts = int(datetime.fromisoformat(exp).timestamp())
        except Exception:
            expire_ts = 0
    content = base64.b64encode("\n".join(lines).encode()).decode()
    title_b64 = base64.b64encode(label.encode()).decode()
    return Response(
        content=content,
        media_type="text/plain; charset=utf-8",
        headers={
            "profile-update-interval": "6",
            "profile-title": f"base64:{title_b64}",
            "subscription-userinfo": f"upload=0; download={used}; total={total}; expire={expire_ts}",
        },
    )

@app.get("/sub-group/{sid}")
async def pub_sub_group(sid: str, request: Request):
    async with SLOCK:
        sub = SUBS.get(sid)
        if not sub:
            raise HTTPException(404)
        if sub.get("exp"):
            try:
                if datetime.fromisoformat(sub["exp"]) < now():
                    raise HTTPException(403, "expired")
            except HTTPException:
                raise
            except Exception:
                pass
        h = host(request)
        lines = []
        total_used = 0
        total_vol = 0
        async with LLOCK:
            ids = sub.get("link_ids") or list(LINKS.keys())
            for i in ids:
                lk = LINKS.get(i)
                if lk and allowed(lk):
                    lines.append(status_line(lk, h))
                    lines.append(share(lk, h))
                    total_used += int(lk.get("used", 0) or 0)
                    total_vol += int(lk.get("vol", 0) or 0)
        if not lines:
            fake = {"label": sub.get("name") or "LPRW", "used": sub.get("used", 0), "vol": sub.get("vol", 0), "exp": sub.get("exp")}
            lines = [status_line(fake, h)]
    content = base64.b64encode("\n".join(lines).encode()).decode()
    expire_ts = 0
    if sub.get("exp"):
        try:
            expire_ts = int(datetime.fromisoformat(sub["exp"]).timestamp())
        except Exception:
            expire_ts = 0
    title_b64 = base64.b64encode((sub.get("name") or "LPRW").encode()).decode()
    return Response(
        content=content,
        media_type="text/plain; charset=utf-8",
        headers={
            "profile-update-interval": "6",
            "profile-title": f"base64:{title_b64}",
            "subscription-userinfo": f"upload=0; download={total_used}; total={total_vol}; expire={expire_ts}",
        },
    )


@app.get("/qr/{lid}")
async def qr(lid: str, request: Request):
    async with LLOCK:
        lk = LINKS.get(lid)
        if not lk:
            raise HTTPException(404)
        text = share(lk, host(request))
    img = qrcode.make(text)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/u/{lid}")
async def user_page(lid: str, request: Request):
    async with LLOCK:
        lk = LINKS.get(lid)
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
        .replace("{{HOST}}", d.get("share", "").split("@")[-1].split(":")[0] if "@" in d.get("share", "") else host(request))
        .replace("{{VERSION}}", VERSION)
    )
    return HTMLResponse(html)

# ── CRITICAL: path includes UUID (same architecture as working gateways) ──
@app.websocket("/ws/{uid}")
async def ws_vless(ws: WebSocket, uid: str):
    def is_ok(u):
        return find_link(u)
    await handle_vless_ws(ws, uid, is_ok, on_usage, reg_conn, unreg_conn)
    asyncio.create_task(schedule_save())

@app.websocket("/trojan-ws/{uid}")
async def ws_trojan(ws: WebSocket, uid: str):
    def is_ok(u):
        lk = find_link(u)
        if lk and lk.get("proto") == "trojan":
            return lk
        # allow if link exists as trojan even when path password matches id
        return lk if lk and lk.get("proto", "vless") == "trojan" else (find_link(u) if find_link(u) and find_link(u).get("proto") == "trojan" else None)
    # simpler:
    def is_ok2(u):
        lk = find_link(u)
        return lk if lk and lk.get("proto") == "trojan" else None
    await handle_trojan_ws(ws, uid, is_ok2, on_usage, reg_conn, unreg_conn)
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
