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
    <div style="width:52px;height:52px;border-radius:14px;background:var(--g);display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;margin-bottom:16px">LP</div>
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
    <div class="logo"><div class="mk">LP</div><div><h2 id="side-name">LPRW</h2><small id="side-ver">v4</small></div></div>
    <div class="nav-item active" data-page="home" onclick="go('home')">🏠 داشبورد</div>
    <div class="nav-item" data-page="links" onclick="go('links')">🔗 لینک‌ها</div>
    <div class="nav-item" data-page="inbounds" onclick="go('inbounds')">📡 پروتکل و اینباند</div>
    <div class="nav-item" data-page="subs" onclick="go('subs')">📋 سابسکریپشن</div>
    <div class="nav-item" data-page="online" onclick="go('online')">🟢 آنلاین</div>
    <div class="nav-item" data-page="settings" onclick="go('settings')">⚙️ تنظیمات</div>
    <div class="side-bottom">
      <button class="btn btn-sm" onclick="toggleTheme()">🌓 تم</button>
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
        <p style="color:var(--mu);font-size:.85rem;margin-bottom:12px">هر اینباند: پروتکل (vless/trojan/ss) + شبکه (ws/xhttp/httpupgrade) + امنیت (tls/none)</p>
        <div style="overflow:auto"><table><thead><tr><th>نام</th><th>پروتکل</th><th>شبکه</th><th>امنیت</th><th>مسیر</th><th></th></tr></thead><tbody id="ib-body"></tbody></table></div>
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
  <button class="active" data-page="home" onclick="go('home')"><span>🏠</span>خانه</button>
  <button data-page="links" onclick="go('links')"><span>🔗</span>لینک</button>
  <button data-page="inbounds" onclick="go('inbounds')"><span>📡</span>اینباند</button>
  <button data-page="online" onclick="go('online')"><span>🟢</span>آنلاین</button>
  <button data-page="settings" onclick="go('settings')"><span>⚙️</span>تنظیمات</button>
</nav>
</div>

<div class="modal-bg" id="m-link"><div class="modal">
  <h3>لینک جدید</h3>
  <div class="field"><label>نام</label><input id="ml-label"></div>
  <div class="field"><label>اینباند</label><select id="ml-ib"></select></div>
  <div class="form-row">
    <div class="field"><label>حجم (GB) — 0=نامحدود</label><input id="ml-vol" type="number" min="0" value="0"></div>
    <div class="field"><label>روز — 0=نامحدود</label><input id="ml-days" type="number" min="0" value="0"></div>
  </div>
  <div class="field"><label>یادداشت</label><input id="ml-remark"></div>
  <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
    <button class="btn" onclick="closeModals()">انصراف</button>
    <button class="btn btn-p" onclick="createLink()">ایجاد</button>
  </div>
</div></div>

<div class="modal-bg" id="m-ib"><div class="modal">
  <h3>اینباند جدید</h3>
  <div class="field"><label>نام</label><input id="mi-name" placeholder="مثلاً VLESS-XHTTP"></div>
  <div class="form-row">
    <div class="field"><label>پروتکل</label>
      <select id="mi-proto"><option value="vless">VLESS</option><option value="trojan">Trojan</option><option value="ss">Shadowsocks</option></select>
    </div>
    <div class="field"><label>شبکه</label>
      <select id="mi-net"><option value="ws">WebSocket</option><option value="xhttp">XHTTP</option><option value="httpupgrade">HTTPUpgrade</option></select>
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
  const titles={home:'داشبورد',links:'لینک‌ها',inbounds:'پروتکل و اینباند',subs:'سابسکریپشن',online:'آنلاین',settings:'تنظیمات'};
  $('#page-title').textContent=titles[p]||p;
  if(p==='links')loadLinks();
  if(p==='inbounds')loadInbounds();
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
      <button class="btn btn-sm" onclick="copyText(\`${l.share.replace(/`/g,'')}\`)">کپی</button>
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

async function loadSettings(){
  const s=await api('/api/settings');
  $('#s-name').value=s.panel_name||'';
  $('#s-announce').value=s.announce||'';
  $('#s-support').value=s.support_url||'';
}

function openLinkModal(){loadInbounds();$('#m-link').classList.add('show')}
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

async function createLink(){
  await api('/api/links',{method:'POST',body:JSON.stringify({
    label:$('#ml-label').value,inbound_id:$('#ml-ib').value,
    volume_gb:parseFloat($('#ml-vol').value)||0,days:parseInt($('#ml-days').value)||0,
    remark:$('#ml-remark').value
  })});
  closeModals();toast('لینک ساخته شد');loadLinks();
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
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{LABEL}} · LPRW</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#06080f;--card:rgba(18,22,36,.94);--bd:rgba(255,255,255,.08);--tx:#eef1f8;--mu:#8b93a8;--pr:#818cf8;--ok:#34d399;--er:#f87171;--g:linear-gradient(135deg,#6366f1,#d946ef)}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:Vazirmatn,sans-serif;background:var(--bg);color:var(--tx);min-height:100vh;padding:24px;display:flex;justify-content:center}
.card{width:100%;max-width:480px;background:var(--card);border:1px solid var(--bd);border-radius:20px;padding:28px;margin-top:20px}
h1{font-size:1.4rem;font-weight:800;margin-bottom:4px}
.sub{color:var(--mu);font-size:.85rem;margin-bottom:18px}
.row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--bd);font-size:.9rem}
.badge{display:inline-block;padding:4px 10px;border-radius:99px;font-size:.75rem;font-weight:700}
.badge.ok{background:rgba(52,211,153,.15);color:var(--ok)}.badge.bad{background:rgba(248,113,113,.15);color:var(--er)}
.bar{height:8px;background:rgba(255,255,255,.08);border-radius:99px;margin:12px 0 20px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--g);border-radius:99px}
.btn{display:inline-flex;padding:10px 14px;border-radius:12px;border:1px solid var(--bd);background:rgba(99,102,241,.15);color:var(--pr);font-weight:700;cursor:pointer;font-family:inherit;margin:4px 4px 4px 0}
code{display:block;background:rgba(0,0,0,.3);padding:12px;border-radius:10px;font-size:.72rem;word-break:break-all;margin:10px 0;direction:ltr;text-align:left}
img{max-width:180px;border-radius:12px;margin:10px auto;display:block}
</style>
</head>
<body>
<div class="card">
  <h1>{{LABEL}}</h1>
  <p class="sub">{{HOST}} · {{PROTO}}</p>
  <div class="row"><span>وضعیت</span><span class="badge {{STATUS_CLASS}}">{{STATUS}}</span></div>
  <div class="row"><span>مصرف</span><span>{{USED}} / {{VOL}}</span></div>
  <div class="bar"><i style="width:{{PCT}}%"></i></div>
  <div class="row"><span>انقضا</span><span>{{EXP}}</span></div>
  <div class="row"><span>آنلاین</span><span>{{ONLINE}}</span></div>
  <p style="margin-top:16px;font-size:.8rem;color:var(--mu)">لینک کانفیگ</p>
  <code id="cfg">{{SHARE}}</code>
  <button class="btn" onclick="navigator.clipboard.writeText(document.getElementById('cfg').textContent)">کپی کانفیگ</button>
  <button class="btn" onclick="navigator.clipboard.writeText('{{SUB}}')">کپی ساب</button>
  <img src="{{QR}}" alt="QR">
  <p style="text-align:center;font-size:.75rem;color:var(--mu);margin-top:12px">LPRW {{VERSION}}</p>
</div>
</body>
</html>
'''
