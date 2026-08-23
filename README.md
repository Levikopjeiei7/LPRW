# LPRW v4.0

پنل پروکسی Railway — VLESS / Trojan / Shadowsocks  
ترنسپورت: WS · HTTPUpgrade · XHTTP (path-based)

## تغییرات v4

- بخش **پروتکل و اینباند** (نام دلخواه، proto، network، security)
- لینک‌ها بر اساس اینباند ساخته می‌شوند
- Shadowsocks AEAD روی WS
- بهینه‌سازی رله (بافر، TCP_NODELAY، IPv4-first، پاسخ سریع VLESS)
- UI بازطراحی‌شده

## دیپلوی Railway

1. آپلود این فایل‌ها روی ریپو
2. Deploy from GitHub
3. Generate Domain
4. Volume روی `/data`
5. متغیرها: `ADMIN_USER` / `ADMIN_PASSWORD`

## مسیرها

| مسیر | کاربرد |
|------|--------|
| `/dashboard` | پنل |
| `/ws/{uuid}` | VLESS WS |
| `/trojan-ws/{uuid}` | Trojan WS |
| `/ss-ws/{uuid}` | Shadowsocks WS |
| `/xhttp/{proto}/{uuid}` | XHTTP path |
| `/hu/{proto}/{uuid}` | HTTPUpgrade path |
| `/sub/{uuid}` | ساب تکی |
| `/sub-group/{id}` | ساب گروهی |

## نکته سرعت

منطقه Railway را نزدیک کاربران بگذارید (اروپا برای ایران معمولاً بهتر است).  
بعد از Generate Domain یک‌بار Redeploy بزنید.
