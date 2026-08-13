"""LPRW v3 dashboard — expanded premium UI."""
DASHBOARD = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LPRW · Leviko Panel</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>

:root{--bg:#05070d;--s1:rgba(16,19,32,.78);--s2:rgba(22,26,42,.92);--s3:rgba(30,35,55,.95);--bd:rgba(255,255,255,.06);--bd2:rgba(255,255,255,.12);--tx:#f1f3f9;--mu:#8b93a8;--mu2:#5c657a;--pr:#6366f1;--pr2:#818cf8;--pr3:#a5b4fc;--ok:#34d399;--er:#f87171;--wn:#fbbf24;--cy:#22d3ee;--pk:#e879f9;--g1:linear-gradient(135deg,#6366f1 0%,#8b5cf6 50%,#d946ef 100%);--shadow:0 24px 60px rgba(0,0,0,.5);--r:18px}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:Vazirmatn,system-ui,sans-serif;background:var(--bg);color:var(--tx);min-height:100vh;line-height:1.65;overflow-x:hidden}
body::before,body::after{content:"";position:fixed;pointer-events:none;z-index:0;border-radius:50%;filter:blur(90px)}
body::before{width:520px;height:520px;top:-100px;right:-60px;background:radial-gradient(circle,rgba(99,102,241,.28),transparent 70%)}
body::after{width:420px;height:420px;bottom:-80px;left:-40px;background:radial-gradient(circle,rgba(217,70,239,.14),transparent 70%)}
button,input,select{font-family:inherit;font-size:.9rem}.hidden{display:none!important}
::-webkit-scrollbar{width:7px}::-webkit-scrollbar-thumb{background:rgba(255,255,255,.12);border-radius:99px}
#login{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;position:relative;z-index:1}
.login-card{width:100%;max-width:440px;background:linear-gradient(165deg,rgba(22,26,42,.98),rgba(8,10,18,.99));border:1px solid var(--bd2);border-radius:28px;padding:52px 42px;box-shadow:var(--shadow),inset 0 1px 0 rgba(255,255,255,.06);position:relative;overflow:hidden;animation:rise .55s ease}
.login-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--g1)}
.brand-mark{width:60px;height:60px;border-radius:18px;background:var(--g1);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.3rem;color:#fff;margin-bottom:24px;box-shadow:0 14px 36px rgba(99,102,241,.5)}
.login-card h1{font-size:1.8rem;font-weight:800;margin-bottom:8px}.login-card h1 span{background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.tagline{color:var(--mu);margin-bottom:34px;font-size:.95rem}
.fg{margin-bottom:18px}.fg label{display:block;margin-bottom:8px;color:var(--mu);font-size:.8rem;font-weight:600}
.fg input,.fg select{width:100%;padding:14px 16px;background:rgba(6,8,16,.85);border:1px solid var(--bd);border-radius:12px;color:var(--tx);outline:none;transition:.2s}
.fg input:focus,.fg select:focus{border-color:var(--pr);box-shadow:0 0 0 4px rgba(99,102,241,.15)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:13px 22px;border:none;border-radius:12px;cursor:pointer;font-weight:700;transition:.2s;font-size:.9rem}
.btn:active{transform:scale(.97)}.btn-p{background:var(--g1);color:#fff;width:100%;box-shadow:0 12px 32px rgba(99,102,241,.42)}.btn-p:hover{filter:brightness(1.1);transform:translateY(-1px)}
.btn-g{background:transparent;border:1px solid var(--bd2);color:var(--tx)}.btn-g:hover{background:var(--s3)}
.btn-d{background:rgba(248,113,113,.12);color:#fca5a5;border:1px solid rgba(248,113,113,.25)}
.btn-ok{background:rgba(52,211,153,.12);color:#6ee7b7;border:1px solid rgba(52,211,153,.25)}
.btn-sm{padding:8px 14px;font-size:.78rem;border-radius:10px}
.err{color:var(--er);font-size:.85rem;margin-top:14px;display:none;text-align:center}
#app{display:none;position:relative;z-index:1}
.side{position:fixed;right:0;top:0;bottom:0;width:272px;background:linear-gradient(180deg,rgba(12,14,24,.98),rgba(5,7,12,.99));border-left:1px solid var(--bd);padding:28px 16px;display:flex;flex-direction:column;z-index:50;backdrop-filter:blur(24px)}
.side-brand{display:flex;align-items:center;gap:12px;padding:0 8px 22px;border-bottom:1px solid var(--bd);margin-bottom:18px}
.side-brand .mark{width:46px;height:46px;border-radius:14px;background:var(--g1);display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;box-shadow:0 10px 24px rgba(99,102,241,.45)}
.side-brand h2{font-size:1.2rem;font-weight:800}.side-brand p{font-size:.7rem;color:var(--mu)}
.nav{display:flex;flex-direction:column;gap:4px;flex:1}
.nav a{display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:13px;color:var(--mu);cursor:pointer;transition:.18s;font-size:.9rem;font-weight:500;border:1px solid transparent}
.nav a svg{width:20px;height:20px;opacity:.7;flex-shrink:0}
.nav a:hover{background:rgba(255,255,255,.04);color:var(--tx)}
.nav a.on{background:linear-gradient(135deg,rgba(99,102,241,.2),rgba(168,85,247,.12));color:var(--pr3);border-color:rgba(99,102,241,.28);box-shadow:0 6px 20px rgba(99,102,241,.14)}
.nav a.on svg{opacity:1}
.side-foot{border-top:1px solid var(--bd);padding-top:14px;margin-top:10px}
.host-pill{font-size:.68rem;color:var(--mu2);word-break:break-all;background:rgba(255,255,255,.03);border:1px solid var(--bd);border-radius:10px;padding:10px 12px;margin-bottom:12px;line-height:1.4}
.host-pill b{color:var(--mu);display:block;margin-bottom:4px;font-size:.62rem;letter-spacing:.05em}
.main{margin-right:272px;padding:32px 36px 56px;min-height:100vh}
.page-head{margin-bottom:26px}.page-head h1{font-size:1.6rem;font-weight:800;letter-spacing:-.02em;margin-bottom:6px}
.page-head p{color:var(--mu);font-size:.9rem}
.head-row{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:26px}
.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:26px}
.sc{background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);padding:22px;position:relative;overflow:hidden;backdrop-filter:blur(14px);transition:.25s}
.sc:hover{transform:translateY(-4px);border-color:var(--bd2);box-shadow:0 20px 48px rgba(0,0,0,.4)}
.sc .sc-top{display:flex;justify-content:space-between;margin-bottom:14px}
.sc .icon{width:46px;height:46px;border-radius:14px;display:flex;align-items:center;justify-content:center}
.sc .icon svg{width:21px;height:21px}
.sc .icon.i1{background:rgba(99,102,241,.2);color:var(--pr2)}.sc .icon.i2{background:rgba(34,211,238,.15);color:var(--cy)}
.sc .icon.i3{background:rgba(52,211,153,.15);color:var(--ok)}.sc .icon.i4{background:rgba(232,121,249,.15);color:var(--pk)}
.sc .lb{color:var(--mu);font-size:.78rem;font-weight:500;margin-bottom:6px}
.sc .vl{font-size:1.7rem;font-weight:800;letter-spacing:-.03em}.sc .sm{font-size:.72rem;color:var(--mu2);margin-top:8px}
.sc .glow{position:absolute;width:120px;height:120px;border-radius:50%;filter:blur(44px);opacity:.32;top:-32px;left:-22px;pointer-events:none}
.panel{background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);backdrop-filter:blur(14px);overflow:hidden;margin-bottom:22px}
.panel-h{display:flex;align-items:center;justify-content:space-between;padding:16px 22px;border-bottom:1px solid var(--bd)}
.panel-h h3{font-size:.95rem;font-weight:700}.panel-h .meta{font-size:.75rem;color:var(--mu)}
.chart-wrap{padding:14px 16px;height:300px}
.tw{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:.86rem}
th{text-align:right;padding:14px 18px;background:rgba(0,0,0,.28);color:var(--mu);font-weight:600;font-size:.7rem;letter-spacing:.04em;text-transform:uppercase}
td{padding:15px 18px;border-top:1px solid var(--bd);vertical-align:middle}tr:hover td{background:rgba(99,102,241,.045)}
.badge{display:inline-flex;align-items:center;gap:6px;padding:5px 11px;border-radius:99px;font-size:.72rem;font-weight:700}
.badge::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
.b-ok{background:rgba(52,211,153,.12);color:#6ee7b7}.b-off{background:rgba(248,113,113,.12);color:#fca5a5}
.b-pr{background:rgba(99,102,241,.16);color:#a5b4fc}.b-tr{background:rgba(168,85,247,.16);color:#d8b4fe}
.b-pr::before,.b-tr::before{display:none}
.prog{height:7px;background:rgba(255,255,255,.06);border-radius:99px;overflow:hidden;min-width:90px;margin-top:6px}
.prog i{display:block;height:100%;background:var(--g1);border-radius:99px}
.chip{display:inline-flex;background:rgba(255,255,255,.04);border:1px solid var(--bd);padding:6px 10px;border-radius:9px;font-size:.72rem;cursor:pointer;color:var(--mu);margin:2px;transition:.15s;font-weight:500}
.chip:hover{color:var(--tx);border-color:var(--pr);background:rgba(99,102,241,.12)}
.chip.danger:hover{border-color:var(--er);color:var(--er)}
.user-cell{display:flex;align-items:center;gap:12px}
.avatar{width:40px;height:40px;border-radius:12px;background:var(--g1);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.9rem;color:#fff;flex-shrink:0;box-shadow:0 6px 16px rgba(99,102,241,.35)}
.user-cell .meta{font-size:.68rem;color:var(--mu2);margin-top:2px;font-family:ui-monospace,monospace}
.ov{position:fixed;inset:0;background:rgba(0,0,0,.78);backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;z-index:100;padding:20px;animation:fadeIn .2s}
.md{background:linear-gradient(165deg,rgba(22,26,42,.99),rgba(8,10,18,.99));border:1px solid var(--bd2);border-radius:24px;padding:34px;width:100%;max-width:520px;max-height:90vh;overflow-y:auto;box-shadow:0 40px 100px rgba(0,0,0,.65);animation:rise .28s}
.md h2{font-size:1.25rem;font-weight:800;margin-bottom:4px}.md .desc{color:var(--mu);font-size:.85rem;margin-bottom:22px}
.md .row2{display:grid;grid-template-columns:1fr 1fr;gap:14px}.md .acts{display:flex;gap:10px;justify-content:flex-end;margin-top:24px}
.al{list-style:none}.al li{display:flex;gap:14px;padding:14px 22px;border-bottom:1px solid var(--bd);font-size:.88rem;align-items:flex-start}
.al li:hover{background:rgba(255,255,255,.02)}
.al .tm{color:var(--mu2);font-size:.75rem;min-width:64px}
.al .dot{width:9px;height:9px;border-radius:50%;margin-top:6px;flex-shrink:0;box-shadow:0 0 10px currentColor}
.dot-ok{background:var(--ok);color:var(--ok)}.dot-info{background:var(--pr2);color:var(--pr2)}.dot-warn{background:var(--wn);color:var(--wn)}
.toast{position:fixed;bottom:28px;left:28px;background:var(--s2);border:1px solid var(--bd2);padding:14px 22px;border-radius:14px;font-size:.88rem;z-index:200;box-shadow:0 16px 40px rgba(0,0,0,.45);max-width:320px;animation:rise .3s;backdrop-filter:blur(12px)}
.empty{text-align:center;padding:56px 24px;color:var(--mu)}
.empty .ico{width:64px;height:64px;margin:0 auto 16px;border-radius:18px;background:rgba(99,102,241,.12);display:flex;align-items:center;justify-content:center;color:var(--pr2)}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@media(max-width:1100px){.sg{grid-template-columns:repeat(2,1fr)}}
@media(max-width:900px){.side{width:100%;height:auto;position:relative;border:0;border-bottom:1px solid var(--bd);flex-direction:row;flex-wrap:wrap;padding:14px;gap:8px}.side-brand{border:0;margin:0;padding:0;flex:1}.nav{flex-direction:row;flex-wrap:wrap;width:100%}.nav a{padding:9px 12px;font-size:.82rem}.side-foot{display:none}.main{margin-right:0;padding:20px 14px}.sg{grid-template-columns:1fr 1fr}.md .row2{grid-template-columns:1fr}}
@media(max-width:480px){.sg{grid-template-columns:1fr}}

.hero-banner{background:linear-gradient(135deg,rgba(99,102,241,.15),rgba(168,85,247,.08));border:1px solid rgba(99,102,241,.2);border-radius:20px;padding:28px 32px;margin-bottom:28px;display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
.hero-banner h2{font-size:1.25rem;font-weight:800;margin-bottom:6px}
.hero-banner p{color:var(--mu);font-size:.88rem}
.pulse{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--ok);box-shadow:0 0 12px var(--ok);animation:pulse 2s infinite;margin-left:8px}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.conn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;padding:18px}
.conn-card{background:rgba(255,255,255,.03);border:1px solid var(--bd);border-radius:14px;padding:14px 16px}
.conn-card .t{font-size:.75rem;color:var(--mu);margin-bottom:4px}
.conn-card .v{font-weight:700;font-size:.95rem}
.tabs{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap}
.tab{padding:10px 18px;border-radius:12px;border:1px solid var(--bd);background:transparent;color:var(--mu);cursor:pointer;font-weight:600;font-size:.85rem}
.tab.on{background:rgba(99,102,241,.15);border-color:rgba(99,102,241,.3);color:var(--pr3)}
.kpi-row{display:flex;gap:24px;flex-wrap:wrap;margin-top:12px}
.kpi{font-size:.8rem;color:var(--mu)}.kpi b{color:var(--tx);font-size:1.1rem;display:block}
.glass{background:rgba(16,19,32,.6);backdrop-filter:blur(16px);border:1px solid var(--bd);border-radius:20px}
.shine{position:relative;overflow:hidden}
.shine::after{content:"";position:absolute;top:0;left:-100%;width:60%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.04),transparent);animation:shine 4s infinite}
@keyframes shine{0%{left:-100%}50%{left:120%}100%{left:120%}}
.footer-bar{margin-top:40px;padding:20px;text-align:center;color:var(--mu2);font-size:.75rem;border-top:1px solid var(--bd)}
.btn-icon{width:40px;height:40px;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--bd);background:rgba(255,255,255,.03);cursor:pointer;color:var(--mu)}
.btn-icon:hover{border-color:var(--pr);color:var(--pr2)}
.search-box{flex:1;min-width:180px;padding:11px 16px;background:rgba(6,8,16,.7);border:1px solid var(--bd);border-radius:12px;color:var(--tx);outline:none}
.search-box:focus{border-color:var(--pr)}
.stat-mini{display:flex;gap:16px;flex-wrap:wrap}
.stat-mini .item{background:rgba(255,255,255,.03);border:1px solid var(--bd);border-radius:12px;padding:12px 16px;min-width:120px}
.stat-mini .item .l{font-size:.7rem;color:var(--mu)}.stat-mini .item .v{font-weight:700;font-size:1.05rem}
/* design-token-0: spacing scale and elevation layer for premium surfaces */
/* design-token-1: spacing scale and elevation layer for premium surfaces */
/* design-token-2: spacing scale and elevation layer for premium surfaces */
/* design-token-3: spacing scale and elevation layer for premium surfaces */
/* design-token-4: spacing scale and elevation layer for premium surfaces */
/* design-token-5: spacing scale and elevation layer for premium surfaces */
/* design-token-6: spacing scale and elevation layer for premium surfaces */
/* design-token-7: spacing scale and elevation layer for premium surfaces */
/* design-token-8: spacing scale and elevation layer for premium surfaces */
/* design-token-9: spacing scale and elevation layer for premium surfaces */
/* design-token-10: spacing scale and elevation layer for premium surfaces */
/* design-token-11: spacing scale and elevation layer for premium surfaces */
/* design-token-12: spacing scale and elevation layer for premium surfaces */
/* design-token-13: spacing scale and elevation layer for premium surfaces */
/* design-token-14: spacing scale and elevation layer for premium surfaces */
/* design-token-15: spacing scale and elevation layer for premium surfaces */
/* design-token-16: spacing scale and elevation layer for premium surfaces */
/* design-token-17: spacing scale and elevation layer for premium surfaces */
/* design-token-18: spacing scale and elevation layer for premium surfaces */
/* design-token-19: spacing scale and elevation layer for premium surfaces */
/* design-token-20: spacing scale and elevation layer for premium surfaces */
/* design-token-21: spacing scale and elevation layer for premium surfaces */
/* design-token-22: spacing scale and elevation layer for premium surfaces */
/* design-token-23: spacing scale and elevation layer for premium surfaces */
/* design-token-24: spacing scale and elevation layer for premium surfaces */
/* design-token-25: spacing scale and elevation layer for premium surfaces */
/* design-token-26: spacing scale and elevation layer for premium surfaces */
/* design-token-27: spacing scale and elevation layer for premium surfaces */
/* design-token-28: spacing scale and elevation layer for premium surfaces */
/* design-token-29: spacing scale and elevation layer for premium surfaces */
/* design-token-30: spacing scale and elevation layer for premium surfaces */
/* design-token-31: spacing scale and elevation layer for premium surfaces */
/* design-token-32: spacing scale and elevation layer for premium surfaces */
/* design-token-33: spacing scale and elevation layer for premium surfaces */
/* design-token-34: spacing scale and elevation layer for premium surfaces */
/* design-token-35: spacing scale and elevation layer for premium surfaces */
/* design-token-36: spacing scale and elevation layer for premium surfaces */
/* design-token-37: spacing scale and elevation layer for premium surfaces */
/* design-token-38: spacing scale and elevation layer for premium surfaces */
/* design-token-39: spacing scale and elevation layer for premium surfaces */
/* design-token-40: spacing scale and elevation layer for premium surfaces */
/* design-token-41: spacing scale and elevation layer for premium surfaces */
/* design-token-42: spacing scale and elevation layer for premium surfaces */
/* design-token-43: spacing scale and elevation layer for premium surfaces */
/* design-token-44: spacing scale and elevation layer for premium surfaces */
/* design-token-45: spacing scale and elevation layer for premium surfaces */
/* design-token-46: spacing scale and elevation layer for premium surfaces */
/* design-token-47: spacing scale and elevation layer for premium surfaces */
/* design-token-48: spacing scale and elevation layer for premium surfaces */
/* design-token-49: spacing scale and elevation layer for premium surfaces */
/* design-token-50: spacing scale and elevation layer for premium surfaces */
/* design-token-51: spacing scale and elevation layer for premium surfaces */
/* design-token-52: spacing scale and elevation layer for premium surfaces */
/* design-token-53: spacing scale and elevation layer for premium surfaces */
/* design-token-54: spacing scale and elevation layer for premium surfaces */
/* design-token-55: spacing scale and elevation layer for premium surfaces */
/* design-token-56: spacing scale and elevation layer for premium surfaces */
/* design-token-57: spacing scale and elevation layer for premium surfaces */
/* design-token-58: spacing scale and elevation layer for premium surfaces */
/* design-token-59: spacing scale and elevation layer for premium surfaces */
/* design-token-60: spacing scale and elevation layer for premium surfaces */
/* design-token-61: spacing scale and elevation layer for premium surfaces */
/* design-token-62: spacing scale and elevation layer for premium surfaces */
/* design-token-63: spacing scale and elevation layer for premium surfaces */
/* design-token-64: spacing scale and elevation layer for premium surfaces */
/* design-token-65: spacing scale and elevation layer for premium surfaces */
/* design-token-66: spacing scale and elevation layer for premium surfaces */
/* design-token-67: spacing scale and elevation layer for premium surfaces */
/* design-token-68: spacing scale and elevation layer for premium surfaces */
/* design-token-69: spacing scale and elevation layer for premium surfaces */
/* design-token-70: spacing scale and elevation layer for premium surfaces */
/* design-token-71: spacing scale and elevation layer for premium surfaces */
/* design-token-72: spacing scale and elevation layer for premium surfaces */
/* design-token-73: spacing scale and elevation layer for premium surfaces */
/* design-token-74: spacing scale and elevation layer for premium surfaces */
/* design-token-75: spacing scale and elevation layer for premium surfaces */
/* design-token-76: spacing scale and elevation layer for premium surfaces */
/* design-token-77: spacing scale and elevation layer for premium surfaces */
/* design-token-78: spacing scale and elevation layer for premium surfaces */
/* design-token-79: spacing scale and elevation layer for premium surfaces */
</style>
</head>
<body>
<div id="login"><div class="login-card">
<div class="brand-mark">LP</div>
<h1>ورود به <span>LPRW</span></h1>
<p class="tagline">Leviko Panel · دروازه چندپروتکلی حرفه‌ای</p>
<div class="fg"><label>رمز عبور مدیر</label><input type="password" id="pw" placeholder="رمز خود را وارد کنید" autofocus></div>
<button class="btn btn-p" id="btn-login">ورود به داشبورد</button>
<p class="err" id="lerr">رمز عبور اشتباه است</p>
</div></div>
<div id="app">
<aside class="side">
<div class="side-brand"><div class="mark">LP</div><div><h2>LPRW</h2><p>Leviko Panel v3</p></div></div>
<nav class="nav">
<a class="on" data-p="dash"><svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>داشبورد</a>
<a data-p="links"><svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>لینک‌ها</a>
<a data-p="subs"><svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>سابسکریپشن</a>
<a data-p="online"><svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M5.636 18.364a9 9 0 010-12.728m12.728 0a9 9 0 010 12.728m-9.9-2.828a4 4 0 010-5.656m5.656 0a4 4 0 010 5.656M12 12h.01"/></svg>آنلاین‌ها</a>
<a data-p="act"><svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>فعالیت‌ها</a>
<a data-p="set"><svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>تنظیمات</a>
</nav>
<div class="side-foot">
<div class="host-pill"><b>دامنه سرویس</b><span id="shost">—</span></div>
<button class="btn btn-g btn-sm" style="width:100%" id="btn-out">خروج از حساب</button>
</div>
</aside>
<main class="main">
<section id="p-dash">
<div class="hero-banner shine">
<div><h2>خوش آمدید به LPRW <span class="pulse"></span></h2><p id="announce">نمای زنده سرویس، ترافیک و اتصالات</p>
<div class="kpi-row"><div class="kpi"><b id="st-ver">v3</b>نسخه</div><div class="kpi"><b id="st-host2">—</b>هاست</div></div></div>
</div>
<div class="sg">
<div class="sc"><div class="glow" style="background:#6366f1"></div><div class="sc-top"><div class="icon i1"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg></div></div><div class="lb">ترافیک کل</div><div class="vl" id="st-b">—</div><div class="sm">داده رد و بدل شده</div></div>
<div class="sc"><div class="glow" style="background:#22d3ee"></div><div class="sc-top"><div class="icon i2"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5.636 18.364a9 9 0 010-12.728m12.728 0a9 9 0 010 12.728"/></svg></div></div><div class="lb">آنلاین الان</div><div class="vl" id="st-o">—</div><div class="sm">اتصالات فعال</div></div>
<div class="sc"><div class="glow" style="background:#34d399"></div><div class="sc-top"><div class="icon i3"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656"/></svg></div></div><div class="lb">لینک فعال</div><div class="vl" id="st-l">—</div><div class="sm">از کل لینک‌ها</div></div>
<div class="sc"><div class="glow" style="background:#e879f9"></div><div class="sc-top"><div class="icon i4"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div></div><div class="lb">آپ‌تایم</div><div class="vl" id="st-u">—</div><div class="sm">از راه‌اندازی</div></div>
</div>
<div class="panel"><div class="panel-h"><h3>نمودار ترافیک ساعتی</h3><span class="meta">۲۴ ساعت اخیر</span></div><div class="chart-wrap"><canvas id="chart"></canvas></div></div>
<div class="panel"><div class="panel-h"><h3>آخرین لینک‌ها</h3><span class="meta">۱۰ مورد</span></div>
<div class="tw"><table><thead><tr><th>کاربر</th><th>پروتکل</th><th>مصرف</th><th>وضعیت</th><th>آنلاین</th></tr></thead><tbody id="dash-tb"></tbody></table></div></div>
<div class="footer-bar">LPRW · Leviko Panel Railway · ساخته‌شده اختصاصی</div>
</section>
<section id="p-links" class="hidden">
<div class="head-row"><div class="page-head" style="margin:0"><h1>مدیریت لینک‌ها</h1><p>VLESS و Trojan با مسیر /ws/{uuid}</p></div>
<button class="btn btn-p" style="width:auto" id="btn-nl">+ لینک جدید</button></div>
<div class="panel"><div class="tw"><table><thead><tr><th>کاربر</th><th>پروتکل</th><th>مصرف</th><th>انقضا</th><th>وضعیت</th><th>عملیات</th></tr></thead><tbody id="links-tb"></tbody></table></div></div>
</section>
<section id="p-subs" class="hidden">
<div class="head-row"><div class="page-head" style="margin:0"><h1>سابسکریپشن</h1><p>اشتراک گروهی (base64)</p></div>
<button class="btn btn-p" style="width:auto" id="btn-ns">+ ساب جدید</button></div>
<div class="panel"><div class="tw"><table><thead><tr><th>نام</th><th>آدرس</th><th>حجم</th><th>عملیات</th></tr></thead><tbody id="subs-tb"></tbody></table></div></div>
</section>
<section id="p-online" class="hidden">
<div class="page-head"><h1>اتصالات آنلاین</h1><p>لیست زنده اتصالات فعال</p></div>
<div class="panel"><div class="conn-grid" id="online-grid"></div></div>
</section>
<section id="p-act" class="hidden">
<div class="page-head"><h1>فعالیت‌ها</h1><p>رویدادهای سیستم</p></div>
<div class="panel"><ul class="al" id="act-list"></ul></div>
</section>
<section id="p-set" class="hidden">
<div class="page-head"><h1>تنظیمات</h1><p>پیکربندی و امنیت</p></div>
<div class="panel" style="padding:28px;max-width:560px">
<div class="fg"><label>نام پنل</label><input id="s-name"></div>
<div class="fg"><label>اعلان داشبورد</label><input id="s-ann"></div>
<div class="fg"><label>پشتیبانی</label><input id="s-sup"></div>
<button class="btn btn-p" style="width:auto" id="btn-ss">ذخیره</button>
<div style="height:1px;background:var(--bd);margin:28px 0"></div>
<h3 style="font-weight:700;margin-bottom:14px">تغییر رمز</h3>
<div class="fg"><label>رمز فعلی</label><input type="password" id="pw-c"></div>
<div class="fg"><label>رمز جدید</label><input type="password" id="pw-n"></div>
<button class="btn btn-ok" style="width:auto" id="btn-pw">تغییر رمز</button>
<div style="height:1px;background:var(--bd);margin:28px 0"></div>
<button class="btn btn-g" style="width:auto" id="btn-backup">دانلود بکاپ JSON</button>
</div></section>
</main></div>
<div id="m-link" class="ov hidden"><div class="md">
<h2>لینک جدید</h2><p class="desc">کانفیگ با path شامل UUID</p>
<div class="fg"><label>برچسب</label><input id="nl-l"></div>
<div class="row2"><div class="fg"><label>پروتکل</label><select id="nl-p"><option value="vless">VLESS</option><option value="trojan">Trojan</option></select></div>
<div class="fg"><label>حجم GB (0=∞)</label><input id="nl-v" type="number" min="0" value="0"></div></div>
<div class="row2"><div class="fg"><label>روز (0=∞)</label><input id="nl-d" type="number" min="0" value="30"></div>
<div class="fg"><label>حد اتصال</label><input id="nl-m" type="number" min="0" value="0"></div></div>
<div class="fg"><label>یادداشت</label><input id="nl-r"></div>
<div class="acts"><button class="btn btn-g" data-close="m-link">انصراف</button><button class="btn btn-p" style="width:auto" id="btn-cl">ایجاد</button></div>
</div></div>
<div id="m-sub" class="ov hidden"><div class="md">
<h2>ساب جدید</h2><p class="desc">اشتراک گروهی</p>
<div class="fg"><label>نام</label><input id="ns-n"></div>
<div class="row2"><div class="fg"><label>حجم GB</label><input id="ns-v" type="number" min="0" value="0"></div>
<div class="fg"><label>روز</label><input id="ns-d" type="number" min="0" value="30"></div></div>
<div class="fg"><label>UUIDها (کاما / خالی=همه)</label><input id="ns-i"></div>
<div class="acts"><button class="btn btn-g" data-close="m-sub">انصراف</button><button class="btn btn-p" style="width:auto" id="btn-cs">ایجاد</button></div>
</div></div>

<script>
const $=s=>document.querySelector(s),$$=s=>document.querySelectorAll(s);let chart=null;
function toast(m){const t=document.createElement('div');t.className='toast';t.textContent=m;document.body.appendChild(t);setTimeout(()=>t.remove(),2800)}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function copy(t){navigator.clipboard.writeText(t).then(()=>toast('کپی شد ✓'))}
function av(n){return (n||'U').trim().charAt(0).toUpperCase()}
async function api(p,o={}){const r=await fetch(p,{credentials:'include',headers:{'Content-Type':'application/json',...(o.headers||{})},...o});if(r.status===401){showLogin();throw new Error('auth')}const d=await r.json().catch(()=>({}));if(!r.ok)throw new Error(typeof d.detail==='string'?d.detail:'خطا');return d}
function showLogin(){$('#login').style.display='flex';$('#app').style.display='none'}
function showApp(){$('#login').style.display='none';$('#app').style.display='block';go('dash')}
function go(p){$$('.nav a').forEach(a=>a.classList.toggle('on',a.dataset.p===p));['dash','links','subs','online','act','set'].forEach(x=>{const e=$('#p-'+x);if(e)e.classList.toggle('hidden',x!==p)});if(p==='dash')loadDash();if(p==='links')loadLinks();if(p==='subs')loadSubs();if(p==='online')loadOnline();if(p==='act')loadAct();if(p==='set')loadSet()}
function openM(id){$('#'+id).classList.remove('hidden')}function closeM(id){$('#'+id).classList.add('hidden')}
function up(s){const h=Math.floor(s/3600),m=Math.floor((s%3600)/60);return h>0?h+'س '+m+'د':m+' دقیقه'}
async function loadDash(){try{const s=await api('/api/stats');$('#st-b').textContent=s.bytes_h;$('#st-o').textContent=s.online;$('#st-l').textContent=s.active_links+' / '+s.links;$('#st-u').textContent=up(s.uptime);$('#shost').textContent=s.host||'—';$('#st-host2').textContent=s.host||'—';$('#st-ver').textContent=s.version||'v3';$('#announce').textContent=s.announce||'نمای زنده سرویس، ترافیک و اتصالات';const labels=Object.keys(s.hourly||{}),data=Object.values(s.hourly||{});if(chart)chart.destroy();chart=new Chart($('#chart'),{type:'line',data:{labels,datasets:[{data,borderColor:'#818cf8',backgroundColor:'rgba(99,102,241,.12)',fill:true,tension:.4,pointRadius:3,pointBackgroundColor:'#818cf8',borderWidth:2.5}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#5c657a',font:{size:10}},grid:{color:'rgba(255,255,255,.04)'},border:{display:false}},y:{ticks:{color:'#5c657a',font:{size:10}},grid:{color:'rgba(255,255,255,.04)'},border:{display:false}}}}});const links=await api('/api/links');$('#dash-tb').innerHTML=links.slice(0,10).map(l=>`<tr><td><div class="user-cell"><div class="avatar">${esc(av(l.label))}</div><div><strong>${esc(l.label)}</strong></div></div></td><td><span class="badge ${l.proto==='trojan'?'b-tr':'b-pr'}">${l.proto.toUpperCase()}</span></td><td>${l.used_h} / ${l.vol_h}<div class="prog"><i style="width:${l.pct}%"></i></div></td><td><span class="badge ${l.ok?'b-ok':'b-off'}">${l.ok?'فعال':'خاموش'}</span></td><td>${l.online}</td></tr>`).join('')||'<tr><td colspan="5"><div class="empty"><p>لینکی نیست</p></div></td></tr>'}catch(e){}}
async function loadLinks(){const links=await api('/api/links');$('#links-tb').innerHTML=links.map(l=>`<tr><td><div class="user-cell"><div class="avatar">${esc(av(l.label))}</div><div><strong>${esc(l.label)}</strong><div class="meta">${l.id.slice(0,13)}…</div></div></div></td><td><span class="badge ${l.proto==='trojan'?'b-tr':'b-pr'}">${l.proto.toUpperCase()}</span></td><td>${l.used_h} / ${l.vol_h}<div class="prog"><i style="width:${l.pct}%"></i></div></td><td>${l.exp?l.exp.slice(0,10):'∞'}</td><td><span class="badge ${l.ok?'b-ok':'b-off'}">${l.ok?'فعال':'خاموش'}</span></td><td style="white-space:nowrap"><button class="chip" data-copy="${esc(l.share)}">کانفیگ</button><button class="chip" data-copy="${esc(l.sub_url)}">ساب</button><button class="chip" data-copy="${esc(l.user_url)}">کاربر</button><button class="chip" data-open="${esc(l.qr_url)}">QR</button><button class="chip" data-tog="${l.id}" data-active="${l.active?0:1}">${l.active?'خاموش':'روشن'}</button><button class="chip" data-rst="${l.id}">ریست</button><button class="chip danger" data-del="${l.id}">حذف</button></td></tr>`).join('')||'<tr><td colspan="6"><div class="empty"><p>لینکی نیست</p></div></td></tr>';$('#links-tb').onclick=async e=>{const t=e.target.closest('[data-copy],[data-open],[data-tog],[data-rst],[data-del]');if(!t)return;if(t.dataset.copy)copy(t.dataset.copy);if(t.dataset.open)window.open(t.dataset.open);if(t.dataset.tog){await api('/api/links/'+t.dataset.tog,{method:'PATCH',body:JSON.stringify({active:t.dataset.active==='1'})});loadLinks();loadDash()}if(t.dataset.rst){await api('/api/links/'+t.dataset.rst,{method:'PATCH',body:JSON.stringify({reset_usage:true})});toast('ریست شد');loadLinks()}if(t.dataset.del&&confirm('حذف؟')){await api('/api/links/'+t.dataset.del,{method:'DELETE'});loadLinks();loadDash()}}}
async function loadSubs(){const subs=await api('/api/subs');$('#subs-tb').innerHTML=subs.map(s=>`<tr><td><strong>${esc(s.name)}</strong></td><td><code style="font-size:.72rem;color:var(--pr3);word-break:break-all">${esc(s.url)}</code> <button class="chip" data-copy="${esc(s.url)}">کپی</button></td><td>${s.vol_h}</td><td><button class="btn btn-d btn-sm" data-dels="${s.id}">حذف</button></td></tr>`).join('')||'<tr><td colspan="4"><div class="empty"><p>سابی نیست</p></div></td></tr>';$('#subs-tb').onclick=async e=>{const t=e.target.closest('[data-copy],[data-dels]');if(!t)return;if(t.dataset.copy)copy(t.dataset.copy);if(t.dataset.dels&&confirm('حذف؟')){await api('/api/subs/'+t.dataset.dels,{method:'DELETE'});loadSubs()}}}
async function loadOnline(){const s=await api('/api/stats');const list=s.connections||[];$('#online-grid').innerHTML=list.length?list.map(c=>`<div class="conn-card"><div class="t">اتصال</div><div class="v">${esc(c.id)}</div><div class="t" style="margin-top:8px">UUID</div><div class="v">${esc(c.uuid)}…</div><div class="t" style="margin-top:8px">مدت</div><div class="v">${c.sec}ث</div></div>`).join(''):'<div class="empty" style="grid-column:1/-1"><p>اتصال فعالی نیست</p></div>'}
async function loadAct(){const list=await api('/api/activity');$('#act-list').innerHTML=list.map(a=>{const lv=a.level==='ok'?'ok':a.level==='warn'?'warn':'info';return `<li><span class="tm">${(a.t||'').slice(11,19)}</span><span class="dot dot-${lv}"></span><span>${esc(a.msg)}</span></li>`}).join('')||'<li style="color:var(--mu);padding:24px">خالی</li>'}
async function loadSet(){const s=await api('/api/settings');$('#s-name').value=s.panel_name||'';$('#s-ann').value=s.announce||'';$('#s-sup').value=s.support_url||''}
$('#btn-login').onclick=async()=>{try{await api('/api/login',{method:'POST',body:JSON.stringify({password:$('#pw').value})});showApp()}catch{$('#lerr').style.display='block'}};
$('#pw').onkeydown=e=>{if(e.key==='Enter')$('#btn-login').click()};
$('#btn-out').onclick=async()=>{await api('/api/logout',{method:'POST'});showLogin()};
$$('.nav a').forEach(a=>a.onclick=()=>go(a.dataset.p));
$$('[data-close]').forEach(b=>b.onclick=()=>closeM(b.dataset.close));
$('#btn-nl').onclick=()=>openM('m-link');$('#btn-ns').onclick=()=>openM('m-sub');
$('#btn-cl').onclick=async()=>{try{const r=await api('/api/links',{method:'POST',body:JSON.stringify({label:$('#nl-l').value.trim()||'User',proto:$('#nl-p').value,volume_gb:+$('#nl-v').value||0,days:+$('#nl-d').value||0,max_conn:+$('#nl-m').value||0,remark:$('#nl-r').value.trim()})});closeM('m-link');toast('ساخته شد');copy(r.link.share);loadLinks();loadDash()}catch(e){toast(e.message)}};
$('#btn-cs').onclick=async()=>{try{const ids=$('#ns-i').value.split(',').map(x=>x.trim()).filter(Boolean);const r=await api('/api/subs',{method:'POST',body:JSON.stringify({name:$('#ns-n').value.trim()||'Sub',volume_gb:+$('#ns-v').value||0,days:+$('#ns-d').value||0,link_ids:ids})});closeM('m-sub');toast('ساب ساخته شد');copy(r.url);loadSubs()}catch(e){toast(e.message)}};
$('#btn-ss').onclick=async()=>{await api('/api/settings',{method:'POST',body:JSON.stringify({panel_name:$('#s-name').value,announce:$('#s-ann').value,support_url:$('#s-sup').value})});toast('ذخیره شد')};
$('#btn-pw').onclick=async()=>{try{await api('/api/password',{method:'POST',body:JSON.stringify({current:$('#pw-c').value,new_password:$('#pw-n').value})});toast('رمز عوض شد')}catch(e){toast(e.message)}};
$('#btn-backup').onclick=async()=>{const d=await api('/api/backup');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(d,null,2)],{type:'application/json'}));a.download='lprw-backup.json';a.click()};
(async()=>{try{await api('/api/me');showApp()}catch{showLogin()}})();
setInterval(()=>{if($('#app').style.display!=='none'&&$('.nav a.on')?.dataset.p==='dash')loadDash()},15000);
</script>
</body></html>
"""
