"""LPRW premium dashboard UI."""
DASHBOARD = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LPRW Panel</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#06080f;--s1:#0d1019;--s2:#131722;--s3:#1a1f2e;--bd:rgba(255,255,255,.06);--bd2:rgba(255,255,255,.1);--tx:#eef0f6;--mu:#7b849c;--pr:#6366f1;--pr2:#818cf8;--ok:#22c55e;--er:#ef4444;--g1:linear-gradient(135deg,#6366f1,#8b5cf6,#a855f7);--r:16px}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:Vazirmatn,system-ui,sans-serif;background:var(--bg);color:var(--tx);min-height:100vh;line-height:1.65;background-image:radial-gradient(ellipse 80% 50% at 10% -10%,rgba(99,102,241,.12),transparent),radial-gradient(ellipse 60% 40% at 100% 0%,rgba(168,85,247,.08),transparent)}
button,input,select{font-family:inherit;font-size:.9rem}.hidden{display:none!important}
#login{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.box{width:100%;max-width:400px;background:rgba(13,16,25,.92);backdrop-filter:blur(24px);border:1px solid var(--bd2);border-radius:24px;padding:44px 36px;box-shadow:0 30px 100px rgba(0,0,0,.6)}
.logo{font-size:2rem;font-weight:800;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px}
.sub{color:var(--mu);margin-bottom:28px;font-size:.9rem}
.fg{margin-bottom:16px}.fg label{display:block;margin-bottom:6px;color:var(--mu);font-size:.82rem;font-weight:500}
.fg input,.fg select{width:100%;padding:13px 16px;background:var(--s2);border:1px solid var(--bd);border-radius:12px;color:var(--tx);outline:none}
.fg input:focus,.fg select:focus{border-color:var(--pr);box-shadow:0 0 0 3px rgba(99,102,241,.15)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 20px;border:none;border-radius:12px;cursor:pointer;font-weight:600;transition:.2s}
.btn-p{background:var(--g1);color:#fff;width:100%}.btn-p:hover{filter:brightness(1.1);box-shadow:0 8px 24px rgba(99,102,241,.35)}
.btn-g{background:transparent;border:1px solid var(--bd2);color:var(--tx)}.btn-g:hover{background:var(--s3)}
.btn-d{background:rgba(239,68,68,.15);color:#fca5a5;border:1px solid rgba(239,68,68,.25)}.btn-sm{padding:7px 12px;font-size:.78rem;border-radius:9px}
.btn-ok{background:rgba(34,197,94,.15);color:#86efac;border:1px solid rgba(34,197,94,.25)}
.err{color:var(--er);font-size:.85rem;margin-top:12px;display:none}
#app{display:none}
.side{position:fixed;right:0;top:0;bottom:0;width:250px;background:rgba(13,16,25,.95);border-left:1px solid var(--bd);padding:28px 16px;display:flex;flex-direction:column;z-index:40}
.side .logo{font-size:1.45rem;padding:0 10px}.side .ver{font-size:.72rem;color:var(--mu);padding:0 10px;margin-bottom:24px}
.nav a{display:block;padding:12px 14px;border-radius:12px;color:var(--mu);cursor:pointer;margin-bottom:4px;font-size:.9rem;font-weight:500}
.nav a:hover{background:var(--s3);color:var(--tx)}.nav a.on{background:rgba(99,102,241,.12);color:var(--pr2);border:1px solid rgba(99,102,241,.2)}
.side-foot{margin-top:auto;border-top:1px solid var(--bd);padding-top:14px}
.side-foot .host{font-size:.7rem;color:var(--mu);word-break:break-all;margin-bottom:10px;padding:0 6px}
.main{margin-right:250px;padding:32px 36px;min-height:100vh}
.pt{font-size:1.45rem;font-weight:700;margin-bottom:4px}.ps{color:var(--mu);font-size:.88rem;margin-bottom:24px}
.head{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:12px}
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-bottom:24px}
.sc{background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);padding:18px 20px}
.sc .lb{color:var(--mu);font-size:.78rem;margin-bottom:6px}.sc .vl{font-size:1.5rem;font-weight:700}
.tw{background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);overflow:hidden}
table{width:100%;border-collapse:collapse;font-size:.85rem}
th{text-align:right;padding:13px 14px;background:var(--s2);color:var(--mu);font-weight:600;font-size:.72rem;text-transform:uppercase}
td{padding:13px 14px;border-top:1px solid var(--bd);vertical-align:middle}tr:hover td{background:rgba(99,102,241,.03)}
.badge{display:inline-block;padding:3px 9px;border-radius:99px;font-size:.72rem;font-weight:600}
.b-ok{background:rgba(34,197,94,.12);color:#4ade80}.b-off{background:rgba(239,68,68,.12);color:#f87171}
.b-pr{background:rgba(99,102,241,.12);color:#a5b4fc}.b-tr{background:rgba(168,85,247,.12);color:#d8b4fe}
.prog{height:6px;background:var(--s3);border-radius:99px;overflow:hidden;min-width:70px;margin-top:5px}.prog i{display:block;height:100%;background:var(--g1);border-radius:99px}
.chip{background:var(--s3);border:1px solid var(--bd);padding:4px 8px;border-radius:8px;font-size:.72rem;cursor:pointer;color:var(--mu);margin:2px}.chip:hover{color:var(--tx);border-color:var(--pr)}
.ov{position:fixed;inset:0;background:rgba(0,0,0,.7);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;z-index:100;padding:20px}
.md{background:var(--s1);border:1px solid var(--bd2);border-radius:20px;padding:30px;width:100%;max-width:480px;max-height:90vh;overflow-y:auto}
.md h2{font-size:1.15rem;margin-bottom:20px}.row2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.acts{display:flex;gap:10px;justify-content:flex-end;margin-top:22px}
.chart-box{background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);padding:18px;margin-bottom:24px;height:250px}
.al{list-style:none}.al li{padding:11px 0;border-bottom:1px solid var(--bd);font-size:.86rem;display:flex;gap:12px}
.al .tm{color:var(--mu);font-size:.75rem;min-width:60px}
.toast{position:fixed;bottom:28px;left:28px;background:var(--s2);border:1px solid var(--bd2);padding:13px 20px;border-radius:14px;font-size:.88rem;z-index:200;max-width:300px}
.empty{text-align:center;padding:40px;color:var(--mu)}
@media(max-width:900px){.side{width:100%;height:auto;position:relative;border:0;border-bottom:1px solid var(--bd);flex-direction:row;flex-wrap:wrap;padding:12px}.side .ver,.side-foot{display:none}.nav{display:flex;flex-wrap:wrap;gap:4px}.nav a{padding:8px 12px;font-size:.82rem}.main{margin-right:0;padding:18px 14px}.row2{grid-template-columns:1fr}}
</style>
</head>
<body>
<div id="login"><div class="box">
<div class="logo">LPRW</div>
<div class="sub">Leviko Panel — ورود مدیر</div>
<div class="fg"><label>رمز عبور</label><input type="password" id="pw" autofocus></div>
<button class="btn btn-p" id="btn-login">ورود</button>
<p class="err" id="lerr">رمز اشتباه است</p>
</div></div>
<div id="app">
<aside class="side">
<div class="logo">LPRW</div>
<div class="ver">v2.1 · Leviko Panel</div>
<nav class="nav">
<a class="on" data-p="dash">داشبورد</a>
<a data-p="links">لینک‌ها</a>
<a data-p="subs">سابسکریپشن</a>
<a data-p="act">فعالیت‌ها</a>
<a data-p="set">تنظیمات</a>
</nav>
<div class="side-foot"><div class="host" id="shost">—</div>
<button class="btn btn-g btn-sm" style="width:100%" id="btn-out">خروج</button></div>
</aside>
<main class="main">
<section id="p-dash">
<div class="pt">داشبورد</div><div class="ps" id="announce"></div>
<div class="sg">
<div class="sc"><div class="lb">ترافیک کل</div><div class="vl" id="st-b">—</div></div>
<div class="sc"><div class="lb">آنلاین</div><div class="vl" id="st-o">—</div></div>
<div class="sc"><div class="lb">لینک فعال</div><div class="vl" id="st-l">—</div></div>
<div class="sc"><div class="lb">آپ‌تایم</div><div class="vl" id="st-u">—</div></div>
</div>
<div class="chart-box"><canvas id="chart"></canvas></div>
<div class="tw"><table><thead><tr><th>برچسب</th><th>پروتکل</th><th>مصرف</th><th>وضعیت</th><th>آنلاین</th></tr></thead><tbody id="dash-tb"></tbody></table></div>
</section>
<section id="p-links" class="hidden">
<div class="head"><div><div class="pt">لینک‌ها</div><div class="ps">VLESS / Trojan</div></div>
<button class="btn btn-p" style="width:auto" id="btn-nl">+ لینک جدید</button></div>
<div class="tw"><table><thead><tr><th>برچسب</th><th>پروتکل</th><th>مصرف</th><th>انقضا</th><th>وضعیت</th><th>عملیات</th></tr></thead><tbody id="links-tb"></tbody></table></div>
</section>
<section id="p-subs" class="hidden">
<div class="head"><div><div class="pt">سابسکریپشن</div><div class="ps">اشتراک گروهی</div></div>
<button class="btn btn-p" style="width:auto" id="btn-ns">+ ساب جدید</button></div>
<div class="tw"><table><thead><tr><th>نام</th><th>آدرس</th><th>حجم</th><th>عملیات</th></tr></thead><tbody id="subs-tb"></tbody></table></div>
</section>
<section id="p-act" class="hidden">
<div class="pt">فعالیت‌ها</div><div class="ps">رویدادهای اخیر</div>
<ul class="al" id="act-list"></ul>
</section>
<section id="p-set" class="hidden">
<div class="pt">تنظیمات</div><div class="ps">پیکربندی پنل</div>
<div class="tw" style="padding:26px;max-width:520px">
<div class="fg"><label>نام پنل</label><input id="s-name"></div>
<div class="fg"><label>اعلان داشبورد</label><input id="s-ann"></div>
<div class="fg"><label>پشتیبانی</label><input id="s-sup"></div>
<div class="fg"><label>Path VLESS</label><input id="s-pv" value="/ws"></div>
<div class="fg"><label>Path Trojan</label><input id="s-pt" value="/trojan"></div>
<button class="btn btn-p" style="width:auto" id="btn-ss">ذخیره</button>
<hr style="border:0;border-top:1px solid var(--bd);margin:24px 0">
<div class="pt" style="font-size:1.05rem">تغییر رمز</div>
<div class="fg" style="margin-top:12px"><label>رمز فعلی</label><input type="password" id="pw-c"></div>
<div class="fg"><label>رمز جدید</label><input type="password" id="pw-n"></div>
<button class="btn btn-ok" style="width:auto" id="btn-pw">تغییر رمز</button>
</div></section>
</main></div>
<div id="m-link" class="ov hidden"><div class="md">
<h2>لینک جدید</h2>
<div class="fg"><label>برچسب</label><input id="nl-l"></div>
<div class="row2">
<div class="fg"><label>پروتکل</label><select id="nl-p"><option value="vless">VLESS</option><option value="trojan">Trojan</option></select></div>
<div class="fg"><label>حجم GB (0=∞)</label><input id="nl-v" type="number" min="0" step="0.5" value="0"></div>
</div>
<div class="row2">
<div class="fg"><label>روز (0=∞)</label><input id="nl-d" type="number" min="0" value="30"></div>
<div class="fg"><label>حد اتصال (0=∞)</label><input id="nl-m" type="number" min="0" value="0"></div>
</div>
<div class="fg"><label>یادداشت</label><input id="nl-r"></div>
<div class="acts"><button class="btn btn-g" data-close="m-link">انصراف</button>
<button class="btn btn-p" style="width:auto" id="btn-cl">ایجاد</button></div>
</div></div>
<div id="m-sub" class="ov hidden"><div class="md">
<h2>ساب جدید</h2>
<div class="fg"><label>نام</label><input id="ns-n"></div>
<div class="row2">
<div class="fg"><label>حجم GB</label><input id="ns-v" type="number" min="0" value="0"></div>
<div class="fg"><label>روز</label><input id="ns-d" type="number" min="0" value="30"></div>
</div>
<div class="fg"><label>UUID لینک‌ها (کاما / خالی=همه)</label><input id="ns-i"></div>
<div class="acts"><button class="btn btn-g" data-close="m-sub">انصراف</button>
<button class="btn btn-p" style="width:auto" id="btn-cs">ایجاد</button></div>
</div></div>
<script>
const $=s=>document.querySelector(s),$$=s=>document.querySelectorAll(s);
let chart=null;
function toast(m){const t=document.createElement('div');t.className='toast';t.textContent=m;document.body.appendChild(t);setTimeout(()=>t.remove(),2800)}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function copy(t){navigator.clipboard.writeText(t).then(()=>toast('کپی شد'))}
async function api(p,o={}){const r=await fetch(p,{credentials:'include',headers:{'Content-Type':'application/json',...(o.headers||{})},...o});if(r.status===401){showLogin();throw new Error('auth')}const d=await r.json().catch(()=>({}));if(!r.ok)throw new Error(typeof d.detail==='string'?d.detail:'خطا');return d}
function showLogin(){$('#login').style.display='flex';$('#app').style.display='none'}
function showApp(){$('#login').style.display='none';$('#app').style.display='block';go('dash')}
function go(p){$$('.nav a').forEach(a=>a.classList.toggle('on',a.dataset.p===p));['dash','links','subs','act','set'].forEach(x=>{const e=$('#p-'+x);if(e)e.classList.toggle('hidden',x!==p)});if(p==='dash')loadDash();if(p==='links')loadLinks();if(p==='subs')loadSubs();if(p==='act')loadAct();if(p==='set')loadSet()}
function openM(id){$('#'+id).classList.remove('hidden')}function closeM(id){$('#'+id).classList.add('hidden')}
function up(s){const h=Math.floor(s/3600),m=Math.floor((s%3600)/60);return h>0?h+'س '+m+'د':m+'د'}
async function loadDash(){try{const s=await api('/api/stats');$('#st-b').textContent=s.bytes_h;$('#st-o').textContent=s.online;$('#st-l').textContent=s.active_links+'/'+s.links;$('#st-u').textContent=up(s.uptime);$('#shost').textContent=s.host||'—';$('#announce').textContent=s.announce||'وضعیت سرویس';const labels=Object.keys(s.hourly||{}),data=Object.values(s.hourly||{});if(chart)chart.destroy();chart=new Chart($('#chart'),{type:'line',data:{labels,datasets:[{data,borderColor:'#818cf8',backgroundColor:'rgba(99,102,241,.12)',fill:true,tension:.4,pointRadius:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#7b849c',font:{size:10}},grid:{color:'rgba(255,255,255,.04)'}},y:{ticks:{color:'#7b849c',font:{size:10}},grid:{color:'rgba(255,255,255,.04)'}}}}});const links=await api('/api/links');$('#dash-tb').innerHTML=links.slice(0,10).map(l=>`<tr><td><strong>${esc(l.label)}</strong></td><td><span class="badge ${l.proto==='trojan'?'b-tr':'b-pr'}">${l.proto.toUpperCase()}</span></td><td>${l.used_h} / ${l.vol_h}<div class="prog"><i style="width:${l.pct}%"></i></div></td><td><span class="badge ${l.ok?'b-ok':'b-off'}">${l.ok?'فعال':'خاموش'}</span></td><td>${l.online}</td></tr>`).join('')||'<tr><td colspan="5"><div class="empty">لینکی نیست</div></td></tr>'}catch(e){}}
async function loadLinks(){const links=await api('/api/links');$('#links-tb').innerHTML=links.map(l=>`<tr>
<td><strong>${esc(l.label)}</strong><div style="font-size:.68rem;color:var(--mu)">${l.id.slice(0,12)}…</div></td>
<td><span class="badge ${l.proto==='trojan'?'b-tr':'b-pr'}">${l.proto.toUpperCase()}</span></td>
<td>${l.used_h} / ${l.vol_h}<div class="prog"><i style="width:${l.pct}%"></i></div></td>
<td>${l.exp?l.exp.slice(0,10):'∞'}</td>
<td><span class="badge ${l.ok?'b-ok':'b-off'}">${l.ok?'فعال':'خاموش'}</span></td>
<td>
<button class="chip" data-copy="${esc(l.share)}">کانفیگ</button>
<button class="chip" data-copy="${esc(l.user_url)}">کاربر</button>
<button class="chip" data-open="${esc(l.qr_url)}">QR</button>
<button class="chip" data-tog="${l.id}" data-active="${l.active?0:1}">${l.active?'خاموش':'روشن'}</button>
<button class="chip" data-rst="${l.id}">ریست</button>
<button class="chip" style="color:#fca5a5" data-del="${l.id}">حذف</button>
</td></tr>`).join('')||'<tr><td colspan="6"><div class="empty">لینکی نیست</div></td></tr>';
$('#links-tb').onclick=async e=>{const t=e.target;if(t.dataset.copy)copy(t.dataset.copy);if(t.dataset.open)window.open(t.dataset.open);if(t.dataset.tog){await api('/api/links/'+t.dataset.tog,{method:'PATCH',body:JSON.stringify({active:t.dataset.active==='1'})});loadLinks();loadDash()}if(t.dataset.rst){await api('/api/links/'+t.dataset.rst,{method:'PATCH',body:JSON.stringify({reset_usage:true})});toast('ریست شد');loadLinks()}if(t.dataset.del&&confirm('حذف؟')){await api('/api/links/'+t.dataset.del,{method:'DELETE'});loadLinks();loadDash()}}}
async function loadSubs(){const subs=await api('/api/subs');$('#subs-tb').innerHTML=subs.map(s=>`<tr><td><strong>${esc(s.name)}</strong></td><td><code style="font-size:.72rem;color:var(--pr2);word-break:break-all">${esc(s.url)}</code> <button class="chip" data-copy="${esc(s.url)}">کپی</button></td><td>${s.vol_h}</td><td><button class="btn btn-d btn-sm" data-dels="${s.id}">حذف</button></td></tr>`).join('')||'<tr><td colspan="4"><div class="empty">سابی نیست</div></td></tr>';
$('#subs-tb').onclick=async e=>{const t=e.target;if(t.dataset.copy)copy(t.dataset.copy);if(t.dataset.dels&&confirm('حذف ساب؟')){await api('/api/subs/'+t.dataset.dels,{method:'DELETE'});loadSubs()}}}
async function loadAct(){const list=await api('/api/activity');$('#act-list').innerHTML=list.map(a=>`<li><span class="tm">${(a.t||'').slice(11,19)}</span><span>${esc(a.msg)}</span></li>`).join('')||'<li style="color:var(--mu)">خالی</li>'}
async function loadSet(){const s=await api('/api/settings');$('#s-name').value=s.panel_name||'';$('#s-ann').value=s.announce||'';$('#s-sup').value=s.support_url||'';$('#s-pv').value=s.path_vless||'/ws';$('#s-pt').value=s.path_trojan||'/trojan'}
$('#btn-login').onclick=async()=>{try{await api('/api/login',{method:'POST',body:JSON.stringify({password:$('#pw').value})});showApp()}catch{$('#lerr').style.display='block'}};
$('#pw').onkeydown=e=>{if(e.key==='Enter')$('#btn-login').click()};
$('#btn-out').onclick=async()=>{await api('/api/logout',{method:'POST'});showLogin()};
$$('.nav a').forEach(a=>a.onclick=()=>go(a.dataset.p));
$$('[data-close]').forEach(b=>b.onclick=()=>closeM(b.dataset.close));
$('#btn-nl').onclick=()=>openM('m-link');$('#btn-ns').onclick=()=>openM('m-sub');
$('#btn-cl').onclick=async()=>{try{const r=await api('/api/links',{method:'POST',body:JSON.stringify({label:$('#nl-l').value.trim()||'User',proto:$('#nl-p').value,volume_gb:+$('#nl-v').value||0,days:+$('#nl-d').value||0,max_conn:+$('#nl-m').value||0,remark:$('#nl-r').value.trim()})});closeM('m-link');toast('ساخته شد');copy(r.link.share);loadLinks();loadDash()}catch(e){toast(e.message)}};
$('#btn-cs').onclick=async()=>{try{const ids=$('#ns-i').value.split(',').map(x=>x.trim()).filter(Boolean);const r=await api('/api/subs',{method:'POST',body:JSON.stringify({name:$('#ns-n').value.trim()||'Sub',volume_gb:+$('#ns-v').value||0,days:+$('#ns-d').value||0,link_ids:ids})});closeM('m-sub');toast('ساب ساخته شد');copy(r.url);loadSubs()}catch(e){toast(e.message)}};
$('#btn-ss').onclick=async()=>{await api('/api/settings',{method:'POST',body:JSON.stringify({panel_name:$('#s-name').value,announce:$('#s-ann').value,support_url:$('#s-sup').value,path_vless:$('#s-pv').value,path_trojan:$('#s-pt').value})});toast('ذخیره شد')};
$('#btn-pw').onclick=async()=>{try{await api('/api/password',{method:'POST',body:JSON.stringify({current:$('#pw-c').value,new_password:$('#pw-n').value})});toast('رمز عوض شد');$('#pw-c').value='';$('#pw-n').value=''}catch(e){toast(e.message)}};
(async()=>{try{await api('/api/me');showApp()}catch{showLogin()}})();
setInterval(()=>{if($('#app').style.display!=='none'&&$('.nav a.on')?.dataset.p==='dash')loadDash()},20000);
</script>
</body></html>
"""
