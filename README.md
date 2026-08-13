# LPRW — Leviko Panel Railway v3

پنل اختصاصی چندپروتکلی برای Railway.

## اصلاح مهم v3

کانفیگ‌ها مثل معماری استاندارد گیت‌وی‌های async روی Railway ساخته می‌شوند:

- **VLESS**: مسیر WebSocket = `/ws/{uuid}`
- **Trojan**: مسیر WebSocket = `/trojan-ws/{uuid}`
- رله TCP واقعی با بافر بزرگ + TCP_NODELAY
- پاسخ VLESS با پیشوند `\x00\x00` روی اولین پکت

## دیپلوی

1. آپلود روی GitHub  
2. Railway → Deploy from GitHub  
3. **Generate Domain** سپس یک‌بار **Redeploy**  
4. Volume → `/data`  
5. `ADMIN_PASSWORD` را عوض کنید  

داشبورد: `https://DOMAIN/dashboard`  
پیش‌فرض رمز: `admin123`

## آدرس‌ها

| مسیر | کاربرد |
|------|--------|
| `/dashboard` | پنل |
| `/ws/{uuid}` | تونل VLESS |
| `/trojan-ws/{uuid}` | تونل Trojan |
| `/sub/{uuid}` | ساب تک (base64) |
| `/sub-group/{id}` | ساب گروهی |
| `/u/{uuid}` | صفحه مصرف |
| `/qr/{uuid}` | QR |

## کلاینت

v2rayNG / Hiddify / Streisand — کانفیگ را از دکمه «کانفیگ» کپی کنید.

---
LPRW v3.0 · Leviko Panel
