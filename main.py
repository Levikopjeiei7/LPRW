"""
LPRW — Leviko Panel Railway v2.1
Original multi-protocol proxy panel for Railway.
"""
from __future__ import annotations

import asyncio
import hashlib
import io
import json
import logging
import os
import secrets
import time
import uuid
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

VERSION = "2.1.0"
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
ADMIN_PW = os.environ.get("ADMIN_PASSWORD", "admin123")
PORT = int(os.environ.get("PORT", 8000))

def host() -> str:
    h = os.environ.get("RAILWAY_PUBLIC_DOMAIN") or os.environ.get("HOST") or "localhost"
    return h.replace("https://", "").replace("http://", "").split("/")[0].strip()

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
ONLINE: dict = defaultdict(set)
STATS = {"bytes": 0, "reqs": 0, "start": time.time()}
ACT: deque = deque(maxlen=500)
HOURLY: dict = defaultdict(int)
SETTINGS = {
    "panel_name": os.environ.get("PANEL_NAME", "LPRW"),
    "announce": "",
    "support_url": "",
    "path_vless": "/ws",
    "path_trojan": "/trojan",
}
LLOCK = asyncio.Lock()
SLOCK = asyncio.Lock()
XLOCK = asyncio.Lock()
SAVE_LOCK = asyncio.Lock()
_pending = False

def act(msg: str, level: str = "info"):
    ACT.append({"msg": msg, "level": level, "t": now().isoformat()})

def allowed(l: dict) -> bool:
    if not l.get("active", True):
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
        log.info("state: %s links %s subs", len(LINKS), len(SUBS))
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
        await asyncio.sleep(1.0)
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
    h = h or host()
    lab = quote(link.get("label") or "LPRW")
    uid = link["id"]
    if link.get("proto") == "trojan":
        path = quote(SETTINGS.get("path_trojan", "/trojan"))
        return f"trojan://{uid}@{h}:443?security=tls&type=ws&host={h}&path={path}&sni={h}&fp=chrome&alpn=h2,http/1.1#{lab}"
    path = quote(SETTINGS.get("path_vless", "/ws"))
    return f"vless://{uid}@{h}:443?encryption=none&security=tls&type=ws&host={h}&path={path}&sni={h}&fp=chrome&alpn=h2,http/1.1#{lab}"

def enrich(l: dict, h: str) -> dict:
    o = dict(l)
    o["used_h"] = bh(l.get("used", 0))
    vol = l.get("vol", 0)
    o["vol_h"] = "نامحدود" if vol <= 0 else bh(vol)
    o["pct"] = min(100, int(l.get("used", 0) / vol * 100)) if vol > 0 else 0
    o["ok"] = allowed(l)
    o["share"] = share(l, h)
    o["online"] = len(ONLINE.get(l["id"], set()))
    o["user_url"] = f"https://{h}/u/{l['id']}"
    o["qr_url"] = f"https://{h}/qr/{l['id']}"
    o["sub_url"] = f"https://{h}/sub-link/{l['id']}"
    return o

def find_link_by_uuid(uid: str) -> Optional[dict]:
    if uid in LINKS and allowed(LINKS[uid]):
        lk = LINKS[uid]
        return lk if lk.get("proto", "vless") == "vless" else None
    compact = uid.replace("-", "")
    for lid, lk in LINKS.items():
        if lid.replace("-", "") == compact and allowed(lk) and lk.get("proto", "vless") == "vless":
            return lk
    return None

def find_link_by_pass(pw: str) -> Optional[dict]:
    if pw in LINKS and allowed(LINKS[pw]) and LINKS[pw].get("proto") == "trojan":
        return LINKS[pw]
    compact = pw.replace("-", "")
    for lid, lk in LINKS.items():
        if lid.replace("-", "") == compact and allowed(lk) and lk.get("proto") == "trojan":
            return lk
    return None

async def on_usage(lid: str, n: int):
    STATS["bytes"] += n
    STATS["reqs"] += 1
    HOURLY[now().strftime("%H:00")] += n
    async with LLOCK:
        if lid in LINKS:
            LINKS[lid]["used"] = LINKS[lid].get("used", 0) + n

def reg_online(lid: str, cid: str):
    ONLINE[lid].add(cid)

def unreg_online(lid: str, cid: str):
    ONLINE[lid].discard(cid)

# models
class LoginIn(BaseModel):
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
    path_vless: Optional[str] = None
    path_trojan: Optional[str] = None

class PasswordIn(BaseModel):
    current: str
    new_password: str = Field(..., min_length=4)

app = FastAPI(title="LPRW", docs_url=None, redoc_url=None)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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
    return {"ok": True, "online": sum(len(v) for v in ONLINE.values()), "links": len(LINKS), "uptime": int(time.time()-STATS["start"])}

@app.post("/api/login")
async def login(body: LoginIn, response: Response):
    if hp(body.password) != _admin:
        raise HTTPException(401, "wrong password")
    tok = await new_sess()
    response.set_cookie(COOKIE, tok, httponly=True, max_age=TTL, samesite="lax")
    act("admin login", "ok")
    return {"ok": True}

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
async def stats(_: bool = Depends(auth)):
    return {
        "bytes": STATS["bytes"], "bytes_h": bh(STATS["bytes"]), "reqs": STATS["reqs"],
        "online": sum(len(v) for v in ONLINE.values()),
        "links": len(LINKS), "active_links": sum(1 for l in LINKS.values() if allowed(l)),
        "subs": len(SUBS), "uptime": int(time.time()-STATS["start"]),
        "hourly": dict(sorted(HOURLY.items())[-24:]), "host": host(),
        "version": VERSION, "announce": SETTINGS.get("announce", ""),
    }

@app.get("/api/activity")
async def activity(_: bool = Depends(auth)):
    return list(ACT)[::-1][:150]

@app.get("/api/links")
async def list_links(_: bool = Depends(auth)):
    h = host()
    async with LLOCK:
        rows = [enrich(l, h) for l in LINKS.values()]
    rows.sort(key=lambda x: x.get("created", ""), reverse=True)
    return rows

@app.post("/api/links")
async def create_link(body: LinkIn, _: bool = Depends(auth)):
    lid = str(uuid.uuid4())
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
    return {"ok": True, "link": enrich(link, host())}

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
    ONLINE.pop(lid, None)
    await schedule_save()
    act(f"link deleted: {lab}", "warn")
    return {"ok": True}

@app.get("/api/subs")
async def list_subs(_: bool = Depends(auth)):
    h = host()
    async with SLOCK:
        out = []
        for s in SUBS.values():
            o = dict(s)
            o["url"] = f"https://{h}/sub/{s['id']}"
            o["used_h"] = bh(s.get("used", 0))
            vol = s.get("vol", 0)
            o["vol_h"] = "نامحدود" if vol <= 0 else bh(vol)
            out.append(o)
    return out

@app.post("/api/subs")
async def create_sub(body: SubIn, _: bool = Depends(auth)):
    sid = secrets.token_urlsafe(14)
    vol = int(body.volume_gb * 1024**3) if body.volume_gb > 0 else 0
    exp = (now() + timedelta(days=body.days)).isoformat() if body.days > 0 else None
    sub = {"id": sid, "name": body.name, "link_ids": body.link_ids, "vol": vol, "used": 0, "exp": exp, "created": now().isoformat()}
    async with SLOCK:
        SUBS[sid] = sub
    await schedule_save()
    act(f"sub created: {body.name}", "ok")
    return {"ok": True, "sub": sub, "url": f"https://{host()}/sub/{sid}"}

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

@app.get("/sub/{sid}")
async def pub_sub(sid: str):
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
        if sub.get("vol", 0) > 0 and sub.get("used", 0) >= sub["vol"]:
            raise HTTPException(403, "quota")
        h = host()
        lines = []
        async with LLOCK:
            ids = sub.get("link_ids") or list(LINKS.keys())
            for i in ids:
                lk = LINKS.get(i)
                if lk and allowed(lk):
                    lines.append(share(lk, h))
    return PlainTextResponse("\n".join(lines), headers={
        "profile-update-interval": "6",
        "subscription-userinfo": f"upload=0; download={sub.get('used',0)}; total={sub.get('vol',0)}; expire=0",
        "content-disposition": f'attachment; filename="{sub.get("name","lprw")}.txt"',
    })

@app.get("/sub-link/{lid}")
async def sub_one(lid: str):
    async with LLOCK:
        lk = LINKS.get(lid)
        if not lk or not allowed(lk):
            raise HTTPException(404)
        return PlainTextResponse(share(lk, host()))

@app.get("/qr/{lid}")
async def qr(lid: str):
    async with LLOCK:
        lk = LINKS.get(lid)
        if not lk:
            raise HTTPException(404)
        text = share(lk, host())
    img = qrcode.make(text)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/u/{lid}")
async def user_page(lid: str):
    async with LLOCK:
        lk = LINKS.get(lid)
        if not lk:
            raise HTTPException(404)
        d = enrich(lk, host())
    pct = d["pct"]
    st = "فعال" if d["ok"] else "غیرفعال"
    bc = "on" if d["ok"] else "off"
    exp = (d.get("exp") or "—")[:10]
    return HTMLResponse(f"""<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{d['label']}</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap" rel="stylesheet">
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Vazirmatn,sans-serif;background:#06080f;color:#eef0f6;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;background-image:radial-gradient(ellipse at 30% 20%,#1a1540 0%,transparent 50%)}}
.card{{background:rgba(16,18,30,.92);border:1px solid rgba(99,102,241,.3);border-radius:24px;padding:36px;max-width:420px;width:100%;box-shadow:0 30px 80px rgba(0,0,0,.5)}}
h1{{font-size:1.35rem;margin-bottom:10px}}.badge{{display:inline-block;padding:5px 14px;border-radius:99px;font-size:.78rem;font-weight:600;margin-bottom:18px}}
.on{{background:rgba(34,197,94,.15);color:#4ade80}}.off{{background:rgba(239,68,68,.15);color:#f87171}}
.bar{{height:12px;background:#1a1f2e;border-radius:99px;overflow:hidden;margin:16px 0}}.fill{{height:100%;width:{pct}%;background:linear-gradient(90deg,#6366f1,#a855f7);border-radius:99px}}
.row{{display:flex;justify-content:space-between;padding:11px 0;border-bottom:1px solid rgba(255,255,255,.06);font-size:.9rem}}.row span{{color:#94a3b8}}
.foot{{margin-top:20px;text-align:center;font-size:.7rem;color:#475569}}</style></head><body><div class="card">
<h1>{d['label']}</h1><span class="badge {bc}">{st}</span><div class="bar"><div class="fill"></div></div>
<div class="row"><span>مصرف</span><strong>{d['used_h']}</strong></div>
<div class="row"><span>حجم</span><strong>{d['vol_h']}</strong></div>
<div class="row"><span>پروتکل</span><strong>{d['proto'].upper()}</strong></div>
<div class="row"><span>آنلاین</span><strong>{d['online']}</strong></div>
<div class="row"><span>انقضا</span><strong>{exp}</strong></div>
<div class="foot">LPRW · Leviko Panel</div></div></body></html>""")

@app.websocket("/ws")
async def ws_vless(ws: WebSocket):
    await ws.accept()
    await handle_vless_ws(ws, find_link_by_uuid, on_usage, reg_online, unreg_online)
    await schedule_save()

@app.websocket("/trojan")
async def ws_trojan(ws: WebSocket):
    await ws.accept()
    await handle_trojan_ws(ws, find_link_by_pass, on_usage, reg_online, unreg_online)
    await schedule_save()

# UI loaded from pages module
from pages import DASHBOARD  # noqa: E402

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(DASHBOARD)

@app.get("/panel")
async def panel():
    return RedirectResponse("/dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")
