# LPRW v4.0 — Leviko Panel Railway

پنل پروکسی سبک برای Railway با پشتیبانی چندپروتکل و مدیریت اینباند.

## تغییرات نسخه ۴

- **رله بهینه‌شده**: بافر ۲ مگابایت، TCP_NODELAY + KEEPALIVE، پاسخ فوری VLESS برای کاهش پینگ
- **Shadowsocks (AEAD aes-256-gcm)** اضافه شد
- **مدیریت اینباند**: بخش جدا برای تعریف اینباند (پروتکل + شبکه + امنیت)
- **شبکه‌ها**: ws / httpupgrade / xhttp (لینک کلاینت مطابق؛ سرور روی مسیرهای بهینه‌شده WS)
- **API اینباند**: `/api/inbounds` (GET/POST/PATCH/DELETE)
- ساخت لینک با `inbound_id` به‌جای انتخاب مستقیم پروتکل

### پروتکل‌ها
| پروتکل | شبکه پشتیبانی‌شده در لینک | مسیر سرور |
|--------|---------------------------|-----------|
| VLESS  | ws, httpupgrade, xhttp    | /ws /hu /xhttp |
| Trojan | ws, httpupgrade, xhttp    | /trojan-ws /trojan-hu /trojan-xhttp |
| SS     | ws                        | /ss-ws |

> توجه: پیاده‌سازی pure-Python روی Railway برای xHTTP/HTTPUpgrade واقعی (فریمینگ Xray) کامل نیست؛ سرور ترافیک را روی مسیرهای WS بهینه‌شده می‌پذیرد و لینک کلاینت با type مربوطه ساخته می‌شود. برای سرعت حداکثری و Reality/xHTTP کامل، پنل‌های مبتنی بر Xray-core روی VPS مناسب‌ترند.

## دیپلوی

همان مراحل قبلی (GitHub → Railway + Volume روی `/data` + Generate Domain).

متغیرهای محیطی:
- `ADMIN_USER` / `ADMIN_PASSWORD`
- `RAILWAY_PUBLIC_DOMAIN` یا `PUBLIC_HOST`
- `PANEL_NAME`
- `DATA_DIR` (پیش‌فرض `/data`)

## API اینباند (جدید)

```
GET  /api/inbounds
POST /api/inbounds   { "name", "proto": "vless|trojan|ss", "network": "ws|xhttp|httpupgrade", "security": "tls|none", "path"? }
PATCH /api/inbounds/{id}
DELETE /api/inbounds/{id}
```

ساخت لینک:
```
POST /api/links  { "label", "inbound_id", "volume_gb", "days", "max_conn", "remark" }
```

## کلاینت‌ها
v2rayNG · Hiddify · NekoBox · Streisand · v2rayN

## مسئولیت
ابزار فنی است؛ رعایت قوانین بر عهده کاربر است.
