"""
LPRW Xray engine manager.

The panel owns the data model; Xray-core owns the data-plane.  This keeps
traffic forwarding out of the Python/ASGI event loop and fixes the original
relay's throughput/latency bottleneck.

Supported user-facing transports:
  ws, xhttp, httpupgrade
Supported security:
  none, tls

Shadowsocks is deliberately mapped to native TCP/UDP in Xray because
Shadowsocks itself does not define WS/XHTTP/HTTPUpgrade as a native transport.
The UI keeps the requested transport selector but the generated SS share link
is marked TCP so it remains interoperable with standard SS clients.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import platform
import shutil
import stat
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

log = logging.getLogger("LPRW.xray")

XRAY_VERSION = os.environ.get("XRAY_VERSION", "26.7.28")
BASE_DIR = Path(os.environ.get("DATA_DIR", "/data"))
XRAY_DIR = BASE_DIR / "xray"
XRAY_BIN = Path(os.environ.get("XRAY_PATH", str(XRAY_DIR / "xray")))
XRAY_CONFIG = XRAY_DIR / "config.json"
XRAY_LOG = XRAY_DIR / "xray.log"

SUPPORTED_PROTOCOLS = {"vless", "trojan", "ss"}
SUPPORTED_NETWORKS = {"ws", "xhttp", "httpupgrade"}
SUPPORTED_SECURITY = {"none", "tls"}

def _linux_asset() -> str:
    arch = platform.machine().lower()
    if arch in ("x86_64", "amd64"):
        return "Xray-linux-64.zip"
    if arch in ("aarch64", "arm64"):
        return "Xray-linux-arm64-v8a.zip"
    if arch in ("armv7l", "armv7"):
        return "Xray-linux-arm32-v7a.zip"
    if arch in ("i386", "i686", "x86"):
        return "Xray-linux-32.zip"
    raise RuntimeError(f"Unsupported Linux architecture: {arch}")

def _download_url() -> str:
    return f"https://github.com/XTLS/Xray-core/releases/download/v{XRAY_VERSION}/{_linux_asset()}"

def ensure_xray() -> Path:
    if XRAY_BIN.exists() and os.access(XRAY_BIN, os.X_OK):
        return XRAY_BIN
    XRAY_DIR.mkdir(parents=True, exist_ok=True)
    archive = XRAY_DIR / "xray.zip"
    url = _download_url()
    log.info("Downloading Xray-core %s", XRAY_VERSION)
    with urllib.request.urlopen(url, timeout=60) as r, archive.open("wb") as f:
        shutil.copyfileobj(r, f)
    with zipfile.ZipFile(archive) as z:
        member = next((n for n in z.namelist() if n.endswith("/xray") or n == "xray"), None)
        if not member:
            raise RuntimeError("Xray archive does not contain xray binary")
        with z.open(member) as src, XRAY_BIN.open("wb") as dst:
            shutil.copyfileobj(src, dst)
    XRAY_BIN.chmod(XRAY_BIN.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    try:
        archive.unlink()
    except OSError:
        pass
    return XRAY_BIN

def _tls_settings(host: str) -> dict:
    cert = os.environ.get("XRAY_TLS_CERT", "").strip()
    key = os.environ.get("XRAY_TLS_KEY", "").strip()
    if not cert or not key:
        raise ValueError(
            "TLS inbound requires XRAY_TLS_CERT and XRAY_TLS_KEY environment variables"
        )
    return {
        "serverName": host,
        "minVersion": "1.2",
        "maxVersion": "1.3",
        "certificates": [{"certificateFile": cert, "keyFile": key}],
    }

def _stream(inb: dict, host: str) -> dict:
    network = inb.get("network", "ws")
    security = inb.get("security", "none")
    path = inb.get("path") or f"/lprw/{inb['id']}"
    out = {"network": network}
    if network == "ws":
        out["wsSettings"] = {"path": path, "headers": {"Host": host}}
    elif network == "xhttp":
        out["xhttpSettings"] = {
            "path": path,
            "host": host,
            "mode": inb.get("xhttp_mode", "auto"),
        }
    elif network == "httpupgrade":
        out["httpupgradeSettings"] = {"path": path, "host": host}
    else:
        raise ValueError(f"Unsupported network: {network}")
    out["security"] = security
    if security == "tls":
        out["tlsSettings"] = _tls_settings(host)
    return out

def build_config(inbounds: list[dict], host: str) -> dict:
    xs = []
    for inb in inbounds:
        if not inb.get("active", True):
            continue
        proto = inb.get("proto", "vless")
        port = int(inb["port"])
        if proto not in SUPPORTED_PROTOCOLS:
            raise ValueError(f"Unsupported protocol: {proto}")
        if proto == "vless":
            clients = []
            for c in inb.get("clients", []):
                if c.get("active", True):
                    clients.append({
                        "id": c["id"],
                        "email": c.get("label", c["id"][:8]),
                        "level": 0,
                    })
            if not clients:
                continue
            item = {
                "listen": "0.0.0.0", "port": port, "protocol": "vless",
                "settings": {"clients": clients, "decryption": "none"},
                "streamSettings": _stream(inb, host),
                "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"]},
            }
        elif proto == "trojan":
            clients = []
            for c in inb.get("clients", []):
                if c.get("active", True):
                    clients.append({"password": c["id"], "email": c.get("label", c["id"][:8])})
            if not clients:
                continue
            item = {
                "listen": "0.0.0.0", "port": port, "protocol": "trojan",
                "settings": {"clients": clients},
                "streamSettings": _stream(inb, host),
                "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"]},
            }
        else:
            # Native Shadowsocks is TCP/UDP. Do not fabricate a non-standard
            # WS/XHTTP SS server; the panel exposes the requested transport
            # selector for metadata but uses interoperable SS over TCP.
            clients = [c for c in inb.get("clients", []) if c.get("active", True)]
            if not clients:
                continue
            item = {
                "listen": "0.0.0.0", "port": port, "protocol": "shadowsocks",
                "settings": {
                    "method": inb.get("ss_method", "aes-128-gcm"),
                    "password": clients[0]["id"],
                    "network": "tcp,udp",
                },
            }
        xs.append(item)
    return {
        "log": {"loglevel": "warning"},
        "dns": {"queryStrategy": "UseIPv4"},
        "inbounds": xs,
        "outbounds": [
            {"protocol": "freedom", "tag": "direct", "settings": {"domainStrategy": "UseIPv4"}},
            {"protocol": "blackhole", "tag": "block"},
        ],
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": [
                {"type": "field", "protocol": ["bittorrent"], "outboundTag": "block"}
            ],
        },
    }

class XrayManager:
    def __init__(self):
        self.proc: subprocess.Popen | None = None
        self.lock = asyncio.Lock()

    def running(self) -> bool:
        return bool(self.proc and self.proc.poll() is None)

    async def apply(self, inbounds: list[dict], host: str) -> dict:
        async with self.lock:
            XRAY_DIR.mkdir(parents=True, exist_ok=True)
            cfg = build_config(inbounds, host)
            tmp = XRAY_CONFIG.with_suffix(".tmp")
            tmp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))
            tmp.replace(XRAY_CONFIG)
            binary = await asyncio.to_thread(ensure_xray)
            if self.running():
                self.proc.terminate()
                try:
                    await asyncio.wait_for(asyncio.to_thread(self.proc.wait), 5)
                except Exception:
                    self.proc.kill()
            logf = XRAY_LOG.open("ab")
            self.proc = subprocess.Popen(
                [str(binary), "run", "-config", str(XRAY_CONFIG)],
                stdout=logf, stderr=logf,
                start_new_session=True,
            )
            await asyncio.sleep(0.25)
            if self.proc.poll() is not None:
                raise RuntimeError(
                    f"Xray exited immediately; see {XRAY_LOG}"
                )
            return {"running": True, "pid": self.proc.pid, "inbounds": len(cfg["inbounds"])}

    async def stop(self):
        async with self.lock:
            if self.running():
                self.proc.terminate()
                try:
                    await asyncio.wait_for(asyncio.to_thread(self.proc.wait), 5)
                except Exception:
                    self.proc.kill()
            self.proc = None
