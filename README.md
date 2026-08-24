# LPRW v4.9.0

Panel for VLESS / Trojan / Shadowsocks over WebSocket.

## Outbound subscription controls

The panel includes an **Outbound** section for subscription composition:

- Remove the panel's primary generated config from subscriptions.
- Remove the usage/expiry status entry from subscriptions.
- Enable outbound configs and add any URI-based config, one per line.
- Outbound entries are appended to individual and group subscriptions.
- Duplicate outbound entries are removed automatically.

Outbound entries are stored as raw subscription URIs, so the panel does not restrict the protocol type.
