"""LPRW v4 UI — dashboard + user portal."""

DASHBOARD = r'''<!DOCTYPE html>
<html lang="fa" dir="rtl" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#06080f">
<title>LPRW Panel</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{
  --bg:#06080f;--bg2:#0b0e18;--card:rgba(18,22,36,.92);--card2:#141825;
  --bd:rgba(255,255,255,.07);--bd2:rgba(255,255,255,.12);
  --tx:#eef1f8;--mu:#8b93a8;--mu2:#5c657a;
  --pr:#6366f1;--pr2:#818cf8;--ok:#34d399;--er:#f87171;--wn:#fbbf24;--cy:#22d3ee;
  --g:linear-gradient(135deg,#6366f1,#8b5cf6 50%,#d946ef);--r:16px;--side:260px;
  --shadow:0 20px 50px rgba(0,0,0,.45);
}
[data-theme="light"]{
  --bg:#f0f3fa;--bg2:#e6eaf5;--card:#fff;--card2:#f8fafc;
  --bd:rgba(15,23,42,.08);--bd2:rgba(15,23,42,.12);
  --tx:#0f172a;--mu:#64748b;--mu2:#94a3b8;--shadow:0 12px 36px rgba(15,23,42,.1);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Vazirmatn,system-ui,sans-serif;background:var(--bg);color:var(--tx);min-height:100vh;line-height:1.6}
body::before{content:"";position:fixed;width:500px;height:500px;top:-100px;right:-80px;background:radial-gradient(circle,rgba(99,102,241,.25),transparent 70%);filter:blur(80px);pointer-events:none;z-index:0}
button,input,select,textarea{font-family:inherit;font-size:.9rem;color:var(--tx)}
.hidden{display:none!important}
::-webkit-scrollbar{width:7px}::-webkit-scrollbar-thumb{background:rgba(129,140,248,.3);border-radius:99px}

#login{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;position:relative;z-index:2}
.login-card{width:100%;max-width:420px;background:var(--card);border:1px solid var(--bd2);border-radius:24px;padding:40px 32px;box-shadow:var(--shadow)}
.login-card h1{font-size:1.7rem;font-weight:800;margin-bottom:6px}
.login-card .sub{color:var(--mu);margin-bottom:24px;font-size:.9rem}
.field{margin-bottom:14px}
.field label{display:block;font-size:.78rem;color:var(--mu);margin-bottom:6px;font-weight:600}
.field input,.field select,.field textarea{width:100%;padding:12px 14px;border-radius:12px;border:1px solid var(--bd2);background:rgba(0,0,0,.22);outline:none}
[data-theme="light"] .field input,[data-theme="light"] .field select{background:#f8fafc}
.field input:focus,.field select:focus{border-color:var(--pr);box-shadow:0 0 0 3px rgba(99,102,241,.18)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:10px 16px;border-radius:12px;border:1px solid var(--bd2);cursor:pointer;font-weight:700;background:var(--card2);color:var(--tx);transition:.15s}
.btn:hover{filter:brightness(1.08)}
.btn-p{background:var(--g);color:#fff;border:none;box-shadow:0 8px 24px rgba(99,102,241,.3)}
.btn-block{width:100%;padding:13px}
.btn-sm{padding:7px 11px;font-size:.8rem;border-radius:10px}
.btn-d{background:rgba(248,113,113,.12);color:var(--er);border-color:rgba(248,113,113,.25)}
.err{display:none;margin-top:10px;padding:10px;border-radius:10px;background:rgba(248,113,113,.12);color:var(--er);font-size:.85rem}

#app{display:none;min-height:100vh;position:relative;z-index:1}
.shell{display:grid;grid-template-columns:var(--side) 1fr;min-height:100vh}
.side{background:linear-gradient(180deg,var(--card),var(--bg2));border-left:1px solid var(--bd);padding:18px 12px;display:flex;flex-direction:column;gap:4px}
.side .logo{display:flex;align-items:center;gap:10px;padding:8px 10px 16px;border-bottom:1px solid var(--bd);margin-bottom:10px}
.side .logo .mk{width:38px;height:38px;border-radius:11px;background:var(--g);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:.9rem;color:#fff}
.side .logo h2{font-size:1rem;font-weight:800}
.side .logo small{color:var(--mu);font-size:.7rem}
.nav-item{display:flex;align-items:center;gap:10px;padding:11px 12px;border-radius:11px;color:var(--mu);cursor:pointer;font-weight:600;font-size:.88rem;border:1px solid transparent}
.nav-item:hover{background:rgba(99,102,241,.08);color:var(--tx)}
.nav-item.active{background:rgba(99,102,241,.14);color:var(--pr2);border-color:rgba(99,102,241,.22)}
.brand-mark{width:44px;height:44px;border-radius:13px;display:grid;place-items:center;position:relative;background:linear-gradient(135deg,#6366f1,#8b5cf6);box-shadow:0 10px 28px rgba(99,102,241,.28);overflow:hidden;color:#fff;font-weight:900;font-size:1.15rem}
.brand-mark:before{content:"";position:absolute;inset:7px;border:1px solid rgba(255,255,255,.42);border-radius:9px;transform:rotate(45deg)}
.brand-mark span{position:relative;z-index:2;font-family:ui-sans-serif,system-ui}
.brand-mark i{position:absolute;width:18px;height:3px;background:rgba(255,255,255,.85);border-radius:99px;bottom:9px;right:7px;transform:rotate(-45deg)}
.switch-row{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:15px 0;border-bottom:1px solid var(--bd);cursor:pointer}
.switch-row:last-child{border-bottom:0}
.switch-row span{display:flex;flex-direction:column;gap:3px}.switch-row small{color:var(--mu);font-size:.76rem;font-weight:400}
.switch-row input{appearance:none;width:48px;height:26px;border-radius:99px;background:var(--mu2);position:relative;cursor:pointer;transition:.2s;flex:0 0 auto}
.switch-row input:before{content:"";position:absolute;width:20px;height:20px;border-radius:50%;background:#fff;top:3px;right:25px;transition:.2s;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.switch-row input:checked{background:var(--pr)}.switch-row input:checked:before{right:3px}
.actions-row{display:flex;gap:8px;flex-wrap:wrap}.outbound-preview{display:grid;gap:8px}.preview-row{display:flex;justify-content:space-between;gap:12px;padding:12px 14px;background:rgba(99,102,241,.06);border:1px solid var(--bd);border-radius:12px}.preview-row span{color:var(--mu)}
.chip-ok{color:var(--ok);border-color:rgba(52,211,153,.25);background:rgba(52,211,153,.08)}

.side-bottom{margin-top:auto;padding-top:14px;border-top:1px solid var(--bd);display:flex;flex-direction:column;gap:6px}
.main{padding:20px 24px 40px;max-width:1280px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:18px;flex-wrap:wrap}
.topbar h1{font-size:1.35rem;font-weight:800}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
@media(max-width:1000px){.kpis{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.kpis{grid-template-columns:1fr}}
.kpi{background:var(--card);border:1px solid var(--bd);border-radius:var(--r);padding:16px}
.kpi .t{font-size:.75rem;color:var(--mu);font-weight:600;margin-bottom:6px}
.kpi .v{font-size:1.4rem;font-weight:800}
.panel{background:var(--card);border:1px solid var(--bd);border-radius:var(--r);padding:18px;margin-bottom:14px}
.panel-h{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.panel-h h3{font-size:1rem;font-weight:800}
table{width:100%;border-collapse:collapse}
th,td{padding:11px 8px;text-align:right;border-bottom:1px solid var(--bd);font-size:.84rem}
th{color:var(--mu);font-weight:700;font-size:.73rem}
.badge{display:inline-block;padding:3px 9px;border-radius:99px;font-size:.72rem;font-weight:700}
.badge.on{background:rgba(52,211,153,.15);color:var(--ok)}
.badge.off{background:rgba(248,113,113,.15);color:var(--er)}
.chip{display:inline-flex;padding:4px 9px;border-radius:99px;font-size:.72rem;font-weight:700;background:rgba(99,102,241,.12);color:var(--pr2);border:1px solid rgba(99,102,241,.2);cursor:pointer}
.modal-bg{position:fixed;inset:0;background:rgba(0,0,0,.6);backdrop-filter:blur(5px);z-index:80;display:none;align-items:center;justify-content:center;padding:16px}
.modal-bg.show{display:flex}
.modal{background:var(--card);border:1px solid var(--bd2);border-radius:18px;padding:22px;width:100%;max-width:500px;box-shadow:var(--shadow);max-height:90vh;overflow:auto}
.modal h3{font-size:1.1rem;font-weight:800;margin-bottom:14px}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:560px){.form-row{grid-template-columns:1fr}}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(16px);background:var(--card2);border:1px solid var(--bd2);padding:11px 16px;border-radius:12px;z-index:99;opacity:0;transition:.25s;font-weight:600}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.empty{text-align:center;padding:32px 14px;color:var(--mu)}
.chart-box{position:relative;height:240px}
.bottom-nav{display:none;position:fixed;bottom:0;left:0;right:0;z-index:60;background:var(--card);border-top:1px solid var(--bd);padding:10px 6px calc(12px + env(safe-area-inset-bottom));justify-content:space-around;gap:4px;box-shadow:0 -8px 28px rgba(0,0,0,.35)}
.bottom-nav button{flex:1;border:none;background:transparent;color:var(--mu);font-family:inherit;font-size:.72rem;font-weight:700;padding:12px 4px;border-radius:14px;cursor:pointer;min-height:56px;line-height:1.25}
.bottom-nav button span{display:block;font-size:1.35rem;margin-bottom:4px}
.bottom-nav button.active{color:var(--pr2);background:rgba(99,102,241,.16)}
@media(max-width:900px){
  .shell{grid-template-columns:1fr}
  .side{display:none!important}
  .main{padding:14px 12px 110px}
  .bottom-nav{display:flex}
}
code{font-family:ui-monospace,monospace;font-size:.76rem;color:var(--pr2);word-break:break-all}
</style>
</head>
<body>
<div id="login">
  <div class="login-card">
    <div class="brand-mark" aria-label="LPRW"><span>L</span><i></i></div>
    <h1>ورود به پنل</h1>
    <p class="sub">LPRW · مدیریت پروکسی</p>
    <div class="field"><label>نام کاربری</label><input id="lu" value="admin" autocomplete="username"></div>
    <div class="field"><label>رمز عبور</label><input id="lp" type="password" autocomplete="current-password"></div>
    <button class="btn btn-p btn-block" onclick="doLogin()">ورود</button>
    <div class="err" id="login-err"></div>
  </div>
</div>

<div id="app">
<div class="shell">
  <aside class="side">
    <div class="logo"><div class="brand-mark" aria-label="LPRW"><span>L</span><i></i></div><div><h2 id="side-name">LPRW</h2><small id="side-ver">v4</small></div></div>
    <div class="nav-item active" data-page="home" onclick="go('home')">داشبورد</div>
    <div class="nav-item" data-page="links" onclick="go('links')">لینک‌ها</div>
    <div class="nav-item" data-page="inbounds" onclick="go('inbounds')">پروتکل و اینباند</div>
    <div class="nav-item" data-page="outbound" onclick="go('outbound')">اوتباند</div>
    <div class="nav-item" data-page="subs" onclick="go('subs')">سابسکریپشن</div>
    <div class="nav-item" data-page="online" onclick="go('online')">آنلاین</div>
    <div class="nav-item" data-page="settings" onclick="go('settings')">تنظیمات</div>
    <div class="side-bottom">
      <button class="btn btn-sm" onclick="toggleTheme()">تم</button>
      <button class="btn btn-sm btn-d" onclick="doLogout()">خروج</button>
    </div>
  </aside>
  <main class="main">
    <div class="topbar"><h1 id="page-title">داشبورد</h1><div class="acts" id="top-acts"></div></div>

    <section id="pg-home">
      <div class="kpis">
        <div class="kpi"><div class="t">ترافیک کل</div><div class="v" id="k-bytes">—</div></div>
        <div class="kpi"><div class="t">آنلاین</div><div class="v" id="k-online">0</div></div>
        <div class="kpi"><div class="t">لینک فعال</div><div class="v" id="k-links">0</div></div>
        <div class="kpi"><div class="t">آپتایم</div><div class="v" id="k-up">—</div></div>
      </div>
      <div class="panel"><div class="panel-h"><h3>ترافیک ساعتی</h3></div><div class="chart-box"><canvas id="chart"></canvas></div></div>
      <div class="panel"><div class="panel-h"><h3>فعالیت اخیر</h3></div><ul id="act-list" style="list-style:none"></ul></div>
    </section>

    <section id="pg-links" class="hidden">
      <div class="panel">
        <div class="panel-h"><h3>لینک‌ها</h3><button class="btn btn-p btn-sm" onclick="openLinkModal()">+ لینک جدید</button></div>
        <div style="overflow:auto"><table><thead><tr><th>نام</th><th>اینباند</th><th>مصرف</th><th>وضعیت</th><th>عملیات</th></tr></thead><tbody id="links-body"></tbody></table></div>
        <div class="empty hidden" id="links-empty">لینکی نیست — اول اینباند بسازید</div>
      </div>
    </section>

    <section id="pg-inbounds" class="hidden">
      <div class="panel">
        <div class="panel-h"><h3>پروتکل و اینباند</h3><button class="btn btn-p btn-sm" onclick="openIbModal()">+ اینباند جدید</button></div>
        <p style="color:var(--mu);font-size:.85rem;margin-bottom:12px">هر اینباند: پروتکل (vless/trojan/ss) + شبکه WebSocket + امنیت (tls/none)</p>
        <div style="overflow:auto"><table><thead><tr><th>نام</th><th>پروتکل</th><th>شبکه</th><th>امنیت</th><th>مسیر</th><th></th></tr></thead><tbody id="ib-body"></tbody></table></div>
      </div>
    </section>

    <section id="pg-outbound" class="hidden">
      <div class="panel">
        <div class="panel-h"><h3>اوتباند</h3><span class="chip" id="ob-state">غیرفعال</span></div>
        <p style="color:var(--mu);font-size:.84rem;margin-bottom:16px">مدیریت کانفیگ‌هایی که به سابسکریپشن اضافه می‌شوند و کنترل نمایش کانفیگ اصلی پنل.</p>
        <div class="outbound-settings">
          <label class="switch-row"><span><b>حذف کانفیگ اصلی پنل از ساب</b><small>وقتی فعال باشد، لینک اصلی VLESS/WS این پنل در ساب نمایش داده نمی‌شود.</small></span><input id="ob-remove-primary" type="checkbox"></label>
          <label class="switch-row"><span><b>حذف کانفیگ نمایش حجم و زمان</b><small>وقتی فعال باشد، خط وضعیت مصرف و زمان از ساب حذف می‌شود.</small></span><input id="ob-remove-status" type="checkbox"></label>
          <label class="switch-row"><span><b>فعال سازی کانفیگ اوتباند</b><small>کانفیگ‌های رایگان، VPS یا پنل‌های دیگر را به ساب اضافه می‌کند.</small></span><input id="ob-enabled" type="checkbox" onchange="toggleOutboundEditor()"></label>
        </div>
        <div id="ob-editor" class="hidden" style="margin-top:16px">
          <div class="field"><label>کانفیگ‌های اوتباند</label><textarea id="ob-configs" rows="10" placeholder="هر کانفیگ در یک خط
ss://...
vless://...
trojan://...
hysteria2://..."></textarea></div>
          <div class="actions-row"><button class="btn btn-p" onclick="saveOutbound()">ذخیره تنظیمات اوتباند</button><button class="btn" onclick="addOutboundSample()">افزودن نمونه</button></div>
          <p style="color:var(--mu);font-size:.75rem;margin-top:8px">هر URI معتبر را می‌توان وارد کرد. محدودیتی برای نوع پروتکل در پنل اعمال نمی‌شود.</p>
        </div>
      </div>
      <div class="panel">
        <div class="panel-h"><h3>وضعیت خروجی ساب</h3></div>
        <div id="ob-preview" class="outbound-preview"></div>
      </div>
    </section>

    <section id="pg-subs" class="hidden">
      <div class="panel">
        <div class="panel-h"><h3>سابسکریپشن گروهی</h3><button class="btn btn-p btn-sm" onclick="openSubModal()">+ ساب جدید</button></div>
        <p style="color:var(--mu);font-size:.84rem;margin-bottom:10px">لینک ساب همان پنل کاربری است — در مرورگر ظاهر دارد، در کلاینت کانفیگ می‌دهد.</p>
        <div style="overflow:auto"><table><thead><tr><th>نام</th><th>لینک‌ها</th><th>URL پنل/ساب</th><th></th></tr></thead><tbody id="subs-body"></tbody></table></div>
      </div>
    </section>

    <section id="pg-online" class="hidden">
      <div class="panel"><div class="panel-h"><h3>اتصالات زنده</h3></div><div id="online-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px"></div></div>
    </section>

    <section id="pg-settings" class="hidden">
      <div class="panel">
        <div class="panel-h"><h3>تنظیمات</h3></div>
        <div class="field"><label>نام پنل</label><input id="s-name"></div>
        <div class="field"><label>اعلان</label><input id="s-announce"></div>
        <div class="field"><label>لینک پشتیبانی</label><input id="s-support"></div>
        <button class="btn btn-p" onclick="saveSettings()">ذخیره</button>
      </div>
      <div class="panel">
        <div class="panel-h"><h3>تغییر رمز</h3></div>
        <div class="field"><label>رمز فعلی</label><input id="pw-cur" type="password"></div>
        <div class="field"><label>رمز جدید</label><input id="pw-new" type="password"></div>
        <button class="btn btn-p" onclick="chgPw()">تغییر رمز</button>
      </div>
    </section>
  </main>
</div>
<nav class="bottom-nav">
  <button class="active" data-page="home" onclick="go('home')">خانه</button>
  <button data-page="links" onclick="go('links')">لینک</button>
  <button data-page="inbounds" onclick="go('inbounds')">اینباند</button>
  <button data-page="outbound" onclick="go('outbound')">اوتباند</button>
  <button data-page="online" onclick="go('online')">آنلاین</button>
  <button data-page="settings" onclick="go('settings')">تنظیمات</button>
</nav>
</div>

<div class="modal-bg" id="m-link"><div class="modal">
  <h3 id="ml-title">لینک جدید</h3>
  <input type="hidden" id="ml-id" value="">
  <div class="field"><label>نام</label><input id="ml-label"></div>
  <div class="field"><label>اینباند</label><select id="ml-ib"></select></div>
  <div class="form-row">
    <div class="field"><label>حجم (GB) — 0=نامحدود</label><input id="ml-vol" type="number" min="0" value="0"></div>
    <div class="field"><label>روز — 0=نامحدود</label><input id="ml-days" type="number" min="0" value="0"></div>
  </div>
  <div class="field"><label>یادداشت</label><input id="ml-remark"></div>
  <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
    <button class="btn" onclick="closeModals()">انصراف</button>
    <button class="btn btn-p" id="ml-save" onclick="saveLink()">ذخیره</button>
  </div>
</div></div>

<div class="modal-bg" id="m-ib"><div class="modal">
  <h3>اینباند جدید</h3>
  <div class="field"><label>نام</label><input id="mi-name" placeholder="مثلاً VLESS-WS"></div>
  <div class="form-row">
    <div class="field"><label>پروتکل</label>
      <select id="mi-proto"><option value="vless">VLESS</option><option value="trojan">Trojan</option><option value="ss">Shadowsocks</option></select>
    </div>
    <div class="field"><label>شبکه</label>
      <select id="mi-net"><option value="ws">WebSocket</option></select>
    </div>
  </div>
  <div class="form-row">
    <div class="field"><label>امنیت</label>
      <select id="mi-sec"><option value="tls">TLS</option><option value="none">خالی (none)</option></select>
    </div>
    <div class="field"><label>مسیر (اختیاری)</label><input id="mi-path" placeholder="/ws"></div>
  </div>
  <div class="field" id="mi-ss-wrap"><label>متد SS</label>
    <select id="mi-ssm"><option value="aes-256-gcm">aes-256-gcm</option><option value="chacha20-ietf-poly1305">chacha20-ietf-poly1305</option></select>
  </div>
  <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
    <button class="btn" onclick="closeModals()">انصراف</button>
    <button class="btn btn-p" onclick="createIb()">ایجاد</button>
  </div>
</div></div>

<div class="modal-bg" id="m-sub"><div class="modal">
  <h3 id="ms-title">ساب گروهی</h3>
  <input type="hidden" id="ms-id" value="">
  <div class="field"><label>نام</label><input id="ms-name"></div>
  <div class="field"><label>لینک‌ها (چندتایی)</label><select id="ms-links" multiple style="min-height:120px"></select></div>
  <div class="form-row">
    <div class="field"><label>حجم GB (0=نامحدود)</label><input id="ms-vol" type="number" min="0" value="0"></div>
    <div class="field"><label>روز (0=نامحدود)</label><input id="ms-days" type="number" min="0" value="0"></div>
  </div>
  <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
    <button class="btn" onclick="closeModals()">انصراف</button>
    <button class="btn btn-p" id="ms-save" onclick="saveSub()">ذخیره</button>
  </div>
</div></div>

<div class="toast" id="toast"></div>
<script>
const $=s=>document.querySelector(s);
const $$=s=>document.querySelectorAll(s);
let chart, inbounds=[], links=[];

function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2200)}
function toggleTheme(){const h=document.documentElement;h.dataset.theme=h.dataset.theme==='dark'?'light':'dark';localStorage.setItem('lprw-theme',h.dataset.theme)}
(function(){const t=localStorage.getItem('lprw-theme');if(t)document.documentElement.dataset.theme=t})();

async function api(path,opts={}){
  const r=await fetch(path,{credentials:'include',...opts,headers:{'Content-Type':'application/json',...(opts.headers||{})}});
  if(r.status===401){showLogin();throw new Error('auth')}
  const j=await r.json().catch(()=>({}));
  if(!r.ok)throw new Error(j.detail||r.statusText);
  return j;
}

function showLogin(){$('#login').style.display='flex';$('#app').style.display='none'}
function showApp(){$('#login').style.display='none';$('#app').style.display='block'}

async function doLogin(){
  try{
    await api('/api/login',{method:'POST',body:JSON.stringify({username:$('#lu').value,password:$('#lp').value})});
    showApp();refresh();
  }catch(e){const er=$('#login-err');er.style.display='block';er.textContent='ورود ناموفق'}
}
async function doLogout(){await api('/api/logout',{method:'POST'});showLogin()}

function go(p){
  $$('[id^=pg-]').forEach(el=>el.classList.add('hidden'));
  const sec=$('#pg-'+p);if(sec)sec.classList.remove('hidden');
  $$('.nav-item,.bottom-nav button').forEach(el=>el.classList.toggle('active',el.dataset.page===p));
  const titles={home:'داشبورد',links:'لینک‌ها',inbounds:'پروتکل و اینباند',outbound:'اوتباند',subs:'سابسکریپشن',online:'آنلاین',settings:'تنظیمات'};
  $('#page-title').textContent=titles[p]||p;
  if(p==='links')loadLinks();
  if(p==='inbounds')loadInbounds();
  if(p==='outbound')loadOutbound();
  if(p==='subs')loadSubs();
  if(p==='online')loadStats();
  if(p==='settings')loadSettings();
}

function closeModals(){$$('.modal-bg').forEach(m=>m.classList.remove('show'))}

async function refresh(){
  try{
    const me=await api('/api/me');
    $('#side-name').textContent=me.name||'LPRW';
    $('#side-ver').textContent='v'+me.version;
    await loadStats();
    await loadInbounds();
  }catch(e){showLogin()}
}

async function loadStats(){
  const s=await api('/api/stats');
  $('#k-bytes').textContent=s.bytes_h;
  $('#k-online').textContent=s.online;
  $('#k-links').textContent=s.active_links+'/'+s.links;
  $('#k-up').textContent=s.uptime_h;
  const grid=$('#online-grid');
  grid.innerHTML=(s.connections||[]).map(c=>`<div class="kpi"><div class="t">${c.uuid}…</div><div class="v" style="font-size:1rem">${c.sec}s</div></div>`).join('')||'<div class="empty">اتصالی نیست</div>';
  const acts=await api('/api/activity');
  $('#act-list').innerHTML=acts.slice(0,20).map(a=>`<li style="padding:8px 0;border-bottom:1px solid var(--bd);font-size:.84rem"><span style="color:var(--mu2);font-size:.75rem;margin-left:8px">${(a.t||'').slice(11,19)}</span>${a.msg}</li>`).join('');
  const labels=Object.keys(s.hourly||{});
  const data=Object.values(s.hourly||{});
  if(chart)chart.destroy();
  chart=new Chart($('#chart'),{type:'line',data:{labels,datasets:[{label:'Bytes',data,borderColor:'#818cf8',backgroundColor:'rgba(99,102,241,.15)',fill:true,tension:.35}]},options:{plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#8b93a8'}},y:{ticks:{color:'#8b93a8'}}},responsive:true,maintainAspectRatio:false}});
}

async function loadInbounds(){
  inbounds=await api('/api/inbounds');
  $('#ib-body').innerHTML=inbounds.map(ib=>`<tr>
    <td>${ib.name}</td><td><span class="chip">${ib.proto}</span></td><td>${ib.network}</td><td>${ib.security}</td><td><code>${ib.path}</code></td>
    <td><button class="btn btn-sm btn-d" onclick="delIb('${ib.id}')">حذف</button></td>
  </tr>`).join('');
  const sel=$('#ml-ib');
  sel.innerHTML=inbounds.map(ib=>`<option value="${ib.id}">${ib.name} (${ib.proto}/${ib.network})</option>`).join('');
}

async function loadLinks(){
  links=await api('/api/links');
  window._links=links;
  const body=$('#links-body');
  const empty=$('#links-empty');
  if(!links.length){body.innerHTML='';empty.classList.remove('hidden');return}
  empty.classList.add('hidden');
  body.innerHTML=links.map(l=>`<tr>
    <td><b>${l.label}</b><br><code style="font-size:.7rem">${l.id.slice(0,8)}…</code></td>
    <td>${l.inbound_name||l.proto}<br><span class="chip">${l.network||'ws'}</span></td>
    <td>${l.used_h} / ${l.vol_h}</td>
    <td><span class="badge ${l.ok?'on':'off'}">${l.ok?'فعال':'غیرفعال'}</span> ${l.online?`🟢${l.online}`:''}</td>
    <td style="white-space:nowrap">
      <button class="btn btn-sm" onclick="editLink('${l.id}')">ویرایش</button>
      <button class="btn btn-sm" onclick="copyText((l.sub_configs||[]).join('\\n'))">کپی کانفیگ‌های ساب</button>
      <button class="btn btn-sm" onclick="copyText('${l.sub_url}')">ساب</button>
      <button class="btn btn-sm btn-d" onclick="delLink('${l.id}')">حذف</button>
    </td>
  </tr>`).join('');
}

async function loadSubs(){
  const subs=await api('/api/subs');
  window._subs=subs;
  $('#subs-body').innerHTML=subs.map(s=>`<tr>
    <td><b>${s.name}</b></td><td>${(s.link_ids||[]).length}</td>
    <td><code style="font-size:.7rem">${s.url}</code><br>
      <button class="btn btn-sm" onclick="copyText('${s.url}')">کپی پنل/ساب</button>
    </td>
    <td style="white-space:nowrap">
      <button class="btn btn-sm" onclick="editSub('${s.id}')">ویرایش</button>
      <button class="btn btn-sm btn-d" onclick="delSub('${s.id}')">حذف</button>
    </td>
  </tr>`).join('')||'<tr><td colspan="4" class="empty">سابی نیست</td></tr>';
}

async function loadOutbound(){
  const o=await api('/api/outbound');
  $('#ob-enabled').checked=!!o.enabled;
  $('#ob-remove-primary').checked=!!o.remove_primary;
  $('#ob-remove-status').checked=!!o.remove_status;
  $('#ob-configs').value=(o.configs||[]).join('\n');
  toggleOutboundEditor();
  renderOutboundPreview(o);
}

function toggleOutboundEditor(){
  $('#ob-editor').classList.toggle('hidden', !$('#ob-enabled').checked);
  renderOutboundPreview({enabled:$('#ob-enabled').checked,remove_primary:$('#ob-remove-primary').checked,remove_status:$('#ob-remove-status').checked,configs:$('#ob-configs').value.split('\n').map(x=>x.trim()).filter(Boolean)});
}

function renderOutboundPreview(o){
  const state=$('#ob-state');
  state.textContent=o.enabled?'فعال':'غیرفعال';
  state.className='chip '+(o.enabled?'chip-ok':'');
  const rows=[];
  rows.push(`<div class="preview-row"><span>کانفیگ اصلی پنل</span><b>${o.remove_primary?'حذف از ساب':'نمایش در ساب'}</b></div>`);
  rows.push(`<div class="preview-row"><span>حجم و زمان</span><b>${o.remove_status?'حذف از ساب':'نمایش در ساب'}</b></div>`);
  rows.push(`<div class="preview-row"><span>کانفیگ‌های اوتباند</span><b>${o.enabled?((o.configs||[]).length+' مورد'):'غیرفعال'}</b></div>`);
  $('#ob-preview').innerHTML=rows.join('');
}

async function saveOutbound(){
  const configs=$('#ob-configs').value.split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
  await api('/api/outbound',{method:'POST',body:JSON.stringify({enabled:$('#ob-enabled').checked,remove_primary:$('#ob-remove-primary').checked,remove_status:$('#ob-remove-status').checked,configs})});
  toast('تنظیمات اوتباند ذخیره شد');
  await loadOutbound();
}

function addOutboundSample(){
  const sample='vless://UUID@host:443?encryption=none&security=tls&type=ws&host=host&path=%2Fws&sni=host#Outbound';
  const box=$('#ob-configs');
  box.value=box.value.trim()?box.value.trim()+'\n'+sample:sample;
}

async function loadSettings(){
  const s=await api('/api/settings');
  $('#s-name').value=s.panel_name||'';
  $('#s-announce').value=s.announce||'';
  $('#s-support').value=s.support_url||'';
}

function openLinkModal(){
  $('#ml-id').value='';
  $('#ml-title').textContent='لینک جدید';
  $('#ml-label').value='';
  $('#ml-vol').value='0';
  $('#ml-days').value='0';
  $('#ml-remark').value='';
  loadInbounds();
  $('#m-link').classList.add('show');
}
async function editLink(id){
  const l=(window._links||[]).find(x=>x.id===id);
  if(!l){toast('لینک پیدا نشد');return}
  await loadInbounds();
  $('#ml-id').value=id;
  $('#ml-title').textContent='ویرایش لینک';
  $('#ml-label').value=l.label||'';
  $('#ml-ib').value=l.inbound_id||'';
  $('#ml-vol').value=l.vol? (l.vol/1024/1024/1024).toFixed(2):0;
  $('#ml-days').value=0;
  $('#ml-remark').value=l.remark||'';
  $('#m-link').classList.add('show');
}
function openIbModal(){$('#m-ib').classList.add('show')}
async function openSubModal(){
  $('#ms-id').value='';
  $('#ms-title').textContent='ساب گروهی جدید';
  $('#ms-name').value='';
  $('#ms-vol').value='0';
  $('#ms-days').value='0';
  links=await api('/api/links');
  $('#ms-links').innerHTML=links.map(l=>`<option value="${l.id}">${l.label}</option>`).join('');
  $('#m-sub').classList.add('show');
}

async function editSub(id){
  const s=(window._subs||[]).find(x=>x.id===id);
  if(!s)return;
  $('#ms-id').value=id;
  $('#ms-title').textContent='ویرایش ساب';
  $('#ms-name').value=s.name||'';
  $('#ms-vol').value=s.vol? (s.vol/1024/1024/1024).toFixed(2):0;
  $('#ms-days').value=0;
  links=await api('/api/links');
  const selected=new Set(s.link_ids||[]);
  $('#ms-links').innerHTML=links.map(l=>`<option value="${l.id}" ${selected.has(l.id)?'selected':''}>${l.label}</option>`).join('');
  $('#m-sub').classList.add('show');
}

async function saveSub(){
  const id=$('#ms-id').value;
  const ids=[...$('#ms-links').selectedOptions].map(o=>o.value);
  const body={name:$('#ms-name').value,link_ids:ids,volume_gb:parseFloat($('#ms-vol').value)||0,days:parseInt($('#ms-days').value)||0};
  if(id){
    await api('/api/subs/'+id,{method:'PATCH',body:JSON.stringify(body)});
    toast('ساب ویرایش شد');
  }else{
    await api('/api/subs',{method:'POST',body:JSON.stringify(body)});
    toast('ساب ساخته شد');
  }
  closeModals();loadSubs();
}

async function saveLink(){
  const id=$('#ml-id').value;
  const body={
    label:$('#ml-label').value,inbound_id:$('#ml-ib').value,
    volume_gb:parseFloat($('#ml-vol').value)||0,days:parseInt($('#ml-days').value)||0,
    remark:$('#ml-remark').value
  };
  if(id){
    await api('/api/links/'+id,{method:'PATCH',body:JSON.stringify(body)});
    toast('لینک ویرایش شد');
  }else{
    await api('/api/links',{method:'POST',body:JSON.stringify(body)});
    toast('لینک ساخته شد');
  }
  closeModals();loadLinks();
}
async function createIb(){
  await api('/api/inbounds',{method:'POST',body:JSON.stringify({
    name:$('#mi-name').value,proto:$('#mi-proto').value,network:$('#mi-net').value,
    security:$('#mi-sec').value,path:$('#mi-path').value,ss_method:$('#mi-ssm').value
  })});
  closeModals();toast('اینباند ساخته شد');loadInbounds();
}
async function delLink(id){if(!confirm('حذف؟'))return;await api('/api/links/'+id,{method:'DELETE'});loadLinks()}
async function delIb(id){if(!confirm('حذف اینباند؟'))return;await api('/api/inbounds/'+id,{method:'DELETE'});loadInbounds()}
async function delSub(id){if(!confirm('حذف؟'))return;await api('/api/subs/'+id,{method:'DELETE'});loadSubs()}
async function saveSettings(){
  await api('/api/settings',{method:'POST',body:JSON.stringify({panel_name:$('#s-name').value,announce:$('#s-announce').value,support_url:$('#s-support').value})});
  toast('ذخیره شد');
}
async function chgPw(){
  await api('/api/password',{method:'POST',body:JSON.stringify({current:$('#pw-cur').value,new_password:$('#pw-new').value})});
  toast('رمز تغییر کرد');
}
function copyText(t){navigator.clipboard.writeText(t);toast('کپی شد')}

(async()=>{
  try{await api('/api/me');showApp();refresh();setInterval(loadStats,15000)}catch(e){showLogin()}
})();
$('#lp').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin()});
</script>
</body>
</html>
'''

USER_PORTAL = r'''<!DOCTYPE html>
<html lang="fa" dir="rtl" data-theme="dark">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{LABEL}} · LPRW</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{--bg:#06080f;--card:rgba(16,19,32,.92);--bd:rgba(255,255,255,.08);--tx:#f1f3f9;--mu:#8b93a8;--pr:#818cf8;--ok:#34d399;--er:#f87171;--g:linear-gradient(135deg,#6366f1,#a855f7 50%,#ec4899);--shadow:0 30px 80px rgba(0,0,0,.55)}
[data-theme="light"]{--bg:#f3f5fb;--card:#fff;--bd:rgba(15,23,42,.1);--tx:#0f172a;--mu:#64748b;--shadow:0 20px 50px rgba(15,23,42,.1)}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:Vazirmatn,system-ui,sans-serif;background:var(--bg);color:var(--tx);min-height:100vh;line-height:1.7}
body::before{content:"";position:fixed;width:520px;height:520px;top:-100px;right:-80px;background:radial-gradient(circle,rgba(99,102,241,.28),transparent 70%);filter:blur(40px);pointer-events:none}
.wrap{max-width:920px;margin:0 auto;padding:28px 18px 60px;position:relative;z-index:1}
.top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:22px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:12px}.brand .mk{width:48px;height:48px;border-radius:14px;background:var(--g);display:grid;place-items:center;font-weight:900;color:#fff}
.brand h1{font-size:1.25rem;font-weight:800}.brand small{color:var(--mu);font-size:.78rem}
.theme{border:1px solid var(--bd);background:var(--card);color:var(--tx);padding:10px 14px;border-radius:12px;cursor:pointer;font-weight:700}
.hero{background:var(--card);border:1px solid var(--bd);border-radius:24px;padding:28px;box-shadow:var(--shadow);margin-bottom:18px}
.hero .name{font-size:1.5rem;font-weight:900;margin-bottom:8px}
.badge{display:inline-flex;padding:5px 12px;border-radius:99px;font-size:.78rem;font-weight:700}
.badge.ok{background:rgba(52,211,153,.15);color:var(--ok)}.badge.bad{background:rgba(248,113,113,.15);color:var(--er)}
.bar{height:14px;background:rgba(128,128,128,.15);border-radius:99px;overflow:hidden;margin:18px 0 10px}.bar>i{display:block;height:100%;width:{{PCT}}%;background:var(--g);border-radius:99px}
.meta{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}@media(max-width:640px){.meta{grid-template-columns:1fr}}
.meta .b{background:rgba(99,102,241,.08);border:1px solid var(--bd);border-radius:16px;padding:14px}.meta .t{font-size:.75rem;color:var(--mu);font-weight:600}.meta .v{font-size:1.05rem;font-weight:800;margin-top:4px}
.grid{display:grid;grid-template-columns:1.2fr .8fr;gap:16px}@media(max-width:800px){.grid{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--bd);border-radius:20px;padding:22px;margin-bottom:16px;box-shadow:var(--shadow)}.card h3{font-size:1.05rem;font-weight:800;margin-bottom:14px}
.share-box{background:rgba(0,0,0,.2);border:1px solid var(--bd);border-radius:14px;padding:12px;font-size:.78rem;word-break:break-all;font-family:ui-monospace,monospace;direction:ltr;text-align:left;max-height:90px;overflow:auto}
[data-theme="light"] .share-box{background:#f8fafc}
.actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.btn{border:1px solid var(--bd);background:rgba(99,102,241,.12);color:var(--pr);padding:10px 14px;border-radius:12px;cursor:pointer;font-weight:700;font-size:.85rem}
.btn-p{background:var(--g);color:#fff;border:none}
.qr{width:100%;max-width:200px;border-radius:16px;border:1px solid var(--bd);background:#fff;padding:8px;margin:0 auto;display:block}
.cli-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
.cli{display:block;background:rgba(99,102,241,.08);border:1px solid var(--bd);border-radius:14px;padding:14px;text-decoration:none;color:var(--tx)}.cli:hover{border-color:rgba(99,102,241,.45)}
.cli-n{font-weight:800;font-size:.9rem}.cli-p{color:var(--mu);font-size:.72rem;margin:4px 0}.cli-a{color:var(--pr);font-size:.78rem;font-weight:700}
.help-card{background:rgba(0,0,0,.15);border:1px solid var(--bd);border-radius:14px;padding:14px;margin-bottom:10px}[data-theme="light"] .help-card{background:#f8fafc}
.help-card h4{font-size:.92rem;margin-bottom:8px}.help-card pre{white-space:pre-wrap;font-family:inherit;font-size:.82rem;color:var(--mu);line-height:1.8}
.steps{display:grid;gap:10px}.steps .s{display:flex;gap:12px;align-items:flex-start;padding:12px;border-radius:14px;background:rgba(99,102,241,.07);border:1px solid var(--bd)}
.steps .n{width:28px;height:28px;border-radius:50%;background:var(--g);color:#fff;display:grid;place-items:center;font-weight:800;font-size:.8rem;flex-shrink:0}
.foot{text-align:center;color:var(--mu);font-size:.75rem;margin-top:28px}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:var(--card);border:1px solid var(--bd);padding:12px 18px;border-radius:12px;box-shadow:var(--shadow);opacity:0;transition:.25s;z-index:9;font-weight:700}.toast.show{opacity:1}
</style></head><body>
<div class="wrap">
<div class="top"><div class="brand"><img class="mk" src="https://avatars.githubusercontent.com/u/316735646?v=4" alt="LPRW" width="48" height="48"><div><h1>LPRW User</h1><small>پنل مصرف اختصاصی</small></div></div>
<button class="theme" id="theme" type="button">☀ / ☾ حالت روز و شب</button></div>
<div class="hero"><div class="name">{{LABEL}}</div><span class="badge {{STATUS_CLASS}}">{{STATUS}}</span>
<div class="bar"><i></i></div>
<div style="display:flex;justify-content:space-between;font-size:.85rem;color:var(--mu);flex-wrap:wrap;gap:8px">
<span>مصرف: <strong style="color:var(--tx)">{{USED}}</strong></span>
<span>سقف: <strong style="color:var(--tx)">{{VOL}}</strong></span>
<span>{{PCT}}٪</span></div>
<div class="meta">
<div class="b"><div class="t">پروتکل</div><div class="v">{{PROTO}}</div></div>
<div class="b"><div class="t">انقضا</div><div class="v">{{EXP}}</div></div>
<div class="b"><div class="t">آنلاین الان</div><div class="v">{{ONLINE}}</div></div>
</div></div>
<div class="grid"><div>
<div class="card"><h3>کانفیگ‌های ساب</h3>
<div class="share-box" id="share">{{SUB_CONFIGS}}</div>
<div class="actions"><button class="btn btn-p" id="copy">کپی تمام کانفیگ‌ها</button>
<button class="btn" id="copy-sub">کپی لینک ساب</button>
<a class="btn" href="{{SUB}}" target="_blank">باز کردن ساب</a></div>
<p style="margin-top:12px;font-size:.8rem;color:var(--mu)">لینک اشتراک: <code style="color:var(--pr)">{{SUB}}</code></p></div>
<div class="card"><h3>دانلود کلاینت</h3><div class="cli-grid">
<a class="cli" href="https://github.com/2dust/v2rayNG/releases" target="_blank" rel="noopener"><div class="cli-n">v2rayNG</div><div class="cli-p">Android</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://github.com/2dust/v2rayN/releases" target="_blank" rel="noopener"><div class="cli-n">v2rayN</div><div class="cli-p">Windows</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://github.com/hiddify/hiddify-app/releases" target="_blank" rel="noopener"><div class="cli-n">Hiddify</div><div class="cli-p">All</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://apps.apple.com/app/streisand/id6450534064" target="_blank" rel="noopener"><div class="cli-n">Streisand</div><div class="cli-p">iOS</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://apps.apple.com/app/v2box-v2ray-client/id6446814690" target="_blank" rel="noopener"><div class="cli-n">V2Box</div><div class="cli-p">iOS</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://github.com/MatsuriDayo/NekoBoxForAndroid/releases" target="_blank" rel="noopener"><div class="cli-n">NekoBox</div><div class="cli-p">Android</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://github.com/MetaCubeX/ClashMetaForAndroid/releases" target="_blank" rel="noopener"><div class="cli-n">Clash Meta</div><div class="cli-p">Desktop</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://apps.apple.com/app/foxray/id6448898396" target="_blank" rel="noopener"><div class="cli-n">FoXray</div><div class="cli-p">iOS</div><div class="cli-a">دانلود</div></a>
</div></div>
<div class="card"><h3>راهنمای اتصال</h3>
<div class="steps">
<div class="s"><div class="n">1</div><div>یکی از کلاینت‌های بالا را نصب کنید.</div></div>
<div class="s"><div class="n">2</div><div>دکمه «کپی کانفیگ» را بزنید یا از QR استفاده کنید.</div></div>
<div class="s"><div class="n">3</div><div>در کلاینت: Import from clipboard / افزودن از کلیپ‌بورد.</div></div>
<div class="s"><div class="n">4</div><div>برای چند دستگاه از لینک سابسکریپشن استفاده کنید.</div></div>
</div></div>
<div class="card"><h3>آموزش کلاینت‌ها</h3>
<div class="help-card"><h4>v2rayNG (اندروید)</h4><pre>1. اپ را نصب کنید\n2. روی + بزنید\n3. ورود از کلیپ‌بورد\n4. کانفیگ را وارد کنید\n5. اتصال را روشن کنید</pre></div>
<div class="help-card"><h4>v2rayN (ویندوز)</h4><pre>1. برنامه را اجرا کنید\n2. Import from clipboard\n3. Set as active server\n4. System proxy = Automatic</pre></div>
<div class="help-card"><h4>Streisand / V2Box (آیفون)</h4><pre>1. نصب از App Store\n2. Paste لینک یا ساب\n3. افزودن پروفایل و اتصال</pre></div>
<div class="help-card"><h4>Hiddify</h4><pre>1. نصب\n2. افزودن از کلیپ‌بورد یا QR\n3. اتصال</pre></div>
<div class="help-card"><h4>NekoBox</h4><pre>1. نصب\n2. New profile from clipboard\n3. Connect</pre></div>
<div class="help-card"><h4>سایر کلاینت‌ها</h4><pre>لینک Subscription را در Add Subscription وارد و Update کنید.</pre></div>
</div></div>
<div>
<div class="card" style="text-align:center"><h3>QR Code</h3>
<img class="qr" src="{{QR}}" alt="QR">
<p style="margin-top:10px;font-size:.78rem;color:var(--mu)">اسکن با کلاینت موبایل</p></div>
<div class="card"><h3>جزئیات</h3>
<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bd)"><span style="color:var(--mu)">هاست</span><strong>{{HOST}}</strong></div>
<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bd)"><span style="color:var(--mu)">نسخه</span><strong>{{VERSION}}</strong></div>
<div style="display:flex;justify-content:space-between;padding:8px 0"><span style="color:var(--mu)">یادداشت</span><strong>{{REMARK}}</strong></div>
</div>
<div class="card"><h3>نکات سرعت</h3>
<ul style="padding-right:18px;color:var(--mu);font-size:.85rem">
<li>کلاینت را به‌روز نگه دارید.</li>
<li>از اینترنت پایدار تست کنید.</li>
<li>اگر پینگ بالا بود زمان دیگری امتحان کنید.</li>
<li>روی هر دستگاه فقط یک پروفایل فعال کافی است.</li>
</ul></div>
</div></div>
<div class="foot">LPRW · Leviko Panel Railway · پنل کاربری</div>
</div>
<div class="toast" id="toast"></div>
<script>
const toast=m=>{const t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2200)};
const apply=t=>{document.documentElement.setAttribute('data-theme',t);localStorage.setItem('lprw_user_theme',t)};
apply(localStorage.getItem('lprw_user_theme')||'dark');
document.getElementById('theme').onclick=()=>{const n=document.documentElement.getAttribute('data-theme')==='light'?'dark':'light';apply(n);toast(n==='dark'?'حالت شب':'حالت روز')};
document.getElementById('copy').onclick=()=>navigator.clipboard.writeText(document.getElementById('share').textContent.trim()).then(()=>toast('تمام کانفیگ‌ها کپی شد'));
document.getElementById('copy-sub').onclick=()=>navigator.clipboard.writeText('{{SUB}}').then(()=>toast('لینک ساب کپی شد'));
</script></body></html>
'''
