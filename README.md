# LPRW — Leviko Panel Railway

پنل مدیریت پروکسی چندپروتکلی اختصاصی برای Railway.

## امکانات

- کانفیگ **VLESS** و **Trojan** روی WebSocket + TLS
- محدودیت **حجم** و **زمان** برای هر لینک
- محدودیت تعداد اتصال همزمان
- **سابسکریپشن** گروهی با هدر userinfo
- صفحه مصرف عمومی کاربر (`/u/{id}`)
- QR Code برای هر کانفیگ
- داشبورد تاریک حرفه‌ای + نمودار ترافیک
- شمارش اتصالات آنلاین واقعی
- تنظیمات پنل و تغییر رمز
- ذخیره پایدار روی Volume

## دیپلوی Railway

1. این مخزن را روی GitHub آپلود کنید
2. Railway → New Project → Deploy from GitHub
3. Settings → Networking → **Generate Domain**
4. (پیشنهادی) Volume به مسیر `/data`
5. متغیر محیطی:
   - `ADMIN_PASSWORD` = رمز قوی (پیش‌فرض: `admin123`)

## آدرس‌ها

| مسیر | توضیح |
|------|--------|
| `/dashboard` | پنل مدیریت |
| `/sub/{id}` | لینک ساب |
| `/sub-link/{id}` | ساب تک‌لینک |
| `/u/{id}` | صفحه مصرف کاربر |
| `/qr/{id}` | تصویر QR |

## ساختار

```
LPRW/
├── main.py
├── pages.py
├── protocol/
│   ├── vless.py
│   └── trojan.py
├── requirements.txt
└── Procfile
```

## نکات

- بعد از Generate Domain یک بار Redeploy کنید تا `RAILWAY_PUBLIC_DOMAIN` اعمال شود
- رمز پیش‌فرض را حتماً عوض کنید
- ترافیک خروجی Railway هزینه دارد (~$0.05/GB)

---

LPRW v2.1 · Leviko Panel
