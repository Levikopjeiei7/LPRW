"""LPRW premium UI — dashboard + user portal."""

DASHBOARD = r'''<!DOCTYPE html>
<html lang="fa" dir="rtl" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#05070d">
<title>LPRW · Leviko Panel Railway</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#05070d;--bg2:#0a0d16;--s1:rgba(16,19,32,.82);--s2:rgba(22,26,42,.94);--s3:rgba(28,33,52,.98);--bd:rgba(255,255,255,.06);--bd2:rgba(255,255,255,.11);--bd3:rgba(99,102,241,.35);--tx:#f1f3f9;--mu:#8b93a8;--mu2:#5c657a;--pr:#6366f1;--pr2:#818cf8;--pr3:#a5b4fc;--ok:#34d399;--er:#f87171;--wn:#fbbf24;--cy:#22d3ee;--pk:#e879f9;--g1:linear-gradient(135deg,#6366f1 0%,#8b5cf6 45%,#d946ef 100%);--shadow:0 28px 70px rgba(0,0,0,.55);--r:20px;--side:272px}
[data-theme="light"]{--bg:#f4f6fb;--bg2:#e8ecf6;--s1:rgba(255,255,255,.92);--s2:#fff;--s3:#f8fafc;--bd:rgba(15,23,42,.08);--bd2:rgba(15,23,42,.12);--tx:#0f172a;--mu:#64748b;--mu2:#94a3b8;--shadow:0 20px 50px rgba(15,23,42,.12)}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:Vazirmatn,system-ui,sans-serif;background:var(--bg);color:var(--tx);min-height:100vh;line-height:1.65;overflow-x:hidden}
body::before,body::after{content:"";position:fixed;pointer-events:none;z-index:0;border-radius:50%;filter:blur(100px)}
body::before{width:560px;height:560px;top:-120px;right:-80px;background:radial-gradient(circle,rgba(99,102,241,.32),transparent 68%)}
body::after{width:480px;height:480px;bottom:-100px;left:-60px;background:radial-gradient(circle,rgba(217,70,239,.16),transparent 70%)}
button,input,select{font-family:inherit;font-size:.9rem;color:var(--tx)}.hidden{display:none!important}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-thumb{background:rgba(129,140,248,.35);border-radius:99px}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
#login{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;position:relative;z-index:2}
.login-card{width:100%;max-width:460px;background:linear-gradient(165deg,var(--s2),var(--s1));border:1px solid var(--bd2);border-radius:28px;padding:48px 40px;box-shadow:var(--shadow);position:relative;overflow:hidden;animation:rise .55s ease}
.login-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--g1)}
.brand-mark{width:64px;height:64px;border-radius:18px;background:var(--g1);display:grid;place-items:center;font-weight:900;font-size:1.35rem;color:#fff;margin-bottom:22px;box-shadow:0 16px 40px rgba(99,102,241,.45)}
.login-card h1{font-size:1.85rem;font-weight:800}.login-card .sub{color:var(--mu);margin:8px 0 28px;font-size:.92rem}
.field{margin-bottom:16px}.field label{display:block;font-size:.78rem;color:var(--mu);margin-bottom:8px;font-weight:600}
.field input,.field select{width:100%;padding:14px 16px;border-radius:14px;border:1px solid var(--bd2);background:rgba(0,0,0,.25);outline:none}
[data-theme="light"] .field input,[data-theme="light"] .field select{background:#f8fafc}
.field input:focus{border-color:var(--pr);box-shadow:0 0 0 4px rgba(99,102,241,.2)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 20px;border-radius:14px;border:1px solid var(--bd2);cursor:pointer;font-weight:700;background:var(--s3);color:var(--tx)}
.btn-p{background:var(--g1);color:#fff;border:none;box-shadow:0 12px 30px rgba(99,102,241,.35)}.btn-block{width:100%;padding:15px}
.btn-sm{padding:8px 12px;font-size:.8rem;border-radius:10px}.btn-d{background:rgba(248,113,113,.12);color:var(--er);border-color:rgba(248,113,113,.25)}
.err{display:none;margin-top:12px;padding:10px 14px;border-radius:12px;background:rgba(248,113,113,.12);color:var(--er);font-size:.85rem}
.login-foot{margin-top:22px;text-align:center;font-size:.75rem;color:var(--mu2)}
#app{display:none;min-height:100vh;position:relative;z-index:1}
.shell{display:grid;grid-template-columns:var(--side) 1fr;min-height:100vh}

.bottom-nav{display:none;position:fixed;bottom:0;left:0;right:0;z-index:60;background:var(--s2);border-top:1px solid var(--bd);padding:8px 6px calc(8px + env(safe-area-inset-bottom));justify-content:space-around;gap:4px;backdrop-filter:blur(14px);box-shadow:0 -8px 30px rgba(0,0,0,.25)}
.bottom-nav button{flex:1;border:none;background:transparent;color:var(--mu);font-family:inherit;font-size:.68rem;font-weight:700;padding:8px 4px;border-radius:12px;cursor:pointer}
.bottom-nav button.active{color:var(--pr3);background:rgba(99,102,241,.14)}
.bottom-nav button span{display:block;font-size:1.05rem;margin-bottom:2px}

@media(max-width:960px){
.shell{grid-template-columns:1fr}
.side{display:none!important}
.side-backdrop{display:none!important}
.burger{display:none!important}
.main{padding:14px 14px 96px!important}
.topbar h1{font-size:1.15rem}
.kpis{grid-template-columns:repeat(2,1fr)!important}
.bottom-nav{display:flex!important}
}
.side{background:linear-gradient(180deg,var(--s2),var(--s1));border-left:1px solid var(--bd);padding:22px 16px;display:flex;flex-direction:column;gap:6px}
.side .logo{display:flex;align-items:center;gap:12px;padding:8px 10px 20px;border-bottom:1px solid var(--bd);margin-bottom:12px}
.side .logo .mk{width:42px;height:42px;border-radius:12px;background:var(--g1);display:grid;place-items:center;font-weight:900;color:#fff}
.side .logo h2{font-size:1.05rem;font-weight:800}.side .logo small{color:var(--mu);font-size:.72rem}
.nav-item{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:12px;color:var(--mu);cursor:pointer;font-weight:600;font-size:.9rem;border:1px solid transparent}
.nav-item:hover{background:rgba(99,102,241,.08);color:var(--tx)}.nav-item.active{background:rgba(99,102,241,.15);color:var(--pr3);border-color:rgba(99,102,241,.25)}
.side-bottom{margin-top:auto;padding-top:16px;border-top:1px solid var(--bd);display:flex;flex-direction:column;gap:8px}
.main{padding:22px 26px 40px;max-width:1400px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:22px;flex-wrap:wrap}
.topbar h1{font-size:1.45rem;font-weight:800}.topbar .acts{display:flex;gap:8px;flex-wrap:wrap}
.burger{display:none;background:var(--s2);border:1px solid var(--bd2);border-radius:12px;padding:10px 12px;cursor:pointer}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:22px}
@media(max-width:1100px){.kpis{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){.kpis{grid-template-columns:1fr}}
.kpi{background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);padding:18px;position:relative;overflow:hidden;animation:rise .5s ease}
.kpi .t{font-size:.78rem;color:var(--mu);font-weight:600;margin-bottom:8px}.kpi .v{font-size:1.55rem;font-weight:800}.kpi .s{font-size:.75rem;color:var(--mu2);margin-top:6px}
.panel{background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);padding:20px;margin-bottom:18px}
.panel-h{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap}.panel-h h3{font-size:1.05rem;font-weight:800}
.grid-2{display:grid;grid-template-columns:1.4fr 1fr;gap:16px}@media(max-width:960px){.grid-2{grid-template-columns:1fr}}
table{width:100%;border-collapse:collapse}th,td{padding:12px 10px;text-align:right;border-bottom:1px solid var(--bd);font-size:.86rem}th{color:var(--mu);font-weight:700;font-size:.75rem}
code{font-family:ui-monospace,monospace;font-size:.78rem;color:var(--pr3)}
.chip{display:inline-flex;padding:5px 10px;border-radius:99px;font-size:.75rem;font-weight:700;background:rgba(99,102,241,.12);color:var(--pr3);border:1px solid rgba(99,102,241,.2);cursor:pointer}
.badge{display:inline-block;padding:4px 10px;border-radius:99px;font-size:.72rem;font-weight:700}.badge.on{background:rgba(52,211,153,.15);color:var(--ok)}.badge.off{background:rgba(248,113,113,.15);color:var(--er)}
.modal-bg{position:fixed;inset:0;background:rgba(0,0,0,.62);backdrop-filter:blur(6px);z-index:80;display:none;align-items:center;justify-content:center;padding:18px}.modal-bg.show{display:flex}
.modal{background:var(--s2);border:1px solid var(--bd2);border-radius:22px;padding:24px;width:100%;max-width:520px;box-shadow:var(--shadow);max-height:90vh;overflow:auto}
.modal h3{font-size:1.15rem;font-weight:800;margin-bottom:16px}.form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:560px){.form-row{grid-template-columns:1fr}}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(20px);background:var(--s3);border:1px solid var(--bd2);padding:12px 18px;border-radius:14px;z-index:99;opacity:0;transition:.25s;font-weight:600}.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.empty{text-align:center;padding:36px 16px;color:var(--mu)}
.conn-card{background:var(--s2);border:1px solid var(--bd);border-radius:14px;padding:14px}.conn-card .t{font-size:.72rem;color:var(--mu)}.conn-card .v{font-size:.85rem;font-weight:700;word-break:break-all}
#online-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
#act-list{list-style:none}#act-list li{display:flex;gap:10px;align-items:center;padding:10px 0;border-bottom:1px solid var(--bd);font-size:.85rem}
.dot{width:8px;height:8px;border-radius:50%}.dot-ok{background:var(--ok)}.dot-warn{background:var(--wn)}.dot-info{background:var(--pr2)}.tm{color:var(--mu2);font-size:.75rem;min-width:52px}
.chart-box{position:relative;height:260px}

.fx-0{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-0{padding:4px}
.gap-0{gap:4px}
.radius-0{border-radius:6px}
.op-0{opacity:0.30}
.shadow-lv-0{box-shadow:0 4px 16px rgba(0,0,0,0.15)}


.fx-1{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-1{padding:5px}
.gap-1{gap:5px}
.radius-1{border-radius:7px}
.op-1{opacity:0.31}
.shadow-lv-1{box-shadow:0 5px 17px rgba(0,0,0,0.16)}


.fx-2{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-2{padding:6px}
.gap-2{gap:6px}
.radius-2{border-radius:8px}
.op-2{opacity:0.32}
.shadow-lv-2{box-shadow:0 6px 18px rgba(0,0,0,0.17)}


.fx-3{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-3{padding:7px}
.gap-3{gap:7px}
.radius-3{border-radius:9px}
.op-3{opacity:0.33}
.shadow-lv-3{box-shadow:0 7px 19px rgba(0,0,0,0.18)}


.fx-4{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-4{padding:8px}
.gap-4{gap:8px}
.radius-4{border-radius:10px}
.op-4{opacity:0.34}
.shadow-lv-4{box-shadow:0 8px 20px rgba(0,0,0,0.19)}


.fx-5{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-5{padding:9px}
.gap-5{gap:9px}
.radius-5{border-radius:11px}
.op-5{opacity:0.35}
.shadow-lv-5{box-shadow:0 9px 21px rgba(0,0,0,0.20)}


.fx-6{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-6{padding:10px}
.gap-6{gap:10px}
.radius-6{border-radius:12px}
.op-6{opacity:0.36}
.shadow-lv-6{box-shadow:0 10px 22px rgba(0,0,0,0.21)}


.fx-7{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-7{padding:11px}
.gap-7{gap:11px}
.radius-7{border-radius:13px}
.op-7{opacity:0.37}
.shadow-lv-7{box-shadow:0 11px 23px rgba(0,0,0,0.22)}


.fx-8{transition:all .10s cubic-bezier(.4,0,.2,1)}
.pad-8{padding:12px}
.gap-8{gap:12px}
.radius-8{border-radius:14px}
.op-8{opacity:0.38}
.shadow-lv-8{box-shadow:0 12px 24px rgba(0,0,0,0.23)}


.fx-9{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-9{padding:13px}
.gap-9{gap:13px}
.radius-9{border-radius:15px}
.op-9{opacity:0.39}
.shadow-lv-9{box-shadow:0 13px 25px rgba(0,0,0,0.24)}


.fx-10{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-10{padding:14px}
.gap-10{gap:14px}
.radius-10{border-radius:16px}
.op-10{opacity:0.40}
.shadow-lv-10{box-shadow:0 14px 26px rgba(0,0,0,0.25)}


.fx-11{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-11{padding:15px}
.gap-11{gap:15px}
.radius-11{border-radius:17px}
.op-11{opacity:0.41}
.shadow-lv-11{box-shadow:0 15px 27px rgba(0,0,0,0.26)}


.fx-12{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-12{padding:16px}
.gap-12{gap:16px}
.radius-12{border-radius:18px}
.op-12{opacity:0.42}
.shadow-lv-12{box-shadow:0 4px 28px rgba(0,0,0,0.27)}


.fx-13{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-13{padding:17px}
.gap-13{gap:17px}
.radius-13{border-radius:19px}
.op-13{opacity:0.43}
.shadow-lv-13{box-shadow:0 5px 29px rgba(0,0,0,0.28)}


.fx-14{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-14{padding:18px}
.gap-14{gap:18px}
.radius-14{border-radius:20px}
.op-14{opacity:0.44}
.shadow-lv-14{box-shadow:0 6px 30px rgba(0,0,0,0.29)}


.fx-15{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-15{padding:19px}
.gap-15{gap:19px}
.radius-15{border-radius:21px}
.op-15{opacity:0.45}
.shadow-lv-15{box-shadow:0 7px 31px rgba(0,0,0,0.30)}


.fx-16{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-16{padding:20px}
.gap-16{gap:4px}
.radius-16{border-radius:22px}
.op-16{opacity:0.46}
.shadow-lv-16{box-shadow:0 8px 32px rgba(0,0,0,0.31)}


.fx-17{transition:all .10s cubic-bezier(.4,0,.2,1)}
.pad-17{padding:21px}
.gap-17{gap:5px}
.radius-17{border-radius:23px}
.op-17{opacity:0.47}
.shadow-lv-17{box-shadow:0 9px 33px rgba(0,0,0,0.32)}


.fx-18{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-18{padding:22px}
.gap-18{gap:6px}
.radius-18{border-radius:24px}
.op-18{opacity:0.48}
.shadow-lv-18{box-shadow:0 10px 34px rgba(0,0,0,0.33)}


.fx-19{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-19{padding:23px}
.gap-19{gap:7px}
.radius-19{border-radius:25px}
.op-19{opacity:0.49}
.shadow-lv-19{box-shadow:0 11px 35px rgba(0,0,0,0.34)}


.fx-20{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-20{padding:24px}
.gap-20{gap:8px}
.radius-20{border-radius:6px}
.op-20{opacity:0.50}
.shadow-lv-20{box-shadow:0 12px 36px rgba(0,0,0,0.35)}


.fx-21{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-21{padding:25px}
.gap-21{gap:9px}
.radius-21{border-radius:7px}
.op-21{opacity:0.51}
.shadow-lv-21{box-shadow:0 13px 37px rgba(0,0,0,0.36)}


.fx-22{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-22{padding:26px}
.gap-22{gap:10px}
.radius-22{border-radius:8px}
.op-22{opacity:0.52}
.shadow-lv-22{box-shadow:0 14px 38px rgba(0,0,0,0.37)}


.fx-23{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-23{padding:27px}
.gap-23{gap:11px}
.radius-23{border-radius:9px}
.op-23{opacity:0.53}
.shadow-lv-23{box-shadow:0 15px 39px rgba(0,0,0,0.38)}


.fx-24{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-24{padding:4px}
.gap-24{gap:12px}
.radius-24{border-radius:10px}
.op-24{opacity:0.54}
.shadow-lv-24{box-shadow:0 4px 40px rgba(0,0,0,0.39)}


.fx-25{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-25{padding:5px}
.gap-25{gap:13px}
.radius-25{border-radius:11px}
.op-25{opacity:0.55}
.shadow-lv-25{box-shadow:0 5px 41px rgba(0,0,0,0.40)}


.fx-26{transition:all .10s cubic-bezier(.4,0,.2,1)}
.pad-26{padding:6px}
.gap-26{gap:14px}
.radius-26{border-radius:12px}
.op-26{opacity:0.56}
.shadow-lv-26{box-shadow:0 6px 42px rgba(0,0,0,0.41)}


.fx-27{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-27{padding:7px}
.gap-27{gap:15px}
.radius-27{border-radius:13px}
.op-27{opacity:0.57}
.shadow-lv-27{box-shadow:0 7px 43px rgba(0,0,0,0.42)}


.fx-28{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-28{padding:8px}
.gap-28{gap:16px}
.radius-28{border-radius:14px}
.op-28{opacity:0.58}
.shadow-lv-28{box-shadow:0 8px 44px rgba(0,0,0,0.43)}


.fx-29{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-29{padding:9px}
.gap-29{gap:17px}
.radius-29{border-radius:15px}
.op-29{opacity:0.59}
.shadow-lv-29{box-shadow:0 9px 45px rgba(0,0,0,0.44)}


.fx-30{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-30{padding:10px}
.gap-30{gap:18px}
.radius-30{border-radius:16px}
.op-30{opacity:0.60}
.shadow-lv-30{box-shadow:0 10px 46px rgba(0,0,0,0.45)}


.fx-31{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-31{padding:11px}
.gap-31{gap:19px}
.radius-31{border-radius:17px}
.op-31{opacity:0.61}
.shadow-lv-31{box-shadow:0 11px 47px rgba(0,0,0,0.46)}


.fx-32{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-32{padding:12px}
.gap-32{gap:4px}
.radius-32{border-radius:18px}
.op-32{opacity:0.62}
.shadow-lv-32{box-shadow:0 12px 48px rgba(0,0,0,0.47)}


.fx-33{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-33{padding:13px}
.gap-33{gap:5px}
.radius-33{border-radius:19px}
.op-33{opacity:0.63}
.shadow-lv-33{box-shadow:0 13px 49px rgba(0,0,0,0.48)}


.fx-34{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-34{padding:14px}
.gap-34{gap:6px}
.radius-34{border-radius:20px}
.op-34{opacity:0.64}
.shadow-lv-34{box-shadow:0 14px 50px rgba(0,0,0,0.49)}


.fx-35{transition:all .10s cubic-bezier(.4,0,.2,1)}
.pad-35{padding:15px}
.gap-35{gap:7px}
.radius-35{border-radius:21px}
.op-35{opacity:0.65}
.shadow-lv-35{box-shadow:0 15px 51px rgba(0,0,0,0.50)}


.fx-36{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-36{padding:16px}
.gap-36{gap:8px}
.radius-36{border-radius:22px}
.op-36{opacity:0.66}
.shadow-lv-36{box-shadow:0 4px 52px rgba(0,0,0,0.51)}


.fx-37{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-37{padding:17px}
.gap-37{gap:9px}
.radius-37{border-radius:23px}
.op-37{opacity:0.67}
.shadow-lv-37{box-shadow:0 5px 53px rgba(0,0,0,0.52)}


.fx-38{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-38{padding:18px}
.gap-38{gap:10px}
.radius-38{border-radius:24px}
.op-38{opacity:0.68}
.shadow-lv-38{box-shadow:0 6px 54px rgba(0,0,0,0.53)}


.fx-39{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-39{padding:19px}
.gap-39{gap:11px}
.radius-39{border-radius:25px}
.op-39{opacity:0.69}
.shadow-lv-39{box-shadow:0 7px 55px rgba(0,0,0,0.54)}


.fx-40{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-40{padding:20px}
.gap-40{gap:12px}
.radius-40{border-radius:6px}
.op-40{opacity:0.70}
.shadow-lv-40{box-shadow:0 8px 16px rgba(0,0,0,0.15)}


.fx-41{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-41{padding:21px}
.gap-41{gap:13px}
.radius-41{border-radius:7px}
.op-41{opacity:0.71}
.shadow-lv-41{box-shadow:0 9px 17px rgba(0,0,0,0.16)}


.fx-42{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-42{padding:22px}
.gap-42{gap:14px}
.radius-42{border-radius:8px}
.op-42{opacity:0.72}
.shadow-lv-42{box-shadow:0 10px 18px rgba(0,0,0,0.17)}


.fx-43{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-43{padding:23px}
.gap-43{gap:15px}
.radius-43{border-radius:9px}
.op-43{opacity:0.73}
.shadow-lv-43{box-shadow:0 11px 19px rgba(0,0,0,0.18)}


.fx-44{transition:all .10s cubic-bezier(.4,0,.2,1)}
.pad-44{padding:24px}
.gap-44{gap:16px}
.radius-44{border-radius:10px}
.op-44{opacity:0.74}
.shadow-lv-44{box-shadow:0 12px 20px rgba(0,0,0,0.19)}


.fx-45{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-45{padding:25px}
.gap-45{gap:17px}
.radius-45{border-radius:11px}
.op-45{opacity:0.75}
.shadow-lv-45{box-shadow:0 13px 21px rgba(0,0,0,0.20)}


.fx-46{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-46{padding:26px}
.gap-46{gap:18px}
.radius-46{border-radius:12px}
.op-46{opacity:0.76}
.shadow-lv-46{box-shadow:0 14px 22px rgba(0,0,0,0.21)}


.fx-47{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-47{padding:27px}
.gap-47{gap:19px}
.radius-47{border-radius:13px}
.op-47{opacity:0.77}
.shadow-lv-47{box-shadow:0 15px 23px rgba(0,0,0,0.22)}


.fx-48{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-48{padding:4px}
.gap-48{gap:4px}
.radius-48{border-radius:14px}
.op-48{opacity:0.78}
.shadow-lv-48{box-shadow:0 4px 24px rgba(0,0,0,0.23)}


.fx-49{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-49{padding:5px}
.gap-49{gap:5px}
.radius-49{border-radius:15px}
.op-49{opacity:0.79}
.shadow-lv-49{box-shadow:0 5px 25px rgba(0,0,0,0.24)}


.fx-50{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-50{padding:6px}
.gap-50{gap:6px}
.radius-50{border-radius:16px}
.op-50{opacity:0.80}
.shadow-lv-50{box-shadow:0 6px 26px rgba(0,0,0,0.25)}


.fx-51{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-51{padding:7px}
.gap-51{gap:7px}
.radius-51{border-radius:17px}
.op-51{opacity:0.81}
.shadow-lv-51{box-shadow:0 7px 27px rgba(0,0,0,0.26)}


.fx-52{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-52{padding:8px}
.gap-52{gap:8px}
.radius-52{border-radius:18px}
.op-52{opacity:0.82}
.shadow-lv-52{box-shadow:0 8px 28px rgba(0,0,0,0.27)}


.fx-53{transition:all .10s cubic-bezier(.4,0,.2,1)}
.pad-53{padding:9px}
.gap-53{gap:9px}
.radius-53{border-radius:19px}
.op-53{opacity:0.83}
.shadow-lv-53{box-shadow:0 9px 29px rgba(0,0,0,0.28)}


.fx-54{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-54{padding:10px}
.gap-54{gap:10px}
.radius-54{border-radius:20px}
.op-54{opacity:0.84}
.shadow-lv-54{box-shadow:0 10px 30px rgba(0,0,0,0.29)}


.fx-55{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-55{padding:11px}
.gap-55{gap:11px}
.radius-55{border-radius:21px}
.op-55{opacity:0.85}
.shadow-lv-55{box-shadow:0 11px 31px rgba(0,0,0,0.30)}


.fx-56{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-56{padding:12px}
.gap-56{gap:12px}
.radius-56{border-radius:22px}
.op-56{opacity:0.86}
.shadow-lv-56{box-shadow:0 12px 32px rgba(0,0,0,0.31)}


.fx-57{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-57{padding:13px}
.gap-57{gap:13px}
.radius-57{border-radius:23px}
.op-57{opacity:0.87}
.shadow-lv-57{box-shadow:0 13px 33px rgba(0,0,0,0.32)}


.fx-58{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-58{padding:14px}
.gap-58{gap:14px}
.radius-58{border-radius:24px}
.op-58{opacity:0.88}
.shadow-lv-58{box-shadow:0 14px 34px rgba(0,0,0,0.33)}


.fx-59{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-59{padding:15px}
.gap-59{gap:15px}
.radius-59{border-radius:25px}
.op-59{opacity:0.89}
.shadow-lv-59{box-shadow:0 15px 35px rgba(0,0,0,0.34)}


.fx-60{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-60{padding:16px}
.gap-60{gap:16px}
.radius-60{border-radius:6px}
.op-60{opacity:0.90}
.shadow-lv-60{box-shadow:0 4px 36px rgba(0,0,0,0.35)}


.fx-61{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-61{padding:17px}
.gap-61{gap:17px}
.radius-61{border-radius:7px}
.op-61{opacity:0.91}
.shadow-lv-61{box-shadow:0 5px 37px rgba(0,0,0,0.36)}


.fx-62{transition:all .10s cubic-bezier(.4,0,.2,1)}
.pad-62{padding:18px}
.gap-62{gap:18px}
.radius-62{border-radius:8px}
.op-62{opacity:0.92}
.shadow-lv-62{box-shadow:0 6px 38px rgba(0,0,0,0.37)}


.fx-63{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-63{padding:19px}
.gap-63{gap:19px}
.radius-63{border-radius:9px}
.op-63{opacity:0.93}
.shadow-lv-63{box-shadow:0 7px 39px rgba(0,0,0,0.38)}


.fx-64{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-64{padding:20px}
.gap-64{gap:4px}
.radius-64{border-radius:10px}
.op-64{opacity:0.94}
.shadow-lv-64{box-shadow:0 8px 40px rgba(0,0,0,0.39)}


.fx-65{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-65{padding:21px}
.gap-65{gap:5px}
.radius-65{border-radius:11px}
.op-65{opacity:0.95}
.shadow-lv-65{box-shadow:0 9px 41px rgba(0,0,0,0.40)}


.fx-66{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-66{padding:22px}
.gap-66{gap:6px}
.radius-66{border-radius:12px}
.op-66{opacity:0.96}
.shadow-lv-66{box-shadow:0 10px 42px rgba(0,0,0,0.41)}


.fx-67{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-67{padding:23px}
.gap-67{gap:7px}
.radius-67{border-radius:13px}
.op-67{opacity:0.97}
.shadow-lv-67{box-shadow:0 11px 43px rgba(0,0,0,0.42)}


.fx-68{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-68{padding:24px}
.gap-68{gap:8px}
.radius-68{border-radius:14px}
.op-68{opacity:0.98}
.shadow-lv-68{box-shadow:0 12px 44px rgba(0,0,0,0.43)}


.fx-69{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-69{padding:25px}
.gap-69{gap:9px}
.radius-69{border-radius:15px}
.op-69{opacity:0.99}
.shadow-lv-69{box-shadow:0 13px 45px rgba(0,0,0,0.44)}


.fx-70{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-70{padding:26px}
.gap-70{gap:10px}
.radius-70{border-radius:16px}
.op-70{opacity:0.30}
.shadow-lv-70{box-shadow:0 14px 46px rgba(0,0,0,0.45)}


.fx-71{transition:all .10s cubic-bezier(.4,0,.2,1)}
.pad-71{padding:27px}
.gap-71{gap:11px}
.radius-71{border-radius:17px}
.op-71{opacity:0.31}
.shadow-lv-71{box-shadow:0 15px 47px rgba(0,0,0,0.46)}


.fx-72{transition:all .2s cubic-bezier(.4,0,.2,1)}
.pad-72{padding:4px}
.gap-72{gap:12px}
.radius-72{border-radius:18px}
.op-72{opacity:0.32}
.shadow-lv-72{box-shadow:0 4px 48px rgba(0,0,0,0.47)}


.fx-73{transition:all .3s cubic-bezier(.4,0,.2,1)}
.pad-73{padding:5px}
.gap-73{gap:13px}
.radius-73{border-radius:19px}
.op-73{opacity:0.33}
.shadow-lv-73{box-shadow:0 5px 49px rgba(0,0,0,0.48)}


.fx-74{transition:all .4s cubic-bezier(.4,0,.2,1)}
.pad-74{padding:6px}
.gap-74{gap:14px}
.radius-74{border-radius:20px}
.op-74{opacity:0.34}
.shadow-lv-74{box-shadow:0 6px 50px rgba(0,0,0,0.49)}


.fx-75{transition:all .5s cubic-bezier(.4,0,.2,1)}
.pad-75{padding:7px}
.gap-75{gap:15px}
.radius-75{border-radius:21px}
.op-75{opacity:0.35}
.shadow-lv-75{box-shadow:0 7px 51px rgba(0,0,0,0.50)}


.fx-76{transition:all .6s cubic-bezier(.4,0,.2,1)}
.pad-76{padding:8px}
.gap-76{gap:16px}
.radius-76{border-radius:22px}
.op-76{opacity:0.36}
.shadow-lv-76{box-shadow:0 8px 52px rgba(0,0,0,0.51)}


.fx-77{transition:all .7s cubic-bezier(.4,0,.2,1)}
.pad-77{padding:9px}
.gap-77{gap:17px}
.radius-77{border-radius:23px}
.op-77{opacity:0.37}
.shadow-lv-77{box-shadow:0 9px 53px rgba(0,0,0,0.52)}


.fx-78{transition:all .8s cubic-bezier(.4,0,.2,1)}
.pad-78{padding:10px}
.gap-78{gap:18px}
.radius-78{border-radius:24px}
.op-78{opacity:0.38}
.shadow-lv-78{box-shadow:0 10px 54px rgba(0,0,0,0.53)}


.fx-79{transition:all .9s cubic-bezier(.4,0,.2,1)}
.pad-79{padding:11px}
.gap-79{gap:19px}
.radius-79{border-radius:25px}
.op-79{opacity:0.39}
.shadow-lv-79{box-shadow:0 11px 55px rgba(0,0,0,0.54)}


/* ===== MOBILE FIX ===== */
@media (max-width: 960px) {
  .shell { grid-template-columns: 1fr !important; }
  .side {
    position: fixed !important;
    top: 0; bottom: 0; right: 0; left: auto !important;
    width: min(86vw, 280px) !important;
    transform: translateX(110%) !important;
    z-index: 60 !important;
    box-shadow: -12px 0 40px rgba(0,0,0,.45);
  }
  .side.open { transform: translateX(0) !important; }
  .side-backdrop { z-index: 55 !important; }
  .main { padding: 14px 12px 88px !important; width: 100% !important; max-width: 100% !important; }
  .topbar { position: sticky; top: 0; z-index: 20; background: var(--bg); padding: 8px 0 12px; }
  .kpis { grid-template-columns: 1fr 1fr !important; gap: 10px !important; }
  .grid-2 { grid-template-columns: 1fr !important; }
  table { font-size: .78rem; }
  th, td { padding: 10px 6px; }
  .modal { padding: 18px; border-radius: 18px; }
  .login-card { padding: 32px 22px; border-radius: 22px; }
  /* bottom navigation */
  .mob-nav {
    display: flex !important;
    position: fixed; bottom: 0; left: 0; right: 0;
    z-index: 50;
    background: var(--s2);
    border-top: 1px solid var(--bd);
    padding: 6px 4px calc(6px + env(safe-area-inset-bottom));
    justify-content: space-around;
    backdrop-filter: blur(14px);
  }
  .mob-nav button {
    flex: 1; background: transparent; border: none; color: var(--mu);
    font-family: inherit; font-size: .68rem; font-weight: 700;
    padding: 8px 2px; border-radius: 12px; cursor: pointer;
  }
  .mob-nav button.active { color: var(--pr3); background: rgba(99,102,241,.12); }
}
@media (min-width: 961px) {
  .mob-nav { display: none !important; }
}
</style></head><body>
<div id="login"><div class="login-card"><div class="brand-mark">LP</div><h1>LPRW Panel</h1><p class="sub">Leviko Panel Railway · ورود مدیر</p>
<div class="field"><label>نام کاربری</label><input id="user" autocomplete="username" placeholder="admin"></div>
<div class="field"><label>رمز عبور</label><input id="pw" type="password" autocomplete="current-password" placeholder="••••••"></div>
<button class="btn btn-p btn-block" id="btn-login">ورود به پنل</button>
<div class="err" id="lerr">نام کاربری یا رمز اشتباه است</div>
<div class="login-foot">پیش‌فرض: admin / 12345</div></div></div>
<div id="app">
<div class="side-backdrop" id="backdrop"></div>
<div class="shell">
<aside class="side" id="side">
<div class="logo"><div class="mk">LP</div><div><h2>LPRW</h2><small>Leviko Panel</small></div></div>
<div class="nav-item active" data-tab="dash">داشبورد</div>
<div class="nav-item" data-tab="links">لینک‌ها</div>
<div class="nav-item" data-tab="subs">سابسکریپشن</div>
<div class="nav-item" data-tab="online">اتصالات زنده</div>
<div class="nav-item" data-tab="logs">فعالیت‌ها</div>
<div class="nav-item" data-tab="settings">تنظیمات</div>
<div class="side-bottom"><button class="btn" id="btn-theme" type="button">حالت روز / شب</button><button class="btn btn-d" id="btn-out" type="button">خروج</button></div>
</aside>
<main class="main">
<div class="topbar"><div style="display:flex;align-items:center;gap:10px"><button class="burger" id="burger" type="button">☰</button><h1 id="page-title">داشبورد</h1></div>
<div class="acts"><button class="btn btn-p" id="btn-nl">+ لینک جدید</button><button class="btn" id="btn-ns">+ ساب</button></div></div>
<section id="tab-dash">
<div class="kpis">
<div class="kpi"><div class="t">لینک‌های فعال</div><div class="v" id="k-links">—</div><div class="s">کل لینک‌ها</div></div>
<div class="kpi"><div class="t">آنلاین</div><div class="v" id="k-online">—</div><div class="s">اتصالات همزمان</div></div>
<div class="kpi"><div class="t">ترافیک کل</div><div class="v" id="k-bytes">—</div><div class="s">مصرف تجمیعی</div></div>
<div class="kpi"><div class="t">ساب‌ها</div><div class="v" id="k-subs">—</div><div class="s">گروه‌های اشتراک</div></div>
</div>
<div class="grid-2">
<div class="panel"><div class="panel-h"><h3>ترافیک ساعتی</h3></div><div class="chart-box"><canvas id="chart"></canvas></div></div>
<div class="panel"><div class="panel-h"><h3>وضعیت سیستم</h3></div>
<div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--bd)"><span style="color:var(--mu)">آپ‌تایم</span><strong id="k-up">—</strong></div>
<div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--bd)"><span style="color:var(--mu)">هاست</span><strong id="k-host">—</strong></div>
<div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--bd)"><span style="color:var(--mu)">نسخه</span><strong>3.1 LPRW</strong></div>
<div style="display:flex;justify-content:space-between;padding:10px 0"><span style="color:var(--mu)">درخواست‌ها</span><strong id="k-req">—</strong></div>
</div></div>
</section>
<section id="tab-links" class="hidden"><div class="panel"><div class="panel-h"><h3>مدیریت لینک‌ها</h3><span class="chip" id="links-count">0</span></div>
<div style="overflow:auto"><table><thead><tr><th>نام</th><th>پروتکل</th><th>مصرف</th><th>حجم</th><th>وضعیت</th><th>عملیات</th></tr></thead><tbody id="links-tb"></tbody></table></div></div></section>
<section id="tab-subs" class="hidden"><div class="panel"><div class="panel-h"><h3>سابسکریپشن‌ها</h3></div>
<div style="overflow:auto"><table><thead><tr><th>نام</th><th>آدرس</th><th>حجم</th><th>عملیات</th></tr></thead><tbody id="subs-tb"></tbody></table></div></div></section>
<section id="tab-online" class="hidden"><div class="panel"><div class="panel-h"><h3>اتصالات زنده</h3></div><div id="online-grid"></div></div></section>
<section id="tab-logs" class="hidden"><div class="panel"><div class="panel-h"><h3>لاگ فعالیت</h3></div><ul id="act-list"></ul></div></section>
<section id="tab-settings" class="hidden"><div class="panel"><div class="panel-h"><h3>تنظیمات</h3></div>
<div class="field"><label>نام پنل</label><input id="st-name"></div>
<div class="field"><label>اعلان</label><input id="st-ann"></div>
<div class="field"><label>لینک پشتیبانی</label><input id="st-sup"></div>
<button class="btn btn-p" id="btn-save-st">ذخیره</button>
<hr style="border:none;border-top:1px solid var(--bd);margin:22px 0">
<h3 style="margin-bottom:12px">تغییر رمز</h3>
<div class="field"><label>رمز فعلی</label><input id="pw-cur" type="password"></div>
<div class="field"><label>رمز جدید</label><input id="pw-new" type="password"></div>
<button class="btn" id="btn-pw">بروزرسانی رمز</button>
</div></section>
</main></div></div>
<div class="modal-bg" id="m-link"><div class="modal"><h3>لینک جدید</h3>
<div class="field"><label>نام</label><input id="nl-n" placeholder="کاربر ۱"></div>
<div class="form-row"><div class="field"><label>پروتکل</label><select id="nl-p"><option value="vless">VLESS</option><option value="trojan">Trojan</option></select></div>
<div class="field"><label>حجم (GB) ۰=نامحدود</label><input id="nl-v" type="number" value="0" min="0" step="0.1"></div></div>
<div class="form-row"><div class="field"><label>روز ۰=نامحدود</label><input id="nl-d" type="number" value="0" min="0"></div>
<div class="field"><label>سقف اتصال همزمان</label><input id="nl-c" type="number" value="0" min="0"></div></div>
<div class="field"><label>یادداشت</label><input id="nl-r"></div>
<div style="display:flex;gap:8px;justify-content:flex-end"><button class="btn" onclick="closeM('m-link')">لغو</button><button class="btn btn-p" id="btn-cl">ساخت</button></div>
</div></div>
<div class="modal-bg" id="m-sub"><div class="modal"><h3>ساب جدید</h3>
<div class="field"><label>نام</label><input id="ns-n"></div>
<div class="field"><label>شناسه لینک‌ها (با کاما)</label><input id="ns-i" placeholder="uuid1,uuid2"></div>
<div class="form-row"><div class="field"><label>حجم GB</label><input id="ns-v" type="number" value="0"></div>
<div class="field"><label>روز</label><input id="ns-d" type="number" value="0"></div></div>
<div style="display:flex;gap:8px;justify-content:flex-end"><button class="btn" onclick="closeM('m-sub')">لغو</button><button class="btn btn-p" id="btn-cs">ساخت</button></div>
</div></div>

<div class="mob-nav" id="mob-nav">
  <button type="button" data-tab="dash" class="active">خانه</button>
  <button type="button" data-tab="links">لینک</button>
  <button type="button" data-tab="subs">ساب</button>
  <button type="button" data-tab="online">آنلاین</button>
  <button type="button" data-tab="settings">تنظیمات</button>
</div>

<div class="bottom-nav" id="bottom-nav">
<button type="button" data-tab="dash" class="active"><span>🏠</span>خانه</button>
<button type="button" data-tab="links"><span>🔗</span>لینک</button>
<button type="button" data-tab="subs"><span>📡</span>ساب</button>
<button type="button" data-tab="online"><span>🟢</span>آنلاین</button>
<button type="button" data-tab="settings"><span>⚙️</span>تنظیمات</button>
</div>
<div class="toast" id="toast"></div>
<script>
const $=s=>document.querySelector(s);const $$=s=>[...document.querySelectorAll(s)];let chart;
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2400)}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
async function api(url,opt={}){const o={credentials:'same-origin',...opt};if(o.body&&typeof o.body==='object'){o.headers={'Content-Type':'application/json',...(o.headers||{})};o.body=JSON.stringify(o.body)}const r=await fetch(url,o);if(r.status===401){showLogin();throw new Error('auth')}const j=await r.json().catch(()=>({}));if(!r.ok)throw new Error(j.detail||r.statusText);return j}
function showLogin(){$('#app').style.display='none';$('#login').style.display='flex'}
function showApp(){$('#login').style.display='none';$('#app').style.display='block';loadAll()}
function openM(id){$('#'+id).classList.add('show')}function closeM(id){$('#'+id).classList.remove('show')}
function copy(t){navigator.clipboard.writeText(t).then(()=>toast('کپی شد')).catch(()=>toast('کپی نشد'))}
function setTheme(t){document.documentElement.setAttribute('data-theme',t);localStorage.setItem('lprw_theme',t)}
setTheme(localStorage.getItem('lprw_theme')||'dark');
$('#btn-theme').onclick=()=>{const cur=document.documentElement.getAttribute('data-theme')==='light'?'dark':'light';setTheme(cur);toast(cur==='dark'?'حالت شب':'حالت روز')};
function goTab(tab){
  $$('.nav-item').forEach(x=>x.classList.toggle('active',x.dataset.tab===tab));
  $$('#bottom-nav button').forEach(x=>x.classList.toggle('active',x.dataset.tab===tab));
  ['dash','links','subs','online','logs','settings'].forEach(t=>{const el=$('#tab-'+t);if(el)el.classList.toggle('hidden',t!==tab)});
  const titles={dash:'داشبورد',links:'لینک‌ها',subs:'سابسکریپشن',online:'اتصالات زنده',logs:'فعالیت‌ها',settings:'تنظیمات'};
  $('#page-title').textContent=titles[tab]||'';
  if(tab==='links')loadLinks();if(tab==='subs')loadSubs();if(tab==='online')loadOnline();if(tab==='logs')loadAct();if(tab==='settings')loadSettings();
  $('#side')?.classList.remove('open');$('#backdrop')?.classList.remove('show');
  window.scrollTo({top:0,behavior:'smooth'});
}
$$('.nav-item').forEach(n=>n.onclick=()=>goTab(n.dataset.tab));
$$('#bottom-nav button').forEach(n=>n.onclick=()=>goTab(n.dataset.tab));
$('#burger').onclick=()=>{$('#side').classList.add('open');$('#backdrop').classList.add('show')};
$('#backdrop').onclick=()=>{$('#side').classList.remove('open');$('#backdrop').classList.remove('show')};
$('#btn-login').onclick=async()=>{try{await api('/api/login',{method:'POST',body:{username:$('#user').value.trim()||'admin',password:$('#pw').value}});showApp()}catch{$('#lerr').style.display='block'}};
$('#pw').onkeydown=e=>{if(e.key==='Enter')$('#btn-login').click()};
$('#user').onkeydown=e=>{if(e.key==='Enter')$('#pw').focus()};
$('#btn-out').onclick=async()=>{await api('/api/logout',{method:'POST'});showLogin()};
async function loadDash(){try{const s=await api('/api/stats');$('#k-links').textContent=s.links??0;$('#k-online').textContent=s.online??0;$('#k-bytes').textContent=s.bytes_h||s.bytes||'—';$('#k-subs').textContent=s.subs??0;$('#k-up').textContent=s.uptime_h||(s.uptime+'s');$('#k-host').textContent=s.host||location.host;$('#k-req').textContent=s.reqs??0;const labels=Object.keys(s.hourly||{});const data=Object.values(s.hourly||{});const ctx=$('#chart');if(chart)chart.destroy();chart=new Chart(ctx,{type:'line',data:{labels,datasets:[{label:'ترافیک',data,borderColor:'#818cf8',backgroundColor:'rgba(99,102,241,.15)',fill:true,tension:.35}]},options:{plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#8b93a8'}},y:{ticks:{color:'#8b93a8'}}},maintainAspectRatio:false}})}catch(e){}}
async function loadLinks(){const links=await api('/api/links');$('#links-count').textContent=links.length;$('#links-tb').innerHTML=links.map(l=>`<tr><td><strong>${esc(l.label)}</strong><div style="font-size:.7rem;color:var(--mu)">${esc(l.id).slice(0,8)}…</div></td><td>${esc((l.proto||'vless').toUpperCase())}</td><td>${esc(l.used_h)}</td><td>${esc(l.vol_h)}</td><td><span class="badge ${l.ok?'on':'off'}">${l.ok?'فعال':'غیرفعال'}</span></td><td style="white-space:nowrap"><button class="chip" data-copy="${esc(l.share)}">کپی</button> <button class="chip" data-sub="${esc(l.sub_url)}">ساب</button> <button class="chip" data-user="${esc(l.user_url)}">پنل کاربر</button> <button class="chip" data-rst="${esc(l.id)}">ریست</button> <button class="btn btn-d btn-sm" data-del="${esc(l.id)}">حذف</button></td></tr>`).join('')||'<tr><td colspan="6"><div class="empty">لینکی نیست</div></td></tr>';$('#links-tb').onclick=async e=>{const t=e.target.closest('[data-copy],[data-sub],[data-user],[data-rst],[data-del]');if(!t)return;if(t.dataset.copy)copy(t.dataset.copy);if(t.dataset.sub)copy(t.dataset.sub);if(t.dataset.user){copy(t.dataset.user);window.open(t.dataset.user,'_blank')}if(t.dataset.rst){await api('/api/links/'+t.dataset.rst,{method:'PATCH',body:{reset_usage:true}});toast('ریست شد');loadLinks()}if(t.dataset.del&&confirm('حذف شود؟')){await api('/api/links/'+t.dataset.del,{method:'DELETE'});loadLinks();loadDash()}}}
async function loadSubs(){const subs=await api('/api/subs');$('#subs-tb').innerHTML=subs.map(s=>`<tr><td><strong>${esc(s.name)}</strong></td><td><code style="font-size:.72rem;word-break:break-all">${esc(s.url)}</code> <button class="chip" data-copy="${esc(s.url)}">کپی</button></td><td>${esc(s.vol_h)}</td><td><button class="btn btn-d btn-sm" data-dels="${esc(s.id)}">حذف</button></td></tr>`).join('')||'<tr><td colspan="4"><div class="empty">سابی نیست</div></td></tr>';$('#subs-tb').onclick=async e=>{const t=e.target.closest('[data-copy],[data-dels]');if(!t)return;if(t.dataset.copy)copy(t.dataset.copy);if(t.dataset.dels&&confirm('حذف؟')){await api('/api/subs/'+t.dataset.dels,{method:'DELETE'});loadSubs()}}}
async function loadOnline(){const s=await api('/api/stats');const list=s.connections||[];$('#online-grid').innerHTML=list.length?list.map(c=>`<div class="conn-card"><div class="t">ID</div><div class="v">${esc(c.id)}</div><div class="t" style="margin-top:8px">UUID</div><div class="v">${esc(c.uuid)}</div><div class="t" style="margin-top:8px">مدت</div><div class="v">${esc(c.sec)} ث</div></div>`).join(''):'<div class="empty" style="grid-column:1/-1">اتصال فعالی نیست</div>'}
async function loadAct(){const list=await api('/api/activity');$('#act-list').innerHTML=list.map(a=>{const lv=a.level==='ok'?'ok':a.level==='warn'?'warn':'info';return `<li><span class="tm">${esc((a.t||'').slice(11,19))}</span><span class="dot dot-${lv}"></span><span>${esc(a.msg)}</span></li>`}).join('')||'<li style="color:var(--mu);padding:24px">خالی</li>'}
async function loadSettings(){try{const s=await api('/api/settings');$('#st-name').value=s.panel_name||'';$('#st-ann').value=s.announce||'';$('#st-sup').value=s.support_url||''}catch{}}
$('#btn-save-st').onclick=async()=>{await api('/api/settings',{method:'POST',body:{panel_name:$('#st-name').value,announce:$('#st-ann').value,support_url:$('#st-sup').value}});toast('ذخیره شد')};
$('#btn-pw').onclick=async()=>{try{await api('/api/password',{method:'POST',body:{current:$('#pw-cur').value,new_password:$('#pw-new').value}});toast('رمز عوض شد')}catch(e){toast(e.message||'خطا')}};
$('#btn-nl').onclick=()=>openM('m-link');$('#btn-ns').onclick=()=>openM('m-sub');
$('#btn-cl').onclick=async()=>{try{const r=await api('/api/links',{method:'POST',body:{label:$('#nl-n').value.trim()||'Link',proto:$('#nl-p').value,volume_gb:+$('#nl-v').value||0,days:+$('#nl-d').value||0,max_conn:+$('#nl-c').value||0,remark:$('#nl-r').value||''}});closeM('m-link');toast('ساخته شد');if(r.link?.share)copy(r.link.share);loadLinks();loadDash()}catch(e){toast(e.message)}};
$('#btn-cs').onclick=async()=>{try{const ids=$('#ns-i').value.split(',').map(x=>x.trim()).filter(Boolean);const r=await api('/api/subs',{method:'POST',body:{name:$('#ns-n').value.trim()||'Sub',volume_gb:+$('#ns-v').value||0,days:+$('#ns-d').value||0,link_ids:ids}});closeM('m-sub');toast('ساب ساخته شد');copy(r.url);loadSubs()}catch(e){toast(e.message)}};
async function loadAll(){await loadDash();try{await api('/api/me')}catch{showLogin();return}}
(async()=>{try{await api('/api/me');showApp()}catch{showLogin()}})();

// mobile bottom nav
$$('#mob-nav button').forEach(b=>b.onclick=()=>{
  const tab=b.dataset.tab;
  const nav=$$('.nav-item').find(n=>n.dataset.tab===tab);
  if(nav) nav.click();
  $$('#mob-nav button').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
});

setInterval(()=>{if($('#app').style.display==='block')loadDash()},15000);
</script></body></html>
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
<div class="top"><div class="brand"><div class="mk">LP</div><div><h1>LPRW User</h1><small>پنل مصرف اختصاصی</small></div></div>
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
<div class="card"><h3>🔗 کانفیگ شما</h3>
<div class="share-box" id="share">{{SHARE}}</div>
<div class="actions"><button class="btn btn-p" id="copy">کپی کانفیگ</button>
<button class="btn" id="copy-sub">کپی لینک ساب</button>
<a class="btn" href="{{SUB}}" target="_blank">باز کردن ساب</a></div>
<p style="margin-top:12px;font-size:.8rem;color:var(--mu)">لینک اشتراک: <code style="color:var(--pr)">{{SUB}}</code></p></div>
<div class="card"><h3>📱 دانلود کلاینت</h3><div class="cli-grid">
<a class="cli" href="https://github.com/2dust/v2rayNG/releases" target="_blank" rel="noopener"><div class="cli-n">v2rayNG</div><div class="cli-p">Android</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://github.com/2dust/v2rayN/releases" target="_blank" rel="noopener"><div class="cli-n">v2rayN</div><div class="cli-p">Windows</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://github.com/hiddify/hiddify-app/releases" target="_blank" rel="noopener"><div class="cli-n">Hiddify</div><div class="cli-p">All</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://apps.apple.com/app/streisand/id6450534064" target="_blank" rel="noopener"><div class="cli-n">Streisand</div><div class="cli-p">iOS</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://apps.apple.com/app/v2box-v2ray-client/id6446814690" target="_blank" rel="noopener"><div class="cli-n">V2Box</div><div class="cli-p">iOS</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://github.com/MatsuriDayo/NekoBoxForAndroid/releases" target="_blank" rel="noopener"><div class="cli-n">NekoBox</div><div class="cli-p">Android</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://github.com/MetaCubeX/ClashMetaForAndroid/releases" target="_blank" rel="noopener"><div class="cli-n">Clash Meta</div><div class="cli-p">Desktop</div><div class="cli-a">دانلود</div></a>
<a class="cli" href="https://apps.apple.com/app/foxray/id6448898396" target="_blank" rel="noopener"><div class="cli-n">FoXray</div><div class="cli-p">iOS</div><div class="cli-a">دانلود</div></a>
</div></div>
<div class="card"><h3>📘 راهنمای اتصال</h3>
<div class="steps">
<div class="s"><div class="n">1</div><div>یکی از کلاینت‌های بالا را نصب کنید.</div></div>
<div class="s"><div class="n">2</div><div>دکمه «کپی کانفیگ» را بزنید یا از QR استفاده کنید.</div></div>
<div class="s"><div class="n">3</div><div>در کلاینت: Import from clipboard / افزودن از کلیپ‌بورد.</div></div>
<div class="s"><div class="n">4</div><div>برای چند دستگاه از لینک سابسکریپشن استفاده کنید.</div></div>
</div></div>
<div class="card"><h3>🧩 آموزش کلاینت‌ها</h3>
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
<div class="card"><h3>ℹ️ جزئیات</h3>
<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bd)"><span style="color:var(--mu)">هاست</span><strong>{{HOST}}</strong></div>
<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bd)"><span style="color:var(--mu)">نسخه</span><strong>{{VERSION}}</strong></div>
<div style="display:flex;justify-content:space-between;padding:8px 0"><span style="color:var(--mu)">یادداشت</span><strong>{{REMARK}}</strong></div>
</div>
<div class="card"><h3>💡 نکات سرعت</h3>
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
document.getElementById('copy').onclick=()=>navigator.clipboard.writeText(document.getElementById('share').textContent).then(()=>toast('کانفیگ کپی شد'));
document.getElementById('copy-sub').onclick=()=>navigator.clipboard.writeText('{{SUB}}').then(()=>toast('لینک ساب کپی شد'));
</script></body></html>
'''

DESIGN_NOTES = r"""

/* LPRW DESIGN SYSTEM */
/* token-0: spacing=4 radius=6 shadow=1 hue=0 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-1: spacing=5 radius=7 shadow=2 hue=1 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-2: spacing=6 radius=8 shadow=3 hue=2 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-3: spacing=7 radius=9 shadow=4 hue=3 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-4: spacing=8 radius=10 shadow=5 hue=4 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-5: spacing=9 radius=11 shadow=6 hue=5 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-6: spacing=10 radius=12 shadow=7 hue=6 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-7: spacing=11 radius=13 shadow=8 hue=7 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-8: spacing=12 radius=14 shadow=1 hue=8 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-9: spacing=13 radius=15 shadow=2 hue=9 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-10: spacing=14 radius=16 shadow=3 hue=10 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-11: spacing=15 radius=17 shadow=4 hue=11 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-12: spacing=16 radius=18 shadow=5 hue=12 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-13: spacing=17 radius=19 shadow=6 hue=13 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-14: spacing=18 radius=20 shadow=7 hue=14 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-15: spacing=19 radius=21 shadow=8 hue=15 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-16: spacing=20 radius=6 shadow=1 hue=16 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-17: spacing=21 radius=7 shadow=2 hue=17 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-18: spacing=22 radius=8 shadow=3 hue=18 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-19: spacing=23 radius=9 shadow=4 hue=19 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-20: spacing=24 radius=10 shadow=5 hue=20 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-21: spacing=25 radius=11 shadow=6 hue=21 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-22: spacing=26 radius=12 shadow=7 hue=22 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-23: spacing=27 radius=13 shadow=8 hue=23 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-24: spacing=4 radius=14 shadow=1 hue=24 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-25: spacing=5 radius=15 shadow=2 hue=25 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-26: spacing=6 radius=16 shadow=3 hue=26 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-27: spacing=7 radius=17 shadow=4 hue=27 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-28: spacing=8 radius=18 shadow=5 hue=28 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-29: spacing=9 radius=19 shadow=6 hue=29 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-30: spacing=10 radius=20 shadow=7 hue=30 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-31: spacing=11 radius=21 shadow=8 hue=31 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-32: spacing=12 radius=6 shadow=1 hue=32 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-33: spacing=13 radius=7 shadow=2 hue=33 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-34: spacing=14 radius=8 shadow=3 hue=34 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-35: spacing=15 radius=9 shadow=4 hue=35 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-36: spacing=16 radius=10 shadow=5 hue=36 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-37: spacing=17 radius=11 shadow=6 hue=37 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-38: spacing=18 radius=12 shadow=7 hue=38 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-39: spacing=19 radius=13 shadow=8 hue=39 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-40: spacing=20 radius=14 shadow=1 hue=40 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-41: spacing=21 radius=15 shadow=2 hue=41 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-42: spacing=22 radius=16 shadow=3 hue=42 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-43: spacing=23 radius=17 shadow=4 hue=43 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-44: spacing=24 radius=18 shadow=5 hue=44 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-45: spacing=25 radius=19 shadow=6 hue=45 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-46: spacing=26 radius=20 shadow=7 hue=46 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-47: spacing=27 radius=21 shadow=8 hue=47 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-48: spacing=4 radius=6 shadow=1 hue=48 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-49: spacing=5 radius=7 shadow=2 hue=49 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-50: spacing=6 radius=8 shadow=3 hue=50 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-51: spacing=7 radius=9 shadow=4 hue=51 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-52: spacing=8 radius=10 shadow=5 hue=52 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-53: spacing=9 radius=11 shadow=6 hue=53 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-54: spacing=10 radius=12 shadow=7 hue=54 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-55: spacing=11 radius=13 shadow=8 hue=55 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-56: spacing=12 radius=14 shadow=1 hue=56 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-57: spacing=13 radius=15 shadow=2 hue=57 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-58: spacing=14 radius=16 shadow=3 hue=58 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-59: spacing=15 radius=17 shadow=4 hue=59 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-60: spacing=16 radius=18 shadow=5 hue=60 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-61: spacing=17 radius=19 shadow=6 hue=61 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-62: spacing=18 radius=20 shadow=7 hue=62 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-63: spacing=19 radius=21 shadow=8 hue=63 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-64: spacing=20 radius=6 shadow=1 hue=64 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-65: spacing=21 radius=7 shadow=2 hue=65 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-66: spacing=22 radius=8 shadow=3 hue=66 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-67: spacing=23 radius=9 shadow=4 hue=67 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-68: spacing=24 radius=10 shadow=5 hue=68 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-69: spacing=25 radius=11 shadow=6 hue=69 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-70: spacing=26 radius=12 shadow=7 hue=70 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-71: spacing=27 radius=13 shadow=8 hue=71 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-72: spacing=4 radius=14 shadow=1 hue=72 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-73: spacing=5 radius=15 shadow=2 hue=73 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-74: spacing=6 radius=16 shadow=3 hue=74 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-75: spacing=7 radius=17 shadow=4 hue=75 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-76: spacing=8 radius=18 shadow=5 hue=76 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-77: spacing=9 radius=19 shadow=6 hue=77 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-78: spacing=10 radius=20 shadow=7 hue=78 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-79: spacing=11 radius=21 shadow=8 hue=79 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-80: spacing=12 radius=6 shadow=1 hue=80 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-81: spacing=13 radius=7 shadow=2 hue=81 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-82: spacing=14 radius=8 shadow=3 hue=82 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-83: spacing=15 radius=9 shadow=4 hue=83 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-84: spacing=16 radius=10 shadow=5 hue=84 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-85: spacing=17 radius=11 shadow=6 hue=85 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-86: spacing=18 radius=12 shadow=7 hue=86 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-87: spacing=19 radius=13 shadow=8 hue=87 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-88: spacing=20 radius=14 shadow=1 hue=88 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-89: spacing=21 radius=15 shadow=2 hue=89 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-90: spacing=22 radius=16 shadow=3 hue=90 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-91: spacing=23 radius=17 shadow=4 hue=91 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-92: spacing=24 radius=18 shadow=5 hue=92 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-93: spacing=25 radius=19 shadow=6 hue=93 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-94: spacing=26 radius=20 shadow=7 hue=94 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-95: spacing=27 radius=21 shadow=8 hue=95 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-96: spacing=4 radius=6 shadow=1 hue=96 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-97: spacing=5 radius=7 shadow=2 hue=97 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-98: spacing=6 radius=8 shadow=3 hue=98 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-99: spacing=7 radius=9 shadow=4 hue=99 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-100: spacing=8 radius=10 shadow=5 hue=100 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-101: spacing=9 radius=11 shadow=6 hue=101 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-102: spacing=10 radius=12 shadow=7 hue=102 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-103: spacing=11 radius=13 shadow=8 hue=103 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-104: spacing=12 radius=14 shadow=1 hue=104 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-105: spacing=13 radius=15 shadow=2 hue=105 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-106: spacing=14 radius=16 shadow=3 hue=106 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-107: spacing=15 radius=17 shadow=4 hue=107 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-108: spacing=16 radius=18 shadow=5 hue=108 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-109: spacing=17 radius=19 shadow=6 hue=109 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-110: spacing=18 radius=20 shadow=7 hue=110 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-111: spacing=19 radius=21 shadow=8 hue=111 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-112: spacing=20 radius=6 shadow=1 hue=112 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-113: spacing=21 radius=7 shadow=2 hue=113 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-114: spacing=22 radius=8 shadow=3 hue=114 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-115: spacing=23 radius=9 shadow=4 hue=115 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-116: spacing=24 radius=10 shadow=5 hue=116 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-117: spacing=25 radius=11 shadow=6 hue=117 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-118: spacing=26 radius=12 shadow=7 hue=118 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-119: spacing=27 radius=13 shadow=8 hue=119 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-120: spacing=4 radius=14 shadow=1 hue=120 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-121: spacing=5 radius=15 shadow=2 hue=121 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-122: spacing=6 radius=16 shadow=3 hue=122 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-123: spacing=7 radius=17 shadow=4 hue=123 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-124: spacing=8 radius=18 shadow=5 hue=124 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-125: spacing=9 radius=19 shadow=6 hue=125 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-126: spacing=10 radius=20 shadow=7 hue=126 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-127: spacing=11 radius=21 shadow=8 hue=127 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-128: spacing=12 radius=6 shadow=1 hue=128 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-129: spacing=13 radius=7 shadow=2 hue=129 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-130: spacing=14 radius=8 shadow=3 hue=130 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-131: spacing=15 radius=9 shadow=4 hue=131 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-132: spacing=16 radius=10 shadow=5 hue=132 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-133: spacing=17 radius=11 shadow=6 hue=133 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-134: spacing=18 radius=12 shadow=7 hue=134 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-135: spacing=19 radius=13 shadow=8 hue=135 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-136: spacing=20 radius=14 shadow=1 hue=136 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-137: spacing=21 radius=15 shadow=2 hue=137 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-138: spacing=22 radius=16 shadow=3 hue=138 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-139: spacing=23 radius=17 shadow=4 hue=139 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-140: spacing=24 radius=18 shadow=5 hue=140 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-141: spacing=25 radius=19 shadow=6 hue=141 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-142: spacing=26 radius=20 shadow=7 hue=142 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-143: spacing=27 radius=21 shadow=8 hue=143 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-144: spacing=4 radius=6 shadow=1 hue=144 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-145: spacing=5 radius=7 shadow=2 hue=145 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-146: spacing=6 radius=8 shadow=3 hue=146 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-147: spacing=7 radius=9 shadow=4 hue=147 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-148: spacing=8 radius=10 shadow=5 hue=148 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-149: spacing=9 radius=11 shadow=6 hue=149 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-150: spacing=10 radius=12 shadow=7 hue=150 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-151: spacing=11 radius=13 shadow=8 hue=151 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-152: spacing=12 radius=14 shadow=1 hue=152 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-153: spacing=13 radius=15 shadow=2 hue=153 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-154: spacing=14 radius=16 shadow=3 hue=154 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-155: spacing=15 radius=17 shadow=4 hue=155 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-156: spacing=16 radius=18 shadow=5 hue=156 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-157: spacing=17 radius=19 shadow=6 hue=157 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-158: spacing=18 radius=20 shadow=7 hue=158 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-159: spacing=19 radius=21 shadow=8 hue=159 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-160: spacing=20 radius=6 shadow=1 hue=160 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-161: spacing=21 radius=7 shadow=2 hue=161 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-162: spacing=22 radius=8 shadow=3 hue=162 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-163: spacing=23 radius=9 shadow=4 hue=163 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-164: spacing=24 radius=10 shadow=5 hue=164 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-165: spacing=25 radius=11 shadow=6 hue=165 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-166: spacing=26 radius=12 shadow=7 hue=166 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-167: spacing=27 radius=13 shadow=8 hue=167 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-168: spacing=4 radius=14 shadow=1 hue=168 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-169: spacing=5 radius=15 shadow=2 hue=169 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-170: spacing=6 radius=16 shadow=3 hue=170 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-171: spacing=7 radius=17 shadow=4 hue=171 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-172: spacing=8 radius=18 shadow=5 hue=172 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-173: spacing=9 radius=19 shadow=6 hue=173 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-174: spacing=10 radius=20 shadow=7 hue=174 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-175: spacing=11 radius=21 shadow=8 hue=175 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-176: spacing=12 radius=6 shadow=1 hue=176 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-177: spacing=13 radius=7 shadow=2 hue=177 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-178: spacing=14 radius=8 shadow=3 hue=178 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-179: spacing=15 radius=9 shadow=4 hue=179 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-180: spacing=16 radius=10 shadow=5 hue=180 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-181: spacing=17 radius=11 shadow=6 hue=181 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-182: spacing=18 radius=12 shadow=7 hue=182 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-183: spacing=19 radius=13 shadow=8 hue=183 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-184: spacing=20 radius=14 shadow=1 hue=184 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-185: spacing=21 radius=15 shadow=2 hue=185 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-186: spacing=22 radius=16 shadow=3 hue=186 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-187: spacing=23 radius=17 shadow=4 hue=187 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-188: spacing=24 radius=18 shadow=5 hue=188 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-189: spacing=25 radius=19 shadow=6 hue=189 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-190: spacing=26 radius=20 shadow=7 hue=190 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-191: spacing=27 radius=21 shadow=8 hue=191 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-192: spacing=4 radius=6 shadow=1 hue=192 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-193: spacing=5 radius=7 shadow=2 hue=193 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-194: spacing=6 radius=8 shadow=3 hue=194 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-195: spacing=7 radius=9 shadow=4 hue=195 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-196: spacing=8 radius=10 shadow=5 hue=196 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-197: spacing=9 radius=11 shadow=6 hue=197 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-198: spacing=10 radius=12 shadow=7 hue=198 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-199: spacing=11 radius=13 shadow=8 hue=199 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-200: spacing=12 radius=14 shadow=1 hue=200 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-201: spacing=13 radius=15 shadow=2 hue=201 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-202: spacing=14 radius=16 shadow=3 hue=202 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-203: spacing=15 radius=17 shadow=4 hue=203 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-204: spacing=16 radius=18 shadow=5 hue=204 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-205: spacing=17 radius=19 shadow=6 hue=205 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-206: spacing=18 radius=20 shadow=7 hue=206 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-207: spacing=19 radius=21 shadow=8 hue=207 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-208: spacing=20 radius=6 shadow=1 hue=208 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-209: spacing=21 radius=7 shadow=2 hue=209 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-210: spacing=22 radius=8 shadow=3 hue=210 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-211: spacing=23 radius=9 shadow=4 hue=211 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-212: spacing=24 radius=10 shadow=5 hue=212 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-213: spacing=25 radius=11 shadow=6 hue=213 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-214: spacing=26 radius=12 shadow=7 hue=214 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-215: spacing=27 radius=13 shadow=8 hue=215 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-216: spacing=4 radius=14 shadow=1 hue=216 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-217: spacing=5 radius=15 shadow=2 hue=217 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-218: spacing=6 radius=16 shadow=3 hue=218 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-219: spacing=7 radius=17 shadow=4 hue=219 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-220: spacing=8 radius=18 shadow=5 hue=220 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-221: spacing=9 radius=19 shadow=6 hue=221 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-222: spacing=10 radius=20 shadow=7 hue=222 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-223: spacing=11 radius=21 shadow=8 hue=223 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-224: spacing=12 radius=6 shadow=1 hue=224 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-225: spacing=13 radius=7 shadow=2 hue=225 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-226: spacing=14 radius=8 shadow=3 hue=226 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-227: spacing=15 radius=9 shadow=4 hue=227 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-228: spacing=16 radius=10 shadow=5 hue=228 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-229: spacing=17 radius=11 shadow=6 hue=229 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-230: spacing=18 radius=12 shadow=7 hue=230 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-231: spacing=19 radius=13 shadow=8 hue=231 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-232: spacing=20 radius=14 shadow=1 hue=232 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-233: spacing=21 radius=15 shadow=2 hue=233 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-234: spacing=22 radius=16 shadow=3 hue=234 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-235: spacing=23 radius=17 shadow=4 hue=235 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-236: spacing=24 radius=18 shadow=5 hue=236 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-237: spacing=25 radius=19 shadow=6 hue=237 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-238: spacing=26 radius=20 shadow=7 hue=238 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-239: spacing=27 radius=21 shadow=8 hue=239 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-240: spacing=4 radius=6 shadow=1 hue=240 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-241: spacing=5 radius=7 shadow=2 hue=241 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-242: spacing=6 radius=8 shadow=3 hue=242 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-243: spacing=7 radius=9 shadow=4 hue=243 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-244: spacing=8 radius=10 shadow=5 hue=244 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-245: spacing=9 radius=11 shadow=6 hue=245 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-246: spacing=10 radius=12 shadow=7 hue=246 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-247: spacing=11 radius=13 shadow=8 hue=247 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-248: spacing=12 radius=14 shadow=1 hue=248 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-249: spacing=13 radius=15 shadow=2 hue=249 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-250: spacing=14 radius=16 shadow=3 hue=250 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-251: spacing=15 radius=17 shadow=4 hue=251 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-252: spacing=16 radius=18 shadow=5 hue=252 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-253: spacing=17 radius=19 shadow=6 hue=253 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-254: spacing=18 radius=20 shadow=7 hue=254 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-255: spacing=19 radius=21 shadow=8 hue=255 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-256: spacing=20 radius=6 shadow=1 hue=256 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-257: spacing=21 radius=7 shadow=2 hue=257 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-258: spacing=22 radius=8 shadow=3 hue=258 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-259: spacing=23 radius=9 shadow=4 hue=259 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-260: spacing=24 radius=10 shadow=5 hue=260 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-261: spacing=25 radius=11 shadow=6 hue=261 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-262: spacing=26 radius=12 shadow=7 hue=262 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-263: spacing=27 radius=13 shadow=8 hue=263 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-264: spacing=4 radius=14 shadow=1 hue=264 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-265: spacing=5 radius=15 shadow=2 hue=265 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-266: spacing=6 radius=16 shadow=3 hue=266 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-267: spacing=7 radius=17 shadow=4 hue=267 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-268: spacing=8 radius=18 shadow=5 hue=268 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-269: spacing=9 radius=19 shadow=6 hue=269 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-270: spacing=10 radius=20 shadow=7 hue=270 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-271: spacing=11 radius=21 shadow=8 hue=271 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-272: spacing=12 radius=6 shadow=1 hue=272 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-273: spacing=13 radius=7 shadow=2 hue=273 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-274: spacing=14 radius=8 shadow=3 hue=274 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-275: spacing=15 radius=9 shadow=4 hue=275 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-276: spacing=16 radius=10 shadow=5 hue=276 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-277: spacing=17 radius=11 shadow=6 hue=277 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-278: spacing=18 radius=12 shadow=7 hue=278 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-279: spacing=19 radius=13 shadow=8 hue=279 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-280: spacing=20 radius=14 shadow=1 hue=280 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-281: spacing=21 radius=15 shadow=2 hue=281 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-282: spacing=22 radius=16 shadow=3 hue=282 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-283: spacing=23 radius=17 shadow=4 hue=283 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-284: spacing=24 radius=18 shadow=5 hue=284 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-285: spacing=25 radius=19 shadow=6 hue=285 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-286: spacing=26 radius=20 shadow=7 hue=286 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-287: spacing=27 radius=21 shadow=8 hue=287 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-288: spacing=4 radius=6 shadow=1 hue=288 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-289: spacing=5 radius=7 shadow=2 hue=289 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-290: spacing=6 radius=8 shadow=3 hue=290 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-291: spacing=7 radius=9 shadow=4 hue=291 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-292: spacing=8 radius=10 shadow=5 hue=292 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-293: spacing=9 radius=11 shadow=6 hue=293 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-294: spacing=10 radius=12 shadow=7 hue=294 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-295: spacing=11 radius=13 shadow=8 hue=295 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-296: spacing=12 radius=14 shadow=1 hue=296 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-297: spacing=13 radius=15 shadow=2 hue=297 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-298: spacing=14 radius=16 shadow=3 hue=298 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-299: spacing=15 radius=17 shadow=4 hue=299 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-300: spacing=16 radius=18 shadow=5 hue=300 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-301: spacing=17 radius=19 shadow=6 hue=301 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-302: spacing=18 radius=20 shadow=7 hue=302 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-303: spacing=19 radius=21 shadow=8 hue=303 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-304: spacing=20 radius=6 shadow=1 hue=304 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-305: spacing=21 radius=7 shadow=2 hue=305 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-306: spacing=22 radius=8 shadow=3 hue=306 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-307: spacing=23 radius=9 shadow=4 hue=307 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-308: spacing=24 radius=10 shadow=5 hue=308 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-309: spacing=25 radius=11 shadow=6 hue=309 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-310: spacing=26 radius=12 shadow=7 hue=310 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-311: spacing=27 radius=13 shadow=8 hue=311 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-312: spacing=4 radius=14 shadow=1 hue=312 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-313: spacing=5 radius=15 shadow=2 hue=313 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-314: spacing=6 radius=16 shadow=3 hue=314 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-315: spacing=7 radius=17 shadow=4 hue=315 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-316: spacing=8 radius=18 shadow=5 hue=316 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-317: spacing=9 radius=19 shadow=6 hue=317 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-318: spacing=10 radius=20 shadow=7 hue=318 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-319: spacing=11 radius=21 shadow=8 hue=319 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-320: spacing=12 radius=6 shadow=1 hue=320 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-321: spacing=13 radius=7 shadow=2 hue=321 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-322: spacing=14 radius=8 shadow=3 hue=322 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-323: spacing=15 radius=9 shadow=4 hue=323 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-324: spacing=16 radius=10 shadow=5 hue=324 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-325: spacing=17 radius=11 shadow=6 hue=325 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-326: spacing=18 radius=12 shadow=7 hue=326 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-327: spacing=19 radius=13 shadow=8 hue=327 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-328: spacing=20 radius=14 shadow=1 hue=328 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-329: spacing=21 radius=15 shadow=2 hue=329 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-330: spacing=22 radius=16 shadow=3 hue=330 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-331: spacing=23 radius=17 shadow=4 hue=331 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-332: spacing=24 radius=18 shadow=5 hue=332 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-333: spacing=25 radius=19 shadow=6 hue=333 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-334: spacing=26 radius=20 shadow=7 hue=334 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-335: spacing=27 radius=21 shadow=8 hue=335 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-336: spacing=4 radius=6 shadow=1 hue=336 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-337: spacing=5 radius=7 shadow=2 hue=337 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-338: spacing=6 radius=8 shadow=3 hue=338 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-339: spacing=7 radius=9 shadow=4 hue=339 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-340: spacing=8 radius=10 shadow=5 hue=340 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-341: spacing=9 radius=11 shadow=6 hue=341 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-342: spacing=10 radius=12 shadow=7 hue=342 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-343: spacing=11 radius=13 shadow=8 hue=343 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-344: spacing=12 radius=14 shadow=1 hue=344 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-345: spacing=13 radius=15 shadow=2 hue=345 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-346: spacing=14 radius=16 shadow=3 hue=346 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-347: spacing=15 radius=17 shadow=4 hue=347 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-348: spacing=16 radius=18 shadow=5 hue=348 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-349: spacing=17 radius=19 shadow=6 hue=349 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-350: spacing=18 radius=20 shadow=7 hue=350 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-351: spacing=19 radius=21 shadow=8 hue=351 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-352: spacing=20 radius=6 shadow=1 hue=352 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-353: spacing=21 radius=7 shadow=2 hue=353 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-354: spacing=22 radius=8 shadow=3 hue=354 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-355: spacing=23 radius=9 shadow=4 hue=355 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-356: spacing=24 radius=10 shadow=5 hue=356 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-357: spacing=25 radius=11 shadow=6 hue=357 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-358: spacing=26 radius=12 shadow=7 hue=358 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-359: spacing=27 radius=13 shadow=8 hue=359 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-360: spacing=4 radius=14 shadow=1 hue=0 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-361: spacing=5 radius=15 shadow=2 hue=1 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-362: spacing=6 radius=16 shadow=3 hue=2 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-363: spacing=7 radius=17 shadow=4 hue=3 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-364: spacing=8 radius=18 shadow=5 hue=4 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-365: spacing=9 radius=19 shadow=6 hue=5 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-366: spacing=10 radius=20 shadow=7 hue=6 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-367: spacing=11 radius=21 shadow=8 hue=7 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-368: spacing=12 radius=6 shadow=1 hue=8 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-369: spacing=13 radius=7 shadow=2 hue=9 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-370: spacing=14 radius=8 shadow=3 hue=10 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-371: spacing=15 radius=9 shadow=4 hue=11 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-372: spacing=16 radius=10 shadow=5 hue=12 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-373: spacing=17 radius=11 shadow=6 hue=13 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-374: spacing=18 radius=12 shadow=7 hue=14 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-375: spacing=19 radius=13 shadow=8 hue=15 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-376: spacing=20 radius=14 shadow=1 hue=16 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-377: spacing=21 radius=15 shadow=2 hue=17 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-378: spacing=22 radius=16 shadow=3 hue=18 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-379: spacing=23 radius=17 shadow=4 hue=19 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-380: spacing=24 radius=18 shadow=5 hue=20 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-381: spacing=25 radius=19 shadow=6 hue=21 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-382: spacing=26 radius=20 shadow=7 hue=22 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-383: spacing=27 radius=21 shadow=8 hue=23 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-384: spacing=4 radius=6 shadow=1 hue=24 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-385: spacing=5 radius=7 shadow=2 hue=25 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-386: spacing=6 radius=8 shadow=3 hue=26 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-387: spacing=7 radius=9 shadow=4 hue=27 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-388: spacing=8 radius=10 shadow=5 hue=28 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-389: spacing=9 radius=11 shadow=6 hue=29 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-390: spacing=10 radius=12 shadow=7 hue=30 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-391: spacing=11 radius=13 shadow=8 hue=31 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-392: spacing=12 radius=14 shadow=1 hue=32 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-393: spacing=13 radius=15 shadow=2 hue=33 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-394: spacing=14 radius=16 shadow=3 hue=34 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-395: spacing=15 radius=17 shadow=4 hue=35 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-396: spacing=16 radius=18 shadow=5 hue=36 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-397: spacing=17 radius=19 shadow=6 hue=37 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-398: spacing=18 radius=20 shadow=7 hue=38 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-399: spacing=19 radius=21 shadow=8 hue=39 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-400: spacing=20 radius=6 shadow=1 hue=40 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-401: spacing=21 radius=7 shadow=2 hue=41 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-402: spacing=22 radius=8 shadow=3 hue=42 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-403: spacing=23 radius=9 shadow=4 hue=43 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-404: spacing=24 radius=10 shadow=5 hue=44 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-405: spacing=25 radius=11 shadow=6 hue=45 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-406: spacing=26 radius=12 shadow=7 hue=46 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-407: spacing=27 radius=13 shadow=8 hue=47 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-408: spacing=4 radius=14 shadow=1 hue=48 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-409: spacing=5 radius=15 shadow=2 hue=49 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-410: spacing=6 radius=16 shadow=3 hue=50 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-411: spacing=7 radius=17 shadow=4 hue=51 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-412: spacing=8 radius=18 shadow=5 hue=52 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-413: spacing=9 radius=19 shadow=6 hue=53 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-414: spacing=10 radius=20 shadow=7 hue=54 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-415: spacing=11 radius=21 shadow=8 hue=55 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-416: spacing=12 radius=6 shadow=1 hue=56 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-417: spacing=13 radius=7 shadow=2 hue=57 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-418: spacing=14 radius=8 shadow=3 hue=58 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-419: spacing=15 radius=9 shadow=4 hue=59 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-420: spacing=16 radius=10 shadow=5 hue=60 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-421: spacing=17 radius=11 shadow=6 hue=61 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-422: spacing=18 radius=12 shadow=7 hue=62 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-423: spacing=19 radius=13 shadow=8 hue=63 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-424: spacing=20 radius=14 shadow=1 hue=64 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-425: spacing=21 radius=15 shadow=2 hue=65 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-426: spacing=22 radius=16 shadow=3 hue=66 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-427: spacing=23 radius=17 shadow=4 hue=67 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-428: spacing=24 radius=18 shadow=5 hue=68 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-429: spacing=25 radius=19 shadow=6 hue=69 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-430: spacing=26 radius=20 shadow=7 hue=70 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-431: spacing=27 radius=21 shadow=8 hue=71 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-432: spacing=4 radius=6 shadow=1 hue=72 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-433: spacing=5 radius=7 shadow=2 hue=73 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-434: spacing=6 radius=8 shadow=3 hue=74 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-435: spacing=7 radius=9 shadow=4 hue=75 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-436: spacing=8 radius=10 shadow=5 hue=76 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-437: spacing=9 radius=11 shadow=6 hue=77 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-438: spacing=10 radius=12 shadow=7 hue=78 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-439: spacing=11 radius=13 shadow=8 hue=79 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-440: spacing=12 radius=14 shadow=1 hue=80 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-441: spacing=13 radius=15 shadow=2 hue=81 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-442: spacing=14 radius=16 shadow=3 hue=82 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-443: spacing=15 radius=17 shadow=4 hue=83 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-444: spacing=16 radius=18 shadow=5 hue=84 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-445: spacing=17 radius=19 shadow=6 hue=85 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-446: spacing=18 radius=20 shadow=7 hue=86 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-447: spacing=19 radius=21 shadow=8 hue=87 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-448: spacing=20 radius=6 shadow=1 hue=88 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-449: spacing=21 radius=7 shadow=2 hue=89 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-450: spacing=22 radius=8 shadow=3 hue=90 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-451: spacing=23 radius=9 shadow=4 hue=91 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-452: spacing=24 radius=10 shadow=5 hue=92 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-453: spacing=25 radius=11 shadow=6 hue=93 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-454: spacing=26 radius=12 shadow=7 hue=94 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-455: spacing=27 radius=13 shadow=8 hue=95 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-456: spacing=4 radius=14 shadow=1 hue=96 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-457: spacing=5 radius=15 shadow=2 hue=97 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-458: spacing=6 radius=16 shadow=3 hue=98 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-459: spacing=7 radius=17 shadow=4 hue=99 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-460: spacing=8 radius=18 shadow=5 hue=100 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-461: spacing=9 radius=19 shadow=6 hue=101 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-462: spacing=10 radius=20 shadow=7 hue=102 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-463: spacing=11 radius=21 shadow=8 hue=103 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-464: spacing=12 radius=6 shadow=1 hue=104 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-465: spacing=13 radius=7 shadow=2 hue=105 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-466: spacing=14 radius=8 shadow=3 hue=106 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-467: spacing=15 radius=9 shadow=4 hue=107 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-468: spacing=16 radius=10 shadow=5 hue=108 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-469: spacing=17 radius=11 shadow=6 hue=109 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-470: spacing=18 radius=12 shadow=7 hue=110 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-471: spacing=19 radius=13 shadow=8 hue=111 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-472: spacing=20 radius=14 shadow=1 hue=112 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-473: spacing=21 radius=15 shadow=2 hue=113 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-474: spacing=22 radius=16 shadow=3 hue=114 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-475: spacing=23 radius=17 shadow=4 hue=115 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-476: spacing=24 radius=18 shadow=5 hue=116 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-477: spacing=25 radius=19 shadow=6 hue=117 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-478: spacing=26 radius=20 shadow=7 hue=118 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-479: spacing=27 radius=21 shadow=8 hue=119 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-480: spacing=4 radius=6 shadow=1 hue=120 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-481: spacing=5 radius=7 shadow=2 hue=121 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-482: spacing=6 radius=8 shadow=3 hue=122 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-483: spacing=7 radius=9 shadow=4 hue=123 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-484: spacing=8 radius=10 shadow=5 hue=124 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-485: spacing=9 radius=11 shadow=6 hue=125 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-486: spacing=10 radius=12 shadow=7 hue=126 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-487: spacing=11 radius=13 shadow=8 hue=127 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-488: spacing=12 radius=14 shadow=1 hue=128 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-489: spacing=13 radius=15 shadow=2 hue=129 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-490: spacing=14 radius=16 shadow=3 hue=130 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
/* token-491: spacing=15 radius=17 shadow=4 hue=131 motion=600ms AA component=card|btn|nav|kpi|modal|toast */
/* token-492: spacing=16 radius=18 shadow=5 hue=132 motion=700ms AA component=card|btn|nav|kpi|modal|toast */
/* token-493: spacing=17 radius=19 shadow=6 hue=133 motion=800ms AA component=card|btn|nav|kpi|modal|toast */
/* token-494: spacing=18 radius=20 shadow=7 hue=134 motion=900ms AA component=card|btn|nav|kpi|modal|toast */
/* token-495: spacing=19 radius=21 shadow=8 hue=135 motion=100ms AA component=card|btn|nav|kpi|modal|toast */
/* token-496: spacing=20 radius=6 shadow=1 hue=136 motion=200ms AA component=card|btn|nav|kpi|modal|toast */
/* token-497: spacing=21 radius=7 shadow=2 hue=137 motion=300ms AA component=card|btn|nav|kpi|modal|toast */
/* token-498: spacing=22 radius=8 shadow=3 hue=138 motion=400ms AA component=card|btn|nav|kpi|modal|toast */
/* token-499: spacing=23 radius=9 shadow=4 hue=139 motion=500ms AA component=card|btn|nav|kpi|modal|toast */
// util-0: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-1: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-2: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-3: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-4: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-5: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-6: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-7: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-8: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-9: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-10: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-11: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-12: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-13: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-14: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-15: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-16: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-17: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-18: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-19: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-20: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-21: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-22: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-23: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-24: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-25: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-26: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-27: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-28: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-29: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-30: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-31: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-32: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-33: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-34: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-35: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-36: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-37: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-38: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-39: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-40: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-41: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-42: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-43: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-44: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-45: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-46: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-47: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-48: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-49: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-50: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-51: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-52: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-53: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-54: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-55: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-56: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-57: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-58: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-59: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-60: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-61: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-62: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-63: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-64: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-65: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-66: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-67: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-68: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-69: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-70: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-71: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-72: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-73: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-74: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-75: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-76: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-77: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-78: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-79: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-80: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-81: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-82: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-83: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-84: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-85: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-86: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-87: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-88: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-89: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-90: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-91: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-92: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-93: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-94: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-95: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-96: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-97: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-98: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-99: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-100: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-101: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-102: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-103: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-104: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-105: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-106: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-107: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-108: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-109: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-110: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-111: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-112: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-113: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-114: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-115: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-116: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-117: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-118: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-119: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-120: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-121: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-122: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-123: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-124: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-125: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-126: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-127: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-128: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-129: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-130: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-131: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-132: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-133: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-134: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-135: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-136: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-137: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-138: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-139: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-140: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-141: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-142: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-143: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-144: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-145: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-146: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-147: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-148: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-149: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-150: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-151: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-152: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-153: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-154: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-155: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-156: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-157: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-158: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-159: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-160: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-161: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-162: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-163: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-164: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-165: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-166: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-167: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-168: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-169: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-170: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-171: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-172: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-173: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-174: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-175: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-176: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-177: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-178: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-179: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-180: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-181: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-182: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-183: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-184: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-185: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-186: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-187: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-188: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-189: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-190: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-191: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-192: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-193: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-194: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-195: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-196: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-197: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-198: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-199: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-200: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-201: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-202: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-203: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-204: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-205: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-206: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-207: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-208: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-209: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-210: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-211: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-212: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-213: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-214: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-215: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-216: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-217: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-218: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-219: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-220: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-221: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-222: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-223: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-224: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-225: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-226: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-227: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-228: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-229: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-230: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-231: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-232: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-233: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-234: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-235: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-236: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-237: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-238: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-239: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-240: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-241: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-242: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-243: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-244: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-245: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-246: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-247: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-248: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
// util-249: formatBytes themePersist apiClient tableRender chartUpdate sessionGuard clipboard qr
"""

EXTRA_UI_TOKENS = r"""
/* layout-grid-0: col=1 gap=4px align=start|center|stretch responsive-bp=320px glass=0.0 blur=8px */
/* layout-grid-1: col=2 gap=5px align=start|center|stretch responsive-bp=322px glass=0.1 blur=9px */
/* layout-grid-2: col=3 gap=6px align=start|center|stretch responsive-bp=324px glass=0.2 blur=10px */
/* layout-grid-3: col=4 gap=7px align=start|center|stretch responsive-bp=326px glass=0.3 blur=11px */
/* layout-grid-4: col=5 gap=8px align=start|center|stretch responsive-bp=328px glass=0.4 blur=12px */
/* layout-grid-5: col=6 gap=9px align=start|center|stretch responsive-bp=330px glass=0.5 blur=13px */
/* layout-grid-6: col=7 gap=10px align=start|center|stretch responsive-bp=332px glass=0.6 blur=14px */
/* layout-grid-7: col=8 gap=11px align=start|center|stretch responsive-bp=334px glass=0.7 blur=15px */
/* layout-grid-8: col=9 gap=12px align=start|center|stretch responsive-bp=336px glass=0.8 blur=16px */
/* layout-grid-9: col=10 gap=13px align=start|center|stretch responsive-bp=338px glass=0.0 blur=17px */
/* layout-grid-10: col=11 gap=14px align=start|center|stretch responsive-bp=340px glass=0.1 blur=18px */
/* layout-grid-11: col=12 gap=15px align=start|center|stretch responsive-bp=342px glass=0.2 blur=19px */
/* layout-grid-12: col=1 gap=16px align=start|center|stretch responsive-bp=344px glass=0.3 blur=20px */
/* layout-grid-13: col=2 gap=17px align=start|center|stretch responsive-bp=346px glass=0.4 blur=21px */
/* layout-grid-14: col=3 gap=18px align=start|center|stretch responsive-bp=348px glass=0.5 blur=22px */
/* layout-grid-15: col=4 gap=19px align=start|center|stretch responsive-bp=350px glass=0.6 blur=23px */
/* layout-grid-16: col=5 gap=20px align=start|center|stretch responsive-bp=352px glass=0.7 blur=24px */
/* layout-grid-17: col=6 gap=21px align=start|center|stretch responsive-bp=354px glass=0.8 blur=25px */
/* layout-grid-18: col=7 gap=22px align=start|center|stretch responsive-bp=356px glass=0.0 blur=26px */
/* layout-grid-19: col=8 gap=23px align=start|center|stretch responsive-bp=358px glass=0.1 blur=27px */
/* layout-grid-20: col=9 gap=4px align=start|center|stretch responsive-bp=360px glass=0.2 blur=8px */
/* layout-grid-21: col=10 gap=5px align=start|center|stretch responsive-bp=362px glass=0.3 blur=9px */
/* layout-grid-22: col=11 gap=6px align=start|center|stretch responsive-bp=364px glass=0.4 blur=10px */
/* layout-grid-23: col=12 gap=7px align=start|center|stretch responsive-bp=366px glass=0.5 blur=11px */
/* layout-grid-24: col=1 gap=8px align=start|center|stretch responsive-bp=368px glass=0.6 blur=12px */
/* layout-grid-25: col=2 gap=9px align=start|center|stretch responsive-bp=370px glass=0.7 blur=13px */
/* layout-grid-26: col=3 gap=10px align=start|center|stretch responsive-bp=372px glass=0.8 blur=14px */
/* layout-grid-27: col=4 gap=11px align=start|center|stretch responsive-bp=374px glass=0.0 blur=15px */
/* layout-grid-28: col=5 gap=12px align=start|center|stretch responsive-bp=376px glass=0.1 blur=16px */
/* layout-grid-29: col=6 gap=13px align=start|center|stretch responsive-bp=378px glass=0.2 blur=17px */
/* layout-grid-30: col=7 gap=14px align=start|center|stretch responsive-bp=380px glass=0.3 blur=18px */
/* layout-grid-31: col=8 gap=15px align=start|center|stretch responsive-bp=382px glass=0.4 blur=19px */
/* layout-grid-32: col=9 gap=16px align=start|center|stretch responsive-bp=384px glass=0.5 blur=20px */
/* layout-grid-33: col=10 gap=17px align=start|center|stretch responsive-bp=386px glass=0.6 blur=21px */
/* layout-grid-34: col=11 gap=18px align=start|center|stretch responsive-bp=388px glass=0.7 blur=22px */
/* layout-grid-35: col=12 gap=19px align=start|center|stretch responsive-bp=390px glass=0.8 blur=23px */
/* layout-grid-36: col=1 gap=20px align=start|center|stretch responsive-bp=392px glass=0.0 blur=24px */
/* layout-grid-37: col=2 gap=21px align=start|center|stretch responsive-bp=394px glass=0.1 blur=25px */
/* layout-grid-38: col=3 gap=22px align=start|center|stretch responsive-bp=396px glass=0.2 blur=26px */
/* layout-grid-39: col=4 gap=23px align=start|center|stretch responsive-bp=398px glass=0.3 blur=27px */
/* layout-grid-40: col=5 gap=4px align=start|center|stretch responsive-bp=400px glass=0.4 blur=8px */
/* layout-grid-41: col=6 gap=5px align=start|center|stretch responsive-bp=402px glass=0.5 blur=9px */
/* layout-grid-42: col=7 gap=6px align=start|center|stretch responsive-bp=404px glass=0.6 blur=10px */
/* layout-grid-43: col=8 gap=7px align=start|center|stretch responsive-bp=406px glass=0.7 blur=11px */
/* layout-grid-44: col=9 gap=8px align=start|center|stretch responsive-bp=408px glass=0.8 blur=12px */
/* layout-grid-45: col=10 gap=9px align=start|center|stretch responsive-bp=410px glass=0.0 blur=13px */
/* layout-grid-46: col=11 gap=10px align=start|center|stretch responsive-bp=412px glass=0.1 blur=14px */
/* layout-grid-47: col=12 gap=11px align=start|center|stretch responsive-bp=414px glass=0.2 blur=15px */
/* layout-grid-48: col=1 gap=12px align=start|center|stretch responsive-bp=416px glass=0.3 blur=16px */
/* layout-grid-49: col=2 gap=13px align=start|center|stretch responsive-bp=418px glass=0.4 blur=17px */
/* layout-grid-50: col=3 gap=14px align=start|center|stretch responsive-bp=420px glass=0.5 blur=18px */
/* layout-grid-51: col=4 gap=15px align=start|center|stretch responsive-bp=422px glass=0.6 blur=19px */
/* layout-grid-52: col=5 gap=16px align=start|center|stretch responsive-bp=424px glass=0.7 blur=20px */
/* layout-grid-53: col=6 gap=17px align=start|center|stretch responsive-bp=426px glass=0.8 blur=21px */
/* layout-grid-54: col=7 gap=18px align=start|center|stretch responsive-bp=428px glass=0.0 blur=22px */
/* layout-grid-55: col=8 gap=19px align=start|center|stretch responsive-bp=430px glass=0.1 blur=23px */
/* layout-grid-56: col=9 gap=20px align=start|center|stretch responsive-bp=432px glass=0.2 blur=24px */
/* layout-grid-57: col=10 gap=21px align=start|center|stretch responsive-bp=434px glass=0.3 blur=25px */
/* layout-grid-58: col=11 gap=22px align=start|center|stretch responsive-bp=436px glass=0.4 blur=26px */
/* layout-grid-59: col=12 gap=23px align=start|center|stretch responsive-bp=438px glass=0.5 blur=27px */
/* layout-grid-60: col=1 gap=4px align=start|center|stretch responsive-bp=440px glass=0.6 blur=8px */
/* layout-grid-61: col=2 gap=5px align=start|center|stretch responsive-bp=442px glass=0.7 blur=9px */
/* layout-grid-62: col=3 gap=6px align=start|center|stretch responsive-bp=444px glass=0.8 blur=10px */
/* layout-grid-63: col=4 gap=7px align=start|center|stretch responsive-bp=446px glass=0.0 blur=11px */
/* layout-grid-64: col=5 gap=8px align=start|center|stretch responsive-bp=448px glass=0.1 blur=12px */
/* layout-grid-65: col=6 gap=9px align=start|center|stretch responsive-bp=450px glass=0.2 blur=13px */
/* layout-grid-66: col=7 gap=10px align=start|center|stretch responsive-bp=452px glass=0.3 blur=14px */
/* layout-grid-67: col=8 gap=11px align=start|center|stretch responsive-bp=454px glass=0.4 blur=15px */
/* layout-grid-68: col=9 gap=12px align=start|center|stretch responsive-bp=456px glass=0.5 blur=16px */
/* layout-grid-69: col=10 gap=13px align=start|center|stretch responsive-bp=458px glass=0.6 blur=17px */
/* layout-grid-70: col=11 gap=14px align=start|center|stretch responsive-bp=460px glass=0.7 blur=18px */
/* layout-grid-71: col=12 gap=15px align=start|center|stretch responsive-bp=462px glass=0.8 blur=19px */
/* layout-grid-72: col=1 gap=16px align=start|center|stretch responsive-bp=464px glass=0.0 blur=20px */
/* layout-grid-73: col=2 gap=17px align=start|center|stretch responsive-bp=466px glass=0.1 blur=21px */
/* layout-grid-74: col=3 gap=18px align=start|center|stretch responsive-bp=468px glass=0.2 blur=22px */
/* layout-grid-75: col=4 gap=19px align=start|center|stretch responsive-bp=470px glass=0.3 blur=23px */
/* layout-grid-76: col=5 gap=20px align=start|center|stretch responsive-bp=472px glass=0.4 blur=24px */
/* layout-grid-77: col=6 gap=21px align=start|center|stretch responsive-bp=474px glass=0.5 blur=25px */
/* layout-grid-78: col=7 gap=22px align=start|center|stretch responsive-bp=476px glass=0.6 blur=26px */
/* layout-grid-79: col=8 gap=23px align=start|center|stretch responsive-bp=478px glass=0.7 blur=27px */
/* layout-grid-80: col=9 gap=4px align=start|center|stretch responsive-bp=480px glass=0.8 blur=8px */
/* layout-grid-81: col=10 gap=5px align=start|center|stretch responsive-bp=482px glass=0.0 blur=9px */
/* layout-grid-82: col=11 gap=6px align=start|center|stretch responsive-bp=484px glass=0.1 blur=10px */
/* layout-grid-83: col=12 gap=7px align=start|center|stretch responsive-bp=486px glass=0.2 blur=11px */
/* layout-grid-84: col=1 gap=8px align=start|center|stretch responsive-bp=488px glass=0.3 blur=12px */
/* layout-grid-85: col=2 gap=9px align=start|center|stretch responsive-bp=490px glass=0.4 blur=13px */
/* layout-grid-86: col=3 gap=10px align=start|center|stretch responsive-bp=492px glass=0.5 blur=14px */
/* layout-grid-87: col=4 gap=11px align=start|center|stretch responsive-bp=494px glass=0.6 blur=15px */
/* layout-grid-88: col=5 gap=12px align=start|center|stretch responsive-bp=496px glass=0.7 blur=16px */
/* layout-grid-89: col=6 gap=13px align=start|center|stretch responsive-bp=498px glass=0.8 blur=17px */
/* layout-grid-90: col=7 gap=14px align=start|center|stretch responsive-bp=500px glass=0.0 blur=18px */
/* layout-grid-91: col=8 gap=15px align=start|center|stretch responsive-bp=502px glass=0.1 blur=19px */
/* layout-grid-92: col=9 gap=16px align=start|center|stretch responsive-bp=504px glass=0.2 blur=20px */
/* layout-grid-93: col=10 gap=17px align=start|center|stretch responsive-bp=506px glass=0.3 blur=21px */
/* layout-grid-94: col=11 gap=18px align=start|center|stretch responsive-bp=508px glass=0.4 blur=22px */
/* layout-grid-95: col=12 gap=19px align=start|center|stretch responsive-bp=510px glass=0.5 blur=23px */
/* layout-grid-96: col=1 gap=20px align=start|center|stretch responsive-bp=512px glass=0.6 blur=24px */
/* layout-grid-97: col=2 gap=21px align=start|center|stretch responsive-bp=514px glass=0.7 blur=25px */
/* layout-grid-98: col=3 gap=22px align=start|center|stretch responsive-bp=516px glass=0.8 blur=26px */
/* layout-grid-99: col=4 gap=23px align=start|center|stretch responsive-bp=518px glass=0.0 blur=27px */
/* layout-grid-100: col=5 gap=4px align=start|center|stretch responsive-bp=520px glass=0.1 blur=8px */
/* layout-grid-101: col=6 gap=5px align=start|center|stretch responsive-bp=522px glass=0.2 blur=9px */
/* layout-grid-102: col=7 gap=6px align=start|center|stretch responsive-bp=524px glass=0.3 blur=10px */
/* layout-grid-103: col=8 gap=7px align=start|center|stretch responsive-bp=526px glass=0.4 blur=11px */
/* layout-grid-104: col=9 gap=8px align=start|center|stretch responsive-bp=528px glass=0.5 blur=12px */
/* layout-grid-105: col=10 gap=9px align=start|center|stretch responsive-bp=530px glass=0.6 blur=13px */
/* layout-grid-106: col=11 gap=10px align=start|center|stretch responsive-bp=532px glass=0.7 blur=14px */
/* layout-grid-107: col=12 gap=11px align=start|center|stretch responsive-bp=534px glass=0.8 blur=15px */
/* layout-grid-108: col=1 gap=12px align=start|center|stretch responsive-bp=536px glass=0.0 blur=16px */
/* layout-grid-109: col=2 gap=13px align=start|center|stretch responsive-bp=538px glass=0.1 blur=17px */
/* layout-grid-110: col=3 gap=14px align=start|center|stretch responsive-bp=540px glass=0.2 blur=18px */
/* layout-grid-111: col=4 gap=15px align=start|center|stretch responsive-bp=542px glass=0.3 blur=19px */
/* layout-grid-112: col=5 gap=16px align=start|center|stretch responsive-bp=544px glass=0.4 blur=20px */
/* layout-grid-113: col=6 gap=17px align=start|center|stretch responsive-bp=546px glass=0.5 blur=21px */
/* layout-grid-114: col=7 gap=18px align=start|center|stretch responsive-bp=548px glass=0.6 blur=22px */
/* layout-grid-115: col=8 gap=19px align=start|center|stretch responsive-bp=550px glass=0.7 blur=23px */
/* layout-grid-116: col=9 gap=20px align=start|center|stretch responsive-bp=552px glass=0.8 blur=24px */
/* layout-grid-117: col=10 gap=21px align=start|center|stretch responsive-bp=554px glass=0.0 blur=25px */
/* layout-grid-118: col=11 gap=22px align=start|center|stretch responsive-bp=556px glass=0.1 blur=26px */
/* layout-grid-119: col=12 gap=23px align=start|center|stretch responsive-bp=558px glass=0.2 blur=27px */
/* layout-grid-120: col=1 gap=4px align=start|center|stretch responsive-bp=560px glass=0.3 blur=8px */
/* layout-grid-121: col=2 gap=5px align=start|center|stretch responsive-bp=562px glass=0.4 blur=9px */
/* layout-grid-122: col=3 gap=6px align=start|center|stretch responsive-bp=564px glass=0.5 blur=10px */
/* layout-grid-123: col=4 gap=7px align=start|center|stretch responsive-bp=566px glass=0.6 blur=11px */
/* layout-grid-124: col=5 gap=8px align=start|center|stretch responsive-bp=568px glass=0.7 blur=12px */
/* layout-grid-125: col=6 gap=9px align=start|center|stretch responsive-bp=570px glass=0.8 blur=13px */
/* layout-grid-126: col=7 gap=10px align=start|center|stretch responsive-bp=572px glass=0.0 blur=14px */
/* layout-grid-127: col=8 gap=11px align=start|center|stretch responsive-bp=574px glass=0.1 blur=15px */
/* layout-grid-128: col=9 gap=12px align=start|center|stretch responsive-bp=576px glass=0.2 blur=16px */
/* layout-grid-129: col=10 gap=13px align=start|center|stretch responsive-bp=578px glass=0.3 blur=17px */
/* layout-grid-130: col=11 gap=14px align=start|center|stretch responsive-bp=580px glass=0.4 blur=18px */
/* layout-grid-131: col=12 gap=15px align=start|center|stretch responsive-bp=582px glass=0.5 blur=19px */
/* layout-grid-132: col=1 gap=16px align=start|center|stretch responsive-bp=584px glass=0.6 blur=20px */
/* layout-grid-133: col=2 gap=17px align=start|center|stretch responsive-bp=586px glass=0.7 blur=21px */
/* layout-grid-134: col=3 gap=18px align=start|center|stretch responsive-bp=588px glass=0.8 blur=22px */
/* layout-grid-135: col=4 gap=19px align=start|center|stretch responsive-bp=590px glass=0.0 blur=23px */
/* layout-grid-136: col=5 gap=20px align=start|center|stretch responsive-bp=592px glass=0.1 blur=24px */
/* layout-grid-137: col=6 gap=21px align=start|center|stretch responsive-bp=594px glass=0.2 blur=25px */
/* layout-grid-138: col=7 gap=22px align=start|center|stretch responsive-bp=596px glass=0.3 blur=26px */
/* layout-grid-139: col=8 gap=23px align=start|center|stretch responsive-bp=598px glass=0.4 blur=27px */
/* layout-grid-140: col=9 gap=4px align=start|center|stretch responsive-bp=600px glass=0.5 blur=8px */
/* layout-grid-141: col=10 gap=5px align=start|center|stretch responsive-bp=602px glass=0.6 blur=9px */
/* layout-grid-142: col=11 gap=6px align=start|center|stretch responsive-bp=604px glass=0.7 blur=10px */
/* layout-grid-143: col=12 gap=7px align=start|center|stretch responsive-bp=606px glass=0.8 blur=11px */
/* layout-grid-144: col=1 gap=8px align=start|center|stretch responsive-bp=608px glass=0.0 blur=12px */
/* layout-grid-145: col=2 gap=9px align=start|center|stretch responsive-bp=610px glass=0.1 blur=13px */
/* layout-grid-146: col=3 gap=10px align=start|center|stretch responsive-bp=612px glass=0.2 blur=14px */
/* layout-grid-147: col=4 gap=11px align=start|center|stretch responsive-bp=614px glass=0.3 blur=15px */
/* layout-grid-148: col=5 gap=12px align=start|center|stretch responsive-bp=616px glass=0.4 blur=16px */
/* layout-grid-149: col=6 gap=13px align=start|center|stretch responsive-bp=618px glass=0.5 blur=17px */
/* layout-grid-150: col=7 gap=14px align=start|center|stretch responsive-bp=620px glass=0.6 blur=18px */
/* layout-grid-151: col=8 gap=15px align=start|center|stretch responsive-bp=622px glass=0.7 blur=19px */
/* layout-grid-152: col=9 gap=16px align=start|center|stretch responsive-bp=624px glass=0.8 blur=20px */
/* layout-grid-153: col=10 gap=17px align=start|center|stretch responsive-bp=626px glass=0.0 blur=21px */
/* layout-grid-154: col=11 gap=18px align=start|center|stretch responsive-bp=628px glass=0.1 blur=22px */
/* layout-grid-155: col=12 gap=19px align=start|center|stretch responsive-bp=630px glass=0.2 blur=23px */
/* layout-grid-156: col=1 gap=20px align=start|center|stretch responsive-bp=632px glass=0.3 blur=24px */
/* layout-grid-157: col=2 gap=21px align=start|center|stretch responsive-bp=634px glass=0.4 blur=25px */
/* layout-grid-158: col=3 gap=22px align=start|center|stretch responsive-bp=636px glass=0.5 blur=26px */
/* layout-grid-159: col=4 gap=23px align=start|center|stretch responsive-bp=638px glass=0.6 blur=27px */
/* layout-grid-160: col=5 gap=4px align=start|center|stretch responsive-bp=640px glass=0.7 blur=8px */
/* layout-grid-161: col=6 gap=5px align=start|center|stretch responsive-bp=642px glass=0.8 blur=9px */
/* layout-grid-162: col=7 gap=6px align=start|center|stretch responsive-bp=644px glass=0.0 blur=10px */
/* layout-grid-163: col=8 gap=7px align=start|center|stretch responsive-bp=646px glass=0.1 blur=11px */
/* layout-grid-164: col=9 gap=8px align=start|center|stretch responsive-bp=648px glass=0.2 blur=12px */
/* layout-grid-165: col=10 gap=9px align=start|center|stretch responsive-bp=650px glass=0.3 blur=13px */
/* layout-grid-166: col=11 gap=10px align=start|center|stretch responsive-bp=652px glass=0.4 blur=14px */
/* layout-grid-167: col=12 gap=11px align=start|center|stretch responsive-bp=654px glass=0.5 blur=15px */
/* layout-grid-168: col=1 gap=12px align=start|center|stretch responsive-bp=656px glass=0.6 blur=16px */
/* layout-grid-169: col=2 gap=13px align=start|center|stretch responsive-bp=658px glass=0.7 blur=17px */
/* layout-grid-170: col=3 gap=14px align=start|center|stretch responsive-bp=660px glass=0.8 blur=18px */
/* layout-grid-171: col=4 gap=15px align=start|center|stretch responsive-bp=662px glass=0.0 blur=19px */
/* layout-grid-172: col=5 gap=16px align=start|center|stretch responsive-bp=664px glass=0.1 blur=20px */
/* layout-grid-173: col=6 gap=17px align=start|center|stretch responsive-bp=666px glass=0.2 blur=21px */
/* layout-grid-174: col=7 gap=18px align=start|center|stretch responsive-bp=668px glass=0.3 blur=22px */
/* layout-grid-175: col=8 gap=19px align=start|center|stretch responsive-bp=670px glass=0.4 blur=23px */
/* layout-grid-176: col=9 gap=20px align=start|center|stretch responsive-bp=672px glass=0.5 blur=24px */
/* layout-grid-177: col=10 gap=21px align=start|center|stretch responsive-bp=674px glass=0.6 blur=25px */
/* layout-grid-178: col=11 gap=22px align=start|center|stretch responsive-bp=676px glass=0.7 blur=26px */
/* layout-grid-179: col=12 gap=23px align=start|center|stretch responsive-bp=678px glass=0.8 blur=27px */
/* layout-grid-180: col=1 gap=4px align=start|center|stretch responsive-bp=680px glass=0.0 blur=8px */
/* layout-grid-181: col=2 gap=5px align=start|center|stretch responsive-bp=682px glass=0.1 blur=9px */
/* layout-grid-182: col=3 gap=6px align=start|center|stretch responsive-bp=684px glass=0.2 blur=10px */
/* layout-grid-183: col=4 gap=7px align=start|center|stretch responsive-bp=686px glass=0.3 blur=11px */
/* layout-grid-184: col=5 gap=8px align=start|center|stretch responsive-bp=688px glass=0.4 blur=12px */
/* layout-grid-185: col=6 gap=9px align=start|center|stretch responsive-bp=690px glass=0.5 blur=13px */
/* layout-grid-186: col=7 gap=10px align=start|center|stretch responsive-bp=692px glass=0.6 blur=14px */
/* layout-grid-187: col=8 gap=11px align=start|center|stretch responsive-bp=694px glass=0.7 blur=15px */
/* layout-grid-188: col=9 gap=12px align=start|center|stretch responsive-bp=696px glass=0.8 blur=16px */
/* layout-grid-189: col=10 gap=13px align=start|center|stretch responsive-bp=698px glass=0.0 blur=17px */
/* layout-grid-190: col=11 gap=14px align=start|center|stretch responsive-bp=700px glass=0.1 blur=18px */
/* layout-grid-191: col=12 gap=15px align=start|center|stretch responsive-bp=702px glass=0.2 blur=19px */
/* layout-grid-192: col=1 gap=16px align=start|center|stretch responsive-bp=704px glass=0.3 blur=20px */
/* layout-grid-193: col=2 gap=17px align=start|center|stretch responsive-bp=706px glass=0.4 blur=21px */
/* layout-grid-194: col=3 gap=18px align=start|center|stretch responsive-bp=708px glass=0.5 blur=22px */
/* layout-grid-195: col=4 gap=19px align=start|center|stretch responsive-bp=710px glass=0.6 blur=23px */
/* layout-grid-196: col=5 gap=20px align=start|center|stretch responsive-bp=712px glass=0.7 blur=24px */
/* layout-grid-197: col=6 gap=21px align=start|center|stretch responsive-bp=714px glass=0.8 blur=25px */
/* layout-grid-198: col=7 gap=22px align=start|center|stretch responsive-bp=716px glass=0.0 blur=26px */
/* layout-grid-199: col=8 gap=23px align=start|center|stretch responsive-bp=718px glass=0.1 blur=27px */
/* layout-grid-200: col=9 gap=4px align=start|center|stretch responsive-bp=720px glass=0.2 blur=8px */
/* layout-grid-201: col=10 gap=5px align=start|center|stretch responsive-bp=722px glass=0.3 blur=9px */
/* layout-grid-202: col=11 gap=6px align=start|center|stretch responsive-bp=724px glass=0.4 blur=10px */
/* layout-grid-203: col=12 gap=7px align=start|center|stretch responsive-bp=726px glass=0.5 blur=11px */
/* layout-grid-204: col=1 gap=8px align=start|center|stretch responsive-bp=728px glass=0.6 blur=12px */
/* layout-grid-205: col=2 gap=9px align=start|center|stretch responsive-bp=730px glass=0.7 blur=13px */
/* layout-grid-206: col=3 gap=10px align=start|center|stretch responsive-bp=732px glass=0.8 blur=14px */
/* layout-grid-207: col=4 gap=11px align=start|center|stretch responsive-bp=734px glass=0.0 blur=15px */
/* layout-grid-208: col=5 gap=12px align=start|center|stretch responsive-bp=736px glass=0.1 blur=16px */
/* layout-grid-209: col=6 gap=13px align=start|center|stretch responsive-bp=738px glass=0.2 blur=17px */
/* layout-grid-210: col=7 gap=14px align=start|center|stretch responsive-bp=740px glass=0.3 blur=18px */
/* layout-grid-211: col=8 gap=15px align=start|center|stretch responsive-bp=742px glass=0.4 blur=19px */
/* layout-grid-212: col=9 gap=16px align=start|center|stretch responsive-bp=744px glass=0.5 blur=20px */
/* layout-grid-213: col=10 gap=17px align=start|center|stretch responsive-bp=746px glass=0.6 blur=21px */
/* layout-grid-214: col=11 gap=18px align=start|center|stretch responsive-bp=748px glass=0.7 blur=22px */
/* layout-grid-215: col=12 gap=19px align=start|center|stretch responsive-bp=750px glass=0.8 blur=23px */
/* layout-grid-216: col=1 gap=20px align=start|center|stretch responsive-bp=752px glass=0.0 blur=24px */
/* layout-grid-217: col=2 gap=21px align=start|center|stretch responsive-bp=754px glass=0.1 blur=25px */
/* layout-grid-218: col=3 gap=22px align=start|center|stretch responsive-bp=756px glass=0.2 blur=26px */
/* layout-grid-219: col=4 gap=23px align=start|center|stretch responsive-bp=758px glass=0.3 blur=27px */
/* layout-grid-220: col=5 gap=4px align=start|center|stretch responsive-bp=760px glass=0.4 blur=8px */
/* layout-grid-221: col=6 gap=5px align=start|center|stretch responsive-bp=762px glass=0.5 blur=9px */
/* layout-grid-222: col=7 gap=6px align=start|center|stretch responsive-bp=764px glass=0.6 blur=10px */
/* layout-grid-223: col=8 gap=7px align=start|center|stretch responsive-bp=766px glass=0.7 blur=11px */
/* layout-grid-224: col=9 gap=8px align=start|center|stretch responsive-bp=768px glass=0.8 blur=12px */
/* layout-grid-225: col=10 gap=9px align=start|center|stretch responsive-bp=770px glass=0.0 blur=13px */
/* layout-grid-226: col=11 gap=10px align=start|center|stretch responsive-bp=772px glass=0.1 blur=14px */
/* layout-grid-227: col=12 gap=11px align=start|center|stretch responsive-bp=774px glass=0.2 blur=15px */
/* layout-grid-228: col=1 gap=12px align=start|center|stretch responsive-bp=776px glass=0.3 blur=16px */
/* layout-grid-229: col=2 gap=13px align=start|center|stretch responsive-bp=778px glass=0.4 blur=17px */
/* layout-grid-230: col=3 gap=14px align=start|center|stretch responsive-bp=780px glass=0.5 blur=18px */
/* layout-grid-231: col=4 gap=15px align=start|center|stretch responsive-bp=782px glass=0.6 blur=19px */
/* layout-grid-232: col=5 gap=16px align=start|center|stretch responsive-bp=784px glass=0.7 blur=20px */
/* layout-grid-233: col=6 gap=17px align=start|center|stretch responsive-bp=786px glass=0.8 blur=21px */
/* layout-grid-234: col=7 gap=18px align=start|center|stretch responsive-bp=788px glass=0.0 blur=22px */
/* layout-grid-235: col=8 gap=19px align=start|center|stretch responsive-bp=790px glass=0.1 blur=23px */
/* layout-grid-236: col=9 gap=20px align=start|center|stretch responsive-bp=792px glass=0.2 blur=24px */
/* layout-grid-237: col=10 gap=21px align=start|center|stretch responsive-bp=794px glass=0.3 blur=25px */
/* layout-grid-238: col=11 gap=22px align=start|center|stretch responsive-bp=796px glass=0.4 blur=26px */
/* layout-grid-239: col=12 gap=23px align=start|center|stretch responsive-bp=798px glass=0.5 blur=27px */
/* layout-grid-240: col=1 gap=4px align=start|center|stretch responsive-bp=800px glass=0.6 blur=8px */
/* layout-grid-241: col=2 gap=5px align=start|center|stretch responsive-bp=802px glass=0.7 blur=9px */
/* layout-grid-242: col=3 gap=6px align=start|center|stretch responsive-bp=804px glass=0.8 blur=10px */
/* layout-grid-243: col=4 gap=7px align=start|center|stretch responsive-bp=806px glass=0.0 blur=11px */
/* layout-grid-244: col=5 gap=8px align=start|center|stretch responsive-bp=808px glass=0.1 blur=12px */
/* layout-grid-245: col=6 gap=9px align=start|center|stretch responsive-bp=810px glass=0.2 blur=13px */
/* layout-grid-246: col=7 gap=10px align=start|center|stretch responsive-bp=812px glass=0.3 blur=14px */
/* layout-grid-247: col=8 gap=11px align=start|center|stretch responsive-bp=814px glass=0.4 blur=15px */
/* layout-grid-248: col=9 gap=12px align=start|center|stretch responsive-bp=816px glass=0.5 blur=16px */
/* layout-grid-249: col=10 gap=13px align=start|center|stretch responsive-bp=818px glass=0.6 blur=17px */
/* layout-grid-250: col=11 gap=14px align=start|center|stretch responsive-bp=820px glass=0.7 blur=18px */
/* layout-grid-251: col=12 gap=15px align=start|center|stretch responsive-bp=822px glass=0.8 blur=19px */
/* layout-grid-252: col=1 gap=16px align=start|center|stretch responsive-bp=824px glass=0.0 blur=20px */
/* layout-grid-253: col=2 gap=17px align=start|center|stretch responsive-bp=826px glass=0.1 blur=21px */
/* layout-grid-254: col=3 gap=18px align=start|center|stretch responsive-bp=828px glass=0.2 blur=22px */
/* layout-grid-255: col=4 gap=19px align=start|center|stretch responsive-bp=830px glass=0.3 blur=23px */
/* layout-grid-256: col=5 gap=20px align=start|center|stretch responsive-bp=832px glass=0.4 blur=24px */
/* layout-grid-257: col=6 gap=21px align=start|center|stretch responsive-bp=834px glass=0.5 blur=25px */
/* layout-grid-258: col=7 gap=22px align=start|center|stretch responsive-bp=836px glass=0.6 blur=26px */
/* layout-grid-259: col=8 gap=23px align=start|center|stretch responsive-bp=838px glass=0.7 blur=27px */
/* layout-grid-260: col=9 gap=4px align=start|center|stretch responsive-bp=840px glass=0.8 blur=8px */
/* layout-grid-261: col=10 gap=5px align=start|center|stretch responsive-bp=842px glass=0.0 blur=9px */
/* layout-grid-262: col=11 gap=6px align=start|center|stretch responsive-bp=844px glass=0.1 blur=10px */
/* layout-grid-263: col=12 gap=7px align=start|center|stretch responsive-bp=846px glass=0.2 blur=11px */
/* layout-grid-264: col=1 gap=8px align=start|center|stretch responsive-bp=848px glass=0.3 blur=12px */
/* layout-grid-265: col=2 gap=9px align=start|center|stretch responsive-bp=850px glass=0.4 blur=13px */
/* layout-grid-266: col=3 gap=10px align=start|center|stretch responsive-bp=852px glass=0.5 blur=14px */
/* layout-grid-267: col=4 gap=11px align=start|center|stretch responsive-bp=854px glass=0.6 blur=15px */
/* layout-grid-268: col=5 gap=12px align=start|center|stretch responsive-bp=856px glass=0.7 blur=16px */
/* layout-grid-269: col=6 gap=13px align=start|center|stretch responsive-bp=858px glass=0.8 blur=17px */
/* layout-grid-270: col=7 gap=14px align=start|center|stretch responsive-bp=860px glass=0.0 blur=18px */
/* layout-grid-271: col=8 gap=15px align=start|center|stretch responsive-bp=862px glass=0.1 blur=19px */
/* layout-grid-272: col=9 gap=16px align=start|center|stretch responsive-bp=864px glass=0.2 blur=20px */
/* layout-grid-273: col=10 gap=17px align=start|center|stretch responsive-bp=866px glass=0.3 blur=21px */
/* layout-grid-274: col=11 gap=18px align=start|center|stretch responsive-bp=868px glass=0.4 blur=22px */
/* layout-grid-275: col=12 gap=19px align=start|center|stretch responsive-bp=870px glass=0.5 blur=23px */
/* layout-grid-276: col=1 gap=20px align=start|center|stretch responsive-bp=872px glass=0.6 blur=24px */
/* layout-grid-277: col=2 gap=21px align=start|center|stretch responsive-bp=874px glass=0.7 blur=25px */
/* layout-grid-278: col=3 gap=22px align=start|center|stretch responsive-bp=876px glass=0.8 blur=26px */
/* layout-grid-279: col=4 gap=23px align=start|center|stretch responsive-bp=878px glass=0.0 blur=27px */
/* layout-grid-280: col=5 gap=4px align=start|center|stretch responsive-bp=880px glass=0.1 blur=8px */
/* layout-grid-281: col=6 gap=5px align=start|center|stretch responsive-bp=882px glass=0.2 blur=9px */
/* layout-grid-282: col=7 gap=6px align=start|center|stretch responsive-bp=884px glass=0.3 blur=10px */
/* layout-grid-283: col=8 gap=7px align=start|center|stretch responsive-bp=886px glass=0.4 blur=11px */
/* layout-grid-284: col=9 gap=8px align=start|center|stretch responsive-bp=888px glass=0.5 blur=12px */
/* layout-grid-285: col=10 gap=9px align=start|center|stretch responsive-bp=890px glass=0.6 blur=13px */
/* layout-grid-286: col=11 gap=10px align=start|center|stretch responsive-bp=892px glass=0.7 blur=14px */
/* layout-grid-287: col=12 gap=11px align=start|center|stretch responsive-bp=894px glass=0.8 blur=15px */
/* layout-grid-288: col=1 gap=12px align=start|center|stretch responsive-bp=896px glass=0.0 blur=16px */
/* layout-grid-289: col=2 gap=13px align=start|center|stretch responsive-bp=898px glass=0.1 blur=17px */
/* layout-grid-290: col=3 gap=14px align=start|center|stretch responsive-bp=900px glass=0.2 blur=18px */
/* layout-grid-291: col=4 gap=15px align=start|center|stretch responsive-bp=902px glass=0.3 blur=19px */
/* layout-grid-292: col=5 gap=16px align=start|center|stretch responsive-bp=904px glass=0.4 blur=20px */
/* layout-grid-293: col=6 gap=17px align=start|center|stretch responsive-bp=906px glass=0.5 blur=21px */
/* layout-grid-294: col=7 gap=18px align=start|center|stretch responsive-bp=908px glass=0.6 blur=22px */
/* layout-grid-295: col=8 gap=19px align=start|center|stretch responsive-bp=910px glass=0.7 blur=23px */
/* layout-grid-296: col=9 gap=20px align=start|center|stretch responsive-bp=912px glass=0.8 blur=24px */
/* layout-grid-297: col=10 gap=21px align=start|center|stretch responsive-bp=914px glass=0.0 blur=25px */
/* layout-grid-298: col=11 gap=22px align=start|center|stretch responsive-bp=916px glass=0.1 blur=26px */
/* layout-grid-299: col=12 gap=23px align=start|center|stretch responsive-bp=918px glass=0.2 blur=27px */
/* layout-grid-300: col=1 gap=4px align=start|center|stretch responsive-bp=920px glass=0.3 blur=8px */
/* layout-grid-301: col=2 gap=5px align=start|center|stretch responsive-bp=922px glass=0.4 blur=9px */
/* layout-grid-302: col=3 gap=6px align=start|center|stretch responsive-bp=924px glass=0.5 blur=10px */
/* layout-grid-303: col=4 gap=7px align=start|center|stretch responsive-bp=926px glass=0.6 blur=11px */
/* layout-grid-304: col=5 gap=8px align=start|center|stretch responsive-bp=928px glass=0.7 blur=12px */
/* layout-grid-305: col=6 gap=9px align=start|center|stretch responsive-bp=930px glass=0.8 blur=13px */
/* layout-grid-306: col=7 gap=10px align=start|center|stretch responsive-bp=932px glass=0.0 blur=14px */
/* layout-grid-307: col=8 gap=11px align=start|center|stretch responsive-bp=934px glass=0.1 blur=15px */
/* layout-grid-308: col=9 gap=12px align=start|center|stretch responsive-bp=936px glass=0.2 blur=16px */
/* layout-grid-309: col=10 gap=13px align=start|center|stretch responsive-bp=938px glass=0.3 blur=17px */
/* layout-grid-310: col=11 gap=14px align=start|center|stretch responsive-bp=940px glass=0.4 blur=18px */
/* layout-grid-311: col=12 gap=15px align=start|center|stretch responsive-bp=942px glass=0.5 blur=19px */
/* layout-grid-312: col=1 gap=16px align=start|center|stretch responsive-bp=944px glass=0.6 blur=20px */
/* layout-grid-313: col=2 gap=17px align=start|center|stretch responsive-bp=946px glass=0.7 blur=21px */
/* layout-grid-314: col=3 gap=18px align=start|center|stretch responsive-bp=948px glass=0.8 blur=22px */
/* layout-grid-315: col=4 gap=19px align=start|center|stretch responsive-bp=950px glass=0.0 blur=23px */
/* layout-grid-316: col=5 gap=20px align=start|center|stretch responsive-bp=952px glass=0.1 blur=24px */
/* layout-grid-317: col=6 gap=21px align=start|center|stretch responsive-bp=954px glass=0.2 blur=25px */
/* layout-grid-318: col=7 gap=22px align=start|center|stretch responsive-bp=956px glass=0.3 blur=26px */
/* layout-grid-319: col=8 gap=23px align=start|center|stretch responsive-bp=958px glass=0.4 blur=27px */
/* layout-grid-320: col=9 gap=4px align=start|center|stretch responsive-bp=960px glass=0.5 blur=8px */
/* layout-grid-321: col=10 gap=5px align=start|center|stretch responsive-bp=962px glass=0.6 blur=9px */
/* layout-grid-322: col=11 gap=6px align=start|center|stretch responsive-bp=964px glass=0.7 blur=10px */
/* layout-grid-323: col=12 gap=7px align=start|center|stretch responsive-bp=966px glass=0.8 blur=11px */
/* layout-grid-324: col=1 gap=8px align=start|center|stretch responsive-bp=968px glass=0.0 blur=12px */
/* layout-grid-325: col=2 gap=9px align=start|center|stretch responsive-bp=970px glass=0.1 blur=13px */
/* layout-grid-326: col=3 gap=10px align=start|center|stretch responsive-bp=972px glass=0.2 blur=14px */
/* layout-grid-327: col=4 gap=11px align=start|center|stretch responsive-bp=974px glass=0.3 blur=15px */
/* layout-grid-328: col=5 gap=12px align=start|center|stretch responsive-bp=976px glass=0.4 blur=16px */
/* layout-grid-329: col=6 gap=13px align=start|center|stretch responsive-bp=978px glass=0.5 blur=17px */
/* layout-grid-330: col=7 gap=14px align=start|center|stretch responsive-bp=980px glass=0.6 blur=18px */
/* layout-grid-331: col=8 gap=15px align=start|center|stretch responsive-bp=982px glass=0.7 blur=19px */
/* layout-grid-332: col=9 gap=16px align=start|center|stretch responsive-bp=984px glass=0.8 blur=20px */
/* layout-grid-333: col=10 gap=17px align=start|center|stretch responsive-bp=986px glass=0.0 blur=21px */
/* layout-grid-334: col=11 gap=18px align=start|center|stretch responsive-bp=988px glass=0.1 blur=22px */
/* layout-grid-335: col=12 gap=19px align=start|center|stretch responsive-bp=990px glass=0.2 blur=23px */
/* layout-grid-336: col=1 gap=20px align=start|center|stretch responsive-bp=992px glass=0.3 blur=24px */
/* layout-grid-337: col=2 gap=21px align=start|center|stretch responsive-bp=994px glass=0.4 blur=25px */
/* layout-grid-338: col=3 gap=22px align=start|center|stretch responsive-bp=996px glass=0.5 blur=26px */
/* layout-grid-339: col=4 gap=23px align=start|center|stretch responsive-bp=998px glass=0.6 blur=27px */
/* layout-grid-340: col=5 gap=4px align=start|center|stretch responsive-bp=1000px glass=0.7 blur=8px */
/* layout-grid-341: col=6 gap=5px align=start|center|stretch responsive-bp=1002px glass=0.8 blur=9px */
/* layout-grid-342: col=7 gap=6px align=start|center|stretch responsive-bp=1004px glass=0.0 blur=10px */
/* layout-grid-343: col=8 gap=7px align=start|center|stretch responsive-bp=1006px glass=0.1 blur=11px */
/* layout-grid-344: col=9 gap=8px align=start|center|stretch responsive-bp=1008px glass=0.2 blur=12px */
/* layout-grid-345: col=10 gap=9px align=start|center|stretch responsive-bp=1010px glass=0.3 blur=13px */
/* layout-grid-346: col=11 gap=10px align=start|center|stretch responsive-bp=1012px glass=0.4 blur=14px */
/* layout-grid-347: col=12 gap=11px align=start|center|stretch responsive-bp=1014px glass=0.5 blur=15px */
/* layout-grid-348: col=1 gap=12px align=start|center|stretch responsive-bp=1016px glass=0.6 blur=16px */
/* layout-grid-349: col=2 gap=13px align=start|center|stretch responsive-bp=1018px glass=0.7 blur=17px */
/* layout-grid-350: col=3 gap=14px align=start|center|stretch responsive-bp=1020px glass=0.8 blur=18px */
/* layout-grid-351: col=4 gap=15px align=start|center|stretch responsive-bp=1022px glass=0.0 blur=19px */
/* layout-grid-352: col=5 gap=16px align=start|center|stretch responsive-bp=1024px glass=0.1 blur=20px */
/* layout-grid-353: col=6 gap=17px align=start|center|stretch responsive-bp=1026px glass=0.2 blur=21px */
/* layout-grid-354: col=7 gap=18px align=start|center|stretch responsive-bp=1028px glass=0.3 blur=22px */
/* layout-grid-355: col=8 gap=19px align=start|center|stretch responsive-bp=1030px glass=0.4 blur=23px */
/* layout-grid-356: col=9 gap=20px align=start|center|stretch responsive-bp=1032px glass=0.5 blur=24px */
/* layout-grid-357: col=10 gap=21px align=start|center|stretch responsive-bp=1034px glass=0.6 blur=25px */
/* layout-grid-358: col=11 gap=22px align=start|center|stretch responsive-bp=1036px glass=0.7 blur=26px */
/* layout-grid-359: col=12 gap=23px align=start|center|stretch responsive-bp=1038px glass=0.8 blur=27px */
/* layout-grid-360: col=1 gap=4px align=start|center|stretch responsive-bp=1040px glass=0.0 blur=8px */
/* layout-grid-361: col=2 gap=5px align=start|center|stretch responsive-bp=1042px glass=0.1 blur=9px */
/* layout-grid-362: col=3 gap=6px align=start|center|stretch responsive-bp=1044px glass=0.2 blur=10px */
/* layout-grid-363: col=4 gap=7px align=start|center|stretch responsive-bp=1046px glass=0.3 blur=11px */
/* layout-grid-364: col=5 gap=8px align=start|center|stretch responsive-bp=1048px glass=0.4 blur=12px */
/* layout-grid-365: col=6 gap=9px align=start|center|stretch responsive-bp=1050px glass=0.5 blur=13px */
/* layout-grid-366: col=7 gap=10px align=start|center|stretch responsive-bp=1052px glass=0.6 blur=14px */
/* layout-grid-367: col=8 gap=11px align=start|center|stretch responsive-bp=1054px glass=0.7 blur=15px */
/* layout-grid-368: col=9 gap=12px align=start|center|stretch responsive-bp=1056px glass=0.8 blur=16px */
/* layout-grid-369: col=10 gap=13px align=start|center|stretch responsive-bp=1058px glass=0.0 blur=17px */
/* layout-grid-370: col=11 gap=14px align=start|center|stretch responsive-bp=1060px glass=0.1 blur=18px */
/* layout-grid-371: col=12 gap=15px align=start|center|stretch responsive-bp=1062px glass=0.2 blur=19px */
/* layout-grid-372: col=1 gap=16px align=start|center|stretch responsive-bp=1064px glass=0.3 blur=20px */
/* layout-grid-373: col=2 gap=17px align=start|center|stretch responsive-bp=1066px glass=0.4 blur=21px */
/* layout-grid-374: col=3 gap=18px align=start|center|stretch responsive-bp=1068px glass=0.5 blur=22px */
/* layout-grid-375: col=4 gap=19px align=start|center|stretch responsive-bp=1070px glass=0.6 blur=23px */
/* layout-grid-376: col=5 gap=20px align=start|center|stretch responsive-bp=1072px glass=0.7 blur=24px */
/* layout-grid-377: col=6 gap=21px align=start|center|stretch responsive-bp=1074px glass=0.8 blur=25px */
/* layout-grid-378: col=7 gap=22px align=start|center|stretch responsive-bp=1076px glass=0.0 blur=26px */
/* layout-grid-379: col=8 gap=23px align=start|center|stretch responsive-bp=1078px glass=0.1 blur=27px */
/* layout-grid-380: col=9 gap=4px align=start|center|stretch responsive-bp=1080px glass=0.2 blur=8px */
/* layout-grid-381: col=10 gap=5px align=start|center|stretch responsive-bp=1082px glass=0.3 blur=9px */
/* layout-grid-382: col=11 gap=6px align=start|center|stretch responsive-bp=1084px glass=0.4 blur=10px */
/* layout-grid-383: col=12 gap=7px align=start|center|stretch responsive-bp=1086px glass=0.5 blur=11px */
/* layout-grid-384: col=1 gap=8px align=start|center|stretch responsive-bp=1088px glass=0.6 blur=12px */
/* layout-grid-385: col=2 gap=9px align=start|center|stretch responsive-bp=1090px glass=0.7 blur=13px */
/* layout-grid-386: col=3 gap=10px align=start|center|stretch responsive-bp=1092px glass=0.8 blur=14px */
/* layout-grid-387: col=4 gap=11px align=start|center|stretch responsive-bp=1094px glass=0.0 blur=15px */
/* layout-grid-388: col=5 gap=12px align=start|center|stretch responsive-bp=1096px glass=0.1 blur=16px */
/* layout-grid-389: col=6 gap=13px align=start|center|stretch responsive-bp=1098px glass=0.2 blur=17px */
/* layout-grid-390: col=7 gap=14px align=start|center|stretch responsive-bp=1100px glass=0.3 blur=18px */
/* layout-grid-391: col=8 gap=15px align=start|center|stretch responsive-bp=1102px glass=0.4 blur=19px */
/* layout-grid-392: col=9 gap=16px align=start|center|stretch responsive-bp=1104px glass=0.5 blur=20px */
/* layout-grid-393: col=10 gap=17px align=start|center|stretch responsive-bp=1106px glass=0.6 blur=21px */
/* layout-grid-394: col=11 gap=18px align=start|center|stretch responsive-bp=1108px glass=0.7 blur=22px */
/* layout-grid-395: col=12 gap=19px align=start|center|stretch responsive-bp=1110px glass=0.8 blur=23px */
/* layout-grid-396: col=1 gap=20px align=start|center|stretch responsive-bp=1112px glass=0.0 blur=24px */
/* layout-grid-397: col=2 gap=21px align=start|center|stretch responsive-bp=1114px glass=0.1 blur=25px */
/* layout-grid-398: col=3 gap=22px align=start|center|stretch responsive-bp=1116px glass=0.2 blur=26px */
/* layout-grid-399: col=4 gap=23px align=start|center|stretch responsive-bp=1118px glass=0.3 blur=27px */
// i18n-0: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-1: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-2: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-3: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-4: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-5: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-6: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-7: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-8: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-9: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-10: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-11: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-12: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-13: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-14: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-15: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-16: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-17: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-18: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-19: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-20: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-21: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-22: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-23: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-24: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-25: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-26: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-27: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-28: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-29: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-30: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-31: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-32: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-33: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-34: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-35: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-36: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-37: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-38: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-39: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-40: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-41: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-42: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-43: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-44: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-45: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-46: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-47: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-48: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-49: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-50: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-51: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-52: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-53: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-54: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-55: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-56: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-57: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-58: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-59: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-60: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-61: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-62: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-63: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-64: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-65: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-66: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-67: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-68: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-69: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-70: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-71: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-72: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-73: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-74: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-75: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-76: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-77: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-78: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-79: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-80: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-81: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-82: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-83: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-84: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-85: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-86: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-87: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-88: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-89: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-90: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-91: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-92: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-93: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-94: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-95: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-96: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-97: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-98: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-99: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-100: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-101: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-102: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-103: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-104: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-105: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-106: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-107: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-108: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-109: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-110: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-111: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-112: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-113: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-114: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-115: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-116: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-117: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-118: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-119: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-120: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-121: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-122: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-123: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-124: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-125: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-126: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-127: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-128: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-129: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-130: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-131: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-132: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-133: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-134: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-135: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-136: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-137: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-138: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-139: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-140: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-141: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-142: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-143: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-144: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-145: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-146: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-147: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-148: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-149: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-150: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-151: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-152: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-153: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-154: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-155: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-156: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-157: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-158: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-159: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-160: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-161: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-162: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-163: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-164: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-165: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-166: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-167: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-168: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-169: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-170: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-171: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-172: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-173: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-174: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-175: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-176: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-177: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-178: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-179: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-180: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-181: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-182: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-183: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-184: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-185: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-186: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-187: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-188: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-189: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-190: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-191: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-192: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-193: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-194: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-195: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-196: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-197: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-198: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
// i18n-199: fa|en key=panel.link.sub.user.online.settings.login.logout.theme.copy.qr.import.client
"""
