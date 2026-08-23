"""
HTTPUpgrade transport handler.

Xray HTTPUpgrade: HTTP/1.1 Upgrade: websocket, then **raw** byte stream
(no WebSocket frames). On Railway the edge typically terminates TLS and
forwards either as WebSocket (framed) or as HTTP.

We register:
  1) WebSocket endpoint /hu/{uid} — works when edge reframes
  2) HTTP GET that responds 101 and relies on WebSocket stack (uvicorn)

Plus a raw-style path that accepts POST body as first packet for debugging.
True unframed HTTPUpgrade end-to-end needs a custom ASGI server; on Railway
the practical path that matches Xray clients through the edge is WebSocket
accept after Upgrade, which uvicorn already does for @app.websocket routes.
"""
from __future__ import annotations

# Handlers live in main via existing handle_vless_ws / handle_trojan_ws on /hu/{uid}.
# This module only documents path constants used by share().

HU_PATH_PREFIX = "/hu"
