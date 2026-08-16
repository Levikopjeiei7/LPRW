"""
LPRW Shadowsocks-WS (AEAD chacha20-ietf-poly1305 / aes-256-gcm).
Path auth: /ss-ws/{uuid}  — password = link id (uuid)
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import socket
import struct

from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from fastapi import WebSocket, WebSocketDisconnect

from protocol.vless import RELAY_BUF, WRITE_HIGH_WATER, QuotaGate, open_tcp, tune_socket

logger = logging.getLogger("LPRW.ss")

METHODS = {
    "chacha20-ietf-poly1305": (32, 32, ChaCha20Poly1305),
    "aes-256-gcm": (32, 32, AESGCM),
    "aes-128-gcm": (16, 16, AESGCM),
}
DEFAULT_METHOD = "chacha20-ietf-poly1305"
TAG = 16


def evp_bytes_to_key(password: bytes, key_len: int) -> bytes:
    m = []
    block = b""
    while len(b"".join(m)) < key_len:
        block = hashlib.md5(block + password).digest()
        m.append(block)
    return b"".join(m)[:key_len]


def hkdf_sha1(key: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    # minimal HKDF-Extract+Expand with SHA1 (Shadowsocks AEAD)
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF

    return HKDF(
        algorithm=hashes.SHA1(),
        length=length,
        salt=salt,
        info=info,
    ).derive(key)


class AeadCrypto:
    def __init__(self, method: str, password: str, is_enc: bool, salt: bytes | None = None):
        key_len, salt_len, cls = METHODS[method]
        master = evp_bytes_to_key(password.encode("utf-8"), key_len)
        if is_enc:
            self.salt = salt or __import__("os").urandom(salt_len)
        else:
            if salt is None or len(salt) != salt_len:
                raise ValueError("bad salt")
            self.salt = salt
        subkey = hkdf_sha1(master, self.salt, b"ss-subkey", key_len)
        self.aead = cls(subkey)
        self.nonce_counter = 0
        self.salt_len = salt_len

    def _nonce(self) -> bytes:
        n = self.nonce_counter
        self.nonce_counter += 1
        return n.to_bytes(12, "little")

    def seal(self, plaintext: bytes) -> bytes:
        return self.aead.encrypt(self._nonce(), plaintext, None)

    def open(self, data: bytes) -> bytes:
        return self.aead.decrypt(self._nonce(), data, None)


def parse_ss_addr(buf: bytes):
    """SOCKS5-like address at start of decrypted payload."""
    if not buf:
        raise ValueError("empty")
    atyp = buf[0]
    pos = 1
    if atyp == 0x01:
        address = socket.inet_ntop(socket.AF_INET, buf[pos : pos + 4])
        pos += 4
    elif atyp == 0x03:
        n = buf[pos]
        pos += 1
        address = buf[pos : pos + n].decode("utf-8", "ignore")
        pos += n
    elif atyp == 0x04:
        address = socket.inet_ntop(socket.AF_INET6, buf[pos : pos + 16])
        pos += 16
    else:
        raise ValueError(f"atyp {atyp}")
    port = int.from_bytes(buf[pos : pos + 2], "big")
    pos += 2
    return address, port, buf[pos:]


class ChunkReader:
    """Buffer WS frames and decrypt SS AEAD length-chunk stream."""

    def __init__(self, dec: AeadCrypto):
        self.dec = dec
        self.buf = b""
        self.need_len = True
        self.next_len = 2 + TAG

    def feed(self, data: bytes) -> list[bytes]:
        self.buf += data
        out = []
        while True:
            if len(self.buf) < self.next_len:
                break
            chunk = self.buf[: self.next_len]
            self.buf = self.buf[self.next_len :]
            try:
                plain = self.dec.open(chunk)
            except Exception as e:
                raise ValueError(f"decrypt fail: {e}") from e
            if self.need_len:
                if len(plain) != 2:
                    raise ValueError("bad len chunk")
                ln = struct.unpack("!H", plain)[0]
                if ln > 0x3FFF:
                    raise ValueError("len too big")
                self.next_len = ln + TAG
                self.need_len = False
            else:
                out.append(plain)
                self.next_len = 2 + TAG
                self.need_len = True
        return out


def pack_chunks(enc: AeadCrypto, data: bytes) -> bytes:
    out = bytearray()
    # max payload per chunk 0x3FFF
    off = 0
    while off < len(data):
        part = data[off : off + 0x3FFF]
        off += len(part)
        out += enc.seal(struct.pack("!H", len(part)))
        out += enc.seal(part)
    return bytes(out)


async def handle_ss_ws(ws, uid, is_allowed, on_usage, register_conn, unregister_conn):
    await ws.accept()
    link = is_allowed(uid)
    if not link:
        await ws.close(code=1008, reason="not authorized")
        return

    method = link.get("ss_method") or DEFAULT_METHOD
    if method not in METHODS:
        method = DEFAULT_METHOD
    password = uid  # password == link id

    conn_id = register_conn(uid)
    writer = None
    try:
        key_len, salt_len, _ = METHODS[method]
        buf = b""
        # need salt first
        while len(buf) < salt_len:
            msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
            if msg["type"] == "websocket.disconnect":
                return
            buf += msg.get("bytes") or (msg.get("text") or "").encode()

        salt = buf[:salt_len]
        buf = buf[salt_len:]
        dec = AeadCrypto(method, password, is_enc=False, salt=salt)
        enc = AeadCrypto(method, password, is_enc=True)
        reader_ss = ChunkReader(dec)

        gate = QuotaGate(uid, on_usage)
        await gate.add(salt_len)

        # decrypt until we have address header
        payload_rest = b""
        addr = port = None
        if buf:
            pieces = reader_ss.feed(buf)
            collected = b"".join(pieces)
            if collected:
                try:
                    addr, port, payload_rest = parse_ss_addr(collected)
                except ValueError:
                    payload_rest = collected

        while addr is None:
            msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
            if msg["type"] == "websocket.disconnect":
                return
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            await gate.add(len(data))
            pieces = reader_ss.feed(data)
            if not pieces:
                continue
            collected = (payload_rest + b"".join(pieces)) if payload_rest else b"".join(pieces)
            payload_rest = b""
            try:
                addr, port, payload_rest = parse_ss_addr(collected)
            except ValueError:
                payload_rest = collected
                if len(payload_rest) > 4096:
                    raise

        tcp_r, writer = await open_tcp(addr, port, timeout=10.0)
        tune_socket(writer)
        # first response must include our salt
        first_hdr = enc.salt
        if payload_rest:
            writer.write(payload_rest)
            await writer.drain()

        async def up():
            nonlocal first_hdr
            try:
                while True:
                    msg = await ws.receive()
                    if msg["type"] == "websocket.disconnect":
                        break
                    data = msg.get("bytes") or (msg.get("text") or "").encode()
                    if not data:
                        continue
                    if not await gate.add(len(data)):
                        break
                    for plain in reader_ss.feed(data):
                        writer.write(plain)
                    if writer.transport.get_write_buffer_size() > WRITE_HIGH_WATER:
                        await writer.drain()
            except Exception:
                pass
            finally:
                await gate.flush()
                try:
                    writer.write_eof()
                except Exception:
                    pass

        async def down():
            try:
                # send salt once at start of downlink
                await ws.send_bytes(first_hdr)
                while True:
                    data = await tcp_r.read(RELAY_BUF)
                    if not data:
                        break
                    if not await gate.add(len(data)):
                        break
                    packed = pack_chunks(enc, data)
                    await ws.send_bytes(packed)
            except Exception:
                pass
            finally:
                await gate.flush()

        done, pending = await asyncio.wait(
            {asyncio.create_task(up()), asyncio.create_task(down())},
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass
    except (WebSocketDisconnect, asyncio.TimeoutError):
        pass
    except Exception as e:
        logger.debug("ss: %s", e)
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        unregister_conn(conn_id)
