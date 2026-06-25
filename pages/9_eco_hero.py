import streamlit as st
import streamlit.components.v1 as components
from shared import apply_css

apply_css()

st.markdown("## 🏃 플로깅 러쉬")
st.markdown("달리면서 쓰레기를 줍고(최대 3개), **헷갈리는 품목을 올바른 분리수거함**에 넣으세요! 움직이는 오염 웅덩이는 피하기.")

st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>줍go · 분류하go · 달리go!</div>
  <div class='hero-sub'>
  화면을 클릭한 뒤 플레이하세요. 쓰레기는 <b>한 번에 3개</b>까지 줍고, 수거함 위에서 <b>내려놓기</b>로 분류해요.<br>
  맞으면 시간 +2초, 틀리면 −3초(정답을 알려줘요). 움직이는 웅덩이도 피하세요!
  </div>
</div>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<div id="pr-root" style="font-family:'Noto Sans KR',sans-serif; max-width:540px; margin:0 auto;">
  <style>
    #pr-root * { box-sizing:border-box; }
    .pr-hud { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:8px; justify-content:center; align-items:center; }
    .pr-chip { background:#1A1A1A; color:#F0F0F0; border-radius:50px; padding:6px 14px; font-size:13px;
               display:flex; align-items:center; gap:6px; }
    .pr-chip b { color:#FF5C8A; font-size:14px; }
    .pr-timewrap { width:100%; height:14px; background:#E5E5E5; border-radius:999px; overflow:hidden; margin-bottom:8px; }
    .pr-timebar { height:100%; width:100%; background:linear-gradient(90deg,#FF2D6B,#FF85A1); border-radius:999px; transition:width .15s linear; }
    .pr-mission { width:100%; text-align:center; font-weight:700; font-size:14px; padding:6px; border-radius:10px;
                  margin-bottom:8px; background:#FFF2CC; color:#8A6D00; min-height:32px; display:flex; align-items:center; justify-content:center; }
    .pr-mission.active { background:#FF2D6B; color:#fff; box-shadow:0 3px 10px rgba(255,45,107,.3); }
    .pr-canvas-wrap { border-radius:14px; overflow:hidden; border:3px solid #1A1A1A;
                      box-shadow:0 6px 18px rgba(0,0,0,0.25); position:relative; }
    canvas#prCanvas { display:block; width:100%; image-rendering:pixelated; background:#7ec850; cursor:pointer; outline:none; }
    .pr-toast { position:absolute; top:10px; left:50%; transform:translateX(-50%); background:rgba(26,26,26,.92);
                color:#fff; padding:8px 16px; border-radius:10px; font-size:13px; font-weight:700; opacity:0;
                transition:opacity .2s; pointer-events:none; max-width:90%; text-align:center; }
    .pr-toast.show { opacity:1; }
    .pr-toast.good { background:rgba(27,122,67,.94); }
    .pr-toast.bad  { background:rgba(179,38,30,.94); }
    .pr-overlay { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center;
                  background:rgba(20,10,15,0.74); color:#fff; text-align:center; gap:12px; padding:16px; }
    .pr-overlay h3 { margin:0; font-size:1.4rem; color:#FF8FB1; }
    .pr-btn { font-family:'Noto Sans KR',sans-serif; padding:10px 22px; border-radius:10px; border:2px solid #1A1A1A;
              background:#FF2D6B; color:#fff; font-weight:700; cursor:pointer; box-shadow:0 3px 0 #1A1A1A; font-size:15px; }
    .pr-pad { display:none; grid-template-columns:repeat(3,52px); gap:6px; justify-content:center; margin-top:12px; }
    @media (hover:none){ .pr-pad{ display:grid; } }
    .pr-pad button { height:52px; border-radius:10px; border:2px solid #1A1A1A; background:#fff; font-size:20px; box-shadow:0 2px 0 #1A1A1A; }
    .pr-pad .sp { visibility:hidden; }
    .pr-pad button[data-act="drop"] { background:#FFE4EE; font-size:13px; font-weight:700; color:#FF2D6B; }
    /* 키캡 그림 범례 */
    .pr-legend { display:flex; gap:16px; justify-content:center; flex-wrap:wrap; margin-top:12px; }
    .pr-leg { display:flex; align-items:center; gap:7px; font-size:12.5px; color:#444; font-weight:600; }
    .kc { display:inline-flex; align-items:center; justify-content:center; background:#fff; border:2px solid #1A1A1A;
          border-radius:6px; box-shadow:0 2px 0 #1A1A1A; font-size:11px; font-weight:800; padding:3px 7px;
          min-width:26px; height:26px; line-height:1; }
    .kc-wide, .kc-space { padding:3px 12px; }
    .kc-arrows { flex-direction:column; gap:1px; height:auto; padding:3px 7px; font-size:9px; letter-spacing:1px; }
  </style>

  <div class="pr-hud">
    <div class="pr-chip">♻️ 점수 <b id="pr-score">0</b></div>
    <div class="pr-chip">🏆 최고 <b id="pr-best">0</b></div>
    <div class="pr-chip">✋ 손(<span id="pr-holdn">0</span>/3) <b id="pr-hold">없음</b></div>
  </div>
  <div class="pr-timewrap"><div class="pr-timebar" id="pr-timebar"></div></div>
  <div class="pr-mission" id="pr-mission">미션 대기 중…</div>

  <div class="pr-canvas-wrap">
    <canvas id="prCanvas" width="420" height="340" tabindex="0"></canvas>
    <div class="pr-toast" id="pr-toast"></div>
    <div class="pr-overlay" id="pr-overlay">
      <h3>🏃 플로깅 러쉬</h3>
      <div style="font-size:14px; max-width:330px;">쓰레기를 최대 3개 주워 알맞은 수거함에 넣으세요.<br>맞는 것만 자동으로 들어가요. 웅덩이와 함정 조심!</div>
      <button class="pr-btn" id="pr-start">게임 시작 ▶</button>
    </div>
  </div>

  <div class="pr-pad" id="pr-pad">
    <div class="sp"></div><button data-dir="up">▲</button><div class="sp"></div>
    <button data-dir="left">◀</button><button data-act="drop">놓기</button><button data-dir="right">▶</button>
    <div class="sp"></div><button data-dir="down">▼</button><div class="sp"></div>
  </div>

  <div class="pr-legend">
    <div class="pr-leg">
      <span class="kc kc-arrows"><span>▲</span><span>◀ ▼ ▶</span></span>
      <span>이동</span>
    </div>
    <div class="pr-leg"><span class="kc kc-wide">Shift</span><span>빠르게 달리기</span></div>
    <div class="pr-leg"><span class="kc kc-space">Space</span><span>내려놓기</span></div>
  </div>
</div>

<script>
(function() {
  const canvas = document.getElementById("prCanvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  const FIELD_BOTTOM = H - 66;
  const MAX_HOLD = 3;

  const BINS_DEF = [
    { type:"general", label:"일반",   color:"#9aa0a6" },
    { type:"plastic", label:"플라",   color:"#4aa3ff" },
    { type:"can",     label:"캔",     color:"#ff7043" },
    { type:"paper",   label:"종이",   color:"#ffd166" },
    { type:"food",    label:"음식물", color:"#46c46a" },
  ];
  const BIN_FULL = { general:"일반쓰레기", plastic:"플라스틱", can:"캔·고철", paper:"종이", food:"음식물" };

  const ITEMS = [
    { id:"shampoo",  name:"샴푸통",   bin:"plastic" },
    { id:"pet",      name:"페트병",   bin:"plastic" },
    { id:"yogurt",   name:"요구르트병", bin:"plastic" },
    { id:"drinkcan", name:"음료캔",   bin:"can" },
    { id:"tincan",   name:"통조림캔", bin:"can" },
    { id:"butane",   name:"부탄가스", bin:"can" },
    { id:"news",     name:"신문지",   bin:"paper" },
    { id:"box",      name:"택배박스", bin:"paper" },
    { id:"paperbag", name:"종이봉투", bin:"paper" },
    { id:"apple",    name:"사과심",   bin:"food" },
    { id:"banana",   name:"바나나껍질", bin:"food" },
    { id:"cabbage",  name:"배추잎",   bin:"food" },
    { id:"papercup", name:"종이컵",   bin:"general", trap:true },
    { id:"eggshell", name:"계란껍질", bin:"general", trap:true },
    { id:"glass",    name:"깨진유리", bin:"general", trap:true },
  ];
  const ITEM_BY_ID = {}; ITEMS.forEach(it => ITEM_BY_ID[it.id]=it);

  function R(x,y,w,h,c){ ctx.fillStyle=c; ctx.fillRect(x|0,y|0,w,h); }
  const ICON = {
    shampoo(cx,cy){ R(cx-6,cy-10,12,18,"#5ec8e8"); R(cx-3,cy-13,6,4,"#2e8b9e"); R(cx-6,cy-2,12,4,"#ffffff"); },
    pet(cx,cy){ R(cx-5,cy-8,10,16,"#bfe9ff"); R(cx-2,cy-12,4,5,"#7fd0e8"); R(cx-3,cy-13,6,2,"#2e8b9e"); },
    yogurt(cx,cy){ R(cx-5,cy-7,10,14,"#ffffff"); R(cx-5,cy-7,10,3,"#ff5d6c"); R(cx-4,cy+4,8,2,"#e0e0e0"); },
    drinkcan(cx,cy){ R(cx-5,cy-9,10,18,"#ff5d6c"); R(cx-5,cy-9,10,3,"#cfcfcf"); R(cx-5,cy+6,10,3,"#cfcfcf"); R(cx-3,cy-3,6,5,"#ffffff"); },
    tincan(cx,cy){ R(cx-6,cy-7,12,15,"#c9ccd1"); R(cx-6,cy-7,12,3,"#9aa0a6"); R(cx-4,cy-2,8,6,"#ffd166"); },
    butane(cx,cy){ R(cx-4,cy-11,8,20,"#f4a742"); R(cx-2,cy-14,4,4,"#888"); R(cx-4,cy-1,8,3,"#b5731f"); },
    news(cx,cy){ R(cx-8,cy-8,16,16,"#f2f0e6"); R(cx-6,cy-6,12,2,"#555"); R(cx-6,cy-2,12,2,"#555"); R(cx-6,cy+2,8,2,"#555"); },
    box(cx,cy){ R(cx-9,cy-7,18,15,"#c79a5b"); R(cx-9,cy-1,18,2,"#8a5a3a"); R(cx-1,cy-7,2,15,"#8a5a3a"); },
    paperbag(cx,cy){ R(cx-6,cy-8,12,16,"#d9b37a"); R(cx-4,cy-11,3,4,"#b5895a"); R(cx+1,cy-11,3,4,"#b5895a"); },
    apple(cx,cy){ R(cx-3,cy-6,6,12,"#f2efe0"); R(cx-5,cy-3,10,5,"#e6e2cf"); R(cx-1,cy-10,2,4,"#7b4a26"); R(cx,cy-11,3,2,"#3ad07f"); },
    banana(cx,cy){ R(cx-7,cy-3,14,5,"#ffd84a"); R(cx-9,cy-6,5,5,"#e6b800"); R(cx+5,cy+1,5,5,"#a87f1f"); },
    cabbage(cx,cy){ ctx.fillStyle="#7ec84a"; ctx.beginPath(); ctx.arc(cx,cy,9,0,6.3); ctx.fill(); R(cx-2,cy-9,4,18,"#a6e06a"); },
    papercup(cx,cy){ R(cx-6,cy-9,12,16,"#ffffff"); R(cx-6,cy-9,12,3,"#4aa3ff"); R(cx-5,cy+5,10,2,"#cfcfcf"); R(cx-7,cy-9,2,16,"#e0e0e0"); },
    eggshell(cx,cy){ ctx.fillStyle="#fff7ec"; ctx.beginPath(); ctx.arc(cx,cy,8,0,6.3); ctx.fill(); R(cx-8,cy-1,16,3,"#d9cdbb"); R(cx-3,cy-2,2,4,"#d9cdbb"); R(cx+2,cy-1,2,3,"#d9cdbb"); },
    glass(cx,cy){ ctx.fillStyle="#a9e7ef"; ctx.beginPath(); ctx.moveTo(cx-8,cy+7); ctx.lineTo(cx-2,cy-9); ctx.lineTo(cx+3,cy+7); ctx.fill();
                  ctx.beginPath(); ctx.moveTo(cx+1,cy+7); ctx.lineTo(cx+7,cy-4); ctx.lineTo(cx+9,cy+7); ctx.fill(); },
  };
  function drawIcon(id, cx, cy){ (ICON[id]||ICON.box)(cx,cy); }

  let best=0, state="idle";
  let score, timeLeft, maxTime, player, items, bins, hazards, keys, lastTs;
  let mission, missionTimer, flash, hazardTimer, hitCooldown, prevBin, toastTimer;

  function rand(a,b){ return Math.random()*(b-a)+a; }

  function buildBins(){
    bins=[]; const n=BINS_DEF.length, slotW=W/n;
    BINS_DEF.forEach(function(b,i){
      bins.push({ type:b.type, label:b.label, color:b.color, x:i*slotW+slotW/2, y:H-30, w:slotW-8, h:56 });
    });
  }

  function reset(){
    score=0; maxTime=45; timeLeft=45;
    player={ x:W/2, y:FIELD_BOTTOM/2, size:18, speed:140, dir:1, hold:[] };
    items=[]; hazards=[]; keys={}; mission=null; missionTimer=8; flash=null;
    hazardTimer=0; hitCooldown=0; prevBin=null; toastTimer=0;
    buildBins();
    for(let i=0;i<5;i++) spawnItem();
    for(let i=0;i<2;i++) spawnHazard();
    updateHUD();
  }

  function pickItemId(){
    const traps=ITEMS.filter(i=>i.trap), normals=ITEMS.filter(i=>!i.trap);
    const pool=(Math.random()<0.3)?traps:normals;
    return pool[Math.floor(Math.random()*pool.length)].id;
  }
  function spawnItem(){ items.push({ x:rand(24,W-24), y:rand(24,FIELD_BOTTOM-30), id:pickItemId(), bob:rand(0,6.28), cool:0 }); }
  function spawnHazard(){ hazards.push({ x:rand(40,W-40), y:rand(40,FIELD_BOTTOM-40), r:rand(13,20), vx:rand(-30,30), vy:rand(-30,30) }); }

  function showToast(msg,kind){ const t=document.getElementById("pr-toast"); t.textContent=msg; t.className="pr-toast show "+(kind||""); toastTimer=1.6; }

  function holdNames(){ return player.hold.map(id=>ITEM_BY_ID[id].name); }

  function updateHUD(){
    document.getElementById("pr-score").textContent=score;
    document.getElementById("pr-best").textContent=best;
    document.getElementById("pr-holdn").textContent=player?player.hold.length:0;
    const names=player?holdNames():[];
    document.getElementById("pr-hold").textContent = names.length ? names.join(", ") : "없음";
    document.getElementById("pr-timebar").style.width=Math.max(0,Math.min(100,timeLeft/maxTime*100))+"%";
    const mEl=document.getElementById("pr-mission");
    if(mission){ mEl.classList.add("active"); mEl.textContent="🎯 미션: "+BIN_FULL[mission.type]+"만! ("+Math.ceil(mission.left)+"초)  콤보 "+mission.combo; }
    else { mEl.classList.remove("active"); mEl.textContent="다음 미션까지 "+Math.ceil(missionTimer)+"초…"; }
  }

  const KEYMAP={ArrowUp:"up",ArrowDown:"down",ArrowLeft:"left",ArrowRight:"right"};
  let spaceHeld=false;
  window.addEventListener("keydown",function(e){
    if(KEYMAP[e.key]){ keys[KEYMAP[e.key]]=true; e.preventDefault(); }
    else if(e.key==="Shift"){ keys.boost=true; }
    else if(e.code==="Space"||e.key===" "){ e.preventDefault(); if(!spaceHeld){ spaceHeld=true; dropFront(); } }
  });
  window.addEventListener("keyup",function(e){
    if(KEYMAP[e.key]){ keys[KEYMAP[e.key]]=false; }
    else if(e.key==="Shift"){ keys.boost=false; }
    else if(e.code==="Space"||e.key===" "){ spaceHeld=false; }
  });
  canvas.addEventListener("click",function(){ canvas.focus(); });
  // 모바일 패드: 방향 + 내려놓기 버튼
  document.querySelectorAll("#pr-pad button[data-dir]").forEach(function(b){
    const dir=b.getAttribute("data-dir");
    const on=function(e){e.preventDefault();keys[dir]=true;}, off=function(e){e.preventDefault();keys[dir]=false;};
    b.addEventListener("touchstart",on); b.addEventListener("touchend",off);
    b.addEventListener("mousedown",on); b.addEventListener("mouseup",off); b.addEventListener("mouseleave",off);
  });
  const dropBtn=document.querySelector("#pr-pad button[data-act='drop']");
  if(dropBtn){ dropBtn.addEventListener("touchstart",function(e){e.preventDefault();dropFront();});
               dropBtn.addEventListener("mousedown",function(e){e.preventDefault();dropFront();}); }

  function circleHit(ax,ay,ar,bx,by,br){ const dx=ax-bx,dy=ay-by; return dx*dx+dy*dy<(ar+br)*(ar+br); }

  function startMission(){ const k=BINS_DEF[Math.floor(Math.random()*BINS_DEF.length)].type; mission={ type:k, left:9, combo:0 }; }

  function depositOne(it){
    let gain=2, pts=10;
    if(mission && mission.type===it.bin){ mission.combo+=1; pts=25; gain=3; flash={c:"rgba(58,208,127,",a:0.32}; }
    else { flash={c:"rgba(58,208,127,",a:0.20}; }
    score+=pts; timeLeft=Math.min(maxTime,timeLeft+gain);
  }

  function curBinAt(){
    for(const b of bins){ if(player.x>b.x-b.w/2 && player.x<b.x+b.w/2 && player.y>b.y-b.h/2) return b; }
    return null;
  }

  // Space = 액션키. 통 위면 맞는 것만 투입(틀린 건 보유), 땅이면 맨 앞 품목 내려놓기.
  function dropFront(){
    if(state!=="play" || player.hold.length===0) return;
    const bin=curBinAt();
    if(bin){
      let names=[];
      for(let i=player.hold.length-1;i>=0;i--){
        const it=ITEM_BY_ID[player.hold[i]];
        if(it.bin===bin.type){ depositOne(it); names.unshift(it.name); player.hold.splice(i,1); }
      }
      if(names.length) showToast("✅ "+names.join(", ")+" → "+BIN_FULL[bin.type], "good");
      else showToast("🚫 이 통엔 맞는 게 없어요!", "bad");
    } else {
      const id=player.hold.shift();
      items.push({ x:player.x, y:Math.min(player.y, FIELD_BOTTOM-30), id:id, bob:0, cool:0.7 });
      showToast("🔽 "+ITEM_BY_ID[id].name+" 내려놓음", "");
    }
    updateHUD();
  }

  function update(dt){
    let vx=0,vy=0;
    if(keys.up)vy-=1; if(keys.down)vy+=1;
    if(keys.left){vx-=1;player.dir=-1;} if(keys.right){vx+=1;player.dir=1;}
    const len=Math.hypot(vx,vy)||1;
    const sp=player.speed*(keys.boost?1.75:1);
    player.x+=(vx/len)*sp*dt; player.y+=(vy/len)*sp*dt;
    player.x=Math.max(player.size/2,Math.min(W-player.size/2,player.x));
    player.y=Math.max(player.size/2,Math.min(H-player.size/2,player.y));

    // 줍기 (3개 미만 + 내려놓은 직후 쿨다운 지난 것만)
    items.forEach(function(it){ if(it.cool>0) it.cool-=dt; });
    if(player.hold.length<MAX_HOLD){
      for(let i=items.length-1;i>=0;i--){
        if(items[i].cool>0) continue;
        if(circleHit(player.x,player.y,player.size/2,items[i].x,items[i].y,12)){
          player.hold.push(items[i].id); items.splice(i,1); spawnItem(); updateHUD();
          if(player.hold.length>=MAX_HOLD) break;
        }
      }
    }

    // (수거함 투입은 Space 액션키로 처리 — dropFront)

    // 웅덩이 이동 + 충돌
    hazards.forEach(function(h){
      h.x+=h.vx*dt; h.y+=h.vy*dt;
      if(h.x<h.r||h.x>W-h.r) h.vx*=-1;
      if(h.y<h.r||h.y>FIELD_BOTTOM-h.r) h.vy*=-1;
    });
    hitCooldown-=dt;
    if(hitCooldown<=0){
      for(const h of hazards){
        if(circleHit(player.x,player.y,player.size/2,h.x,h.y,h.r*0.8)){
          timeLeft-=3; hitCooldown=0.9; flash={c:"rgba(255,45,107,",a:0.4};
          showToast("💦 웅덩이! -3초", "bad"); break;
        }
      }
    }
    hazardTimer+=dt;
    if(hazardTimer>13 && hazards.length<5){ spawnHazard(); hazardTimer=0; }

    // 미션
    if(mission){ mission.left-=dt; if(mission.left<=0){ mission=null; missionTimer=rand(8,12); } }
    else { missionTimer-=dt; if(missionTimer<=0) startMission(); }

    if(flash){ flash.a-=dt*0.8; if(flash.a<=0) flash=null; }
    if(toastTimer>0){ toastTimer-=dt; if(toastTimer<=0) document.getElementById("pr-toast").classList.remove("show"); }

    timeLeft-=dt;
    if(timeLeft<=0){ timeLeft=0; endGame(); return; }
    updateHUD();
  }

  function label(text,x,y){
    ctx.font="bold 10px 'Noto Sans KR',sans-serif"; ctx.textAlign="center"; ctx.textBaseline="middle";
    const w=ctx.measureText(text).width+8;
    ctx.fillStyle="rgba(26,26,26,.82)"; ctx.fillRect(x-w/2,y-7,w,14);
    ctx.fillStyle="#fff"; ctx.fillText(text,x,y);
  }

  function drawBins(){
    bins.forEach(function(b){
      R(b.x-b.w/2,b.y-b.h/2,b.w,b.h,"#2b2b2b");
      R(b.x-b.w/2+3,b.y-b.h/2+3,b.w-6,b.h-6,b.color);
      R(b.x-b.w/2-2,b.y-b.h/2-6,b.w+4,8,"#1A1A1A");
      ctx.fillStyle="#1A1A1A"; ctx.font="bold 12px 'Noto Sans KR',sans-serif"; ctx.textAlign="center"; ctx.textBaseline="middle";
      ctx.fillText(b.label,b.x,b.y+6);
      if(mission && mission.type===b.type){ ctx.strokeStyle="#fff"; ctx.lineWidth=3; ctx.strokeRect(b.x-b.w/2-3,b.y-b.h/2-9,b.w+6,b.h+12); }
    });
  }

  function drawHazards(){
    hazards.forEach(function(h){
      ctx.fillStyle="#1A1A1A"; ctx.beginPath(); ctx.ellipse(h.x,h.y,h.r,h.r*0.7,0,0,6.3); ctx.fill();
      ctx.fillStyle="rgba(120,80,160,.6)"; ctx.beginPath(); ctx.ellipse(h.x-h.r*0.3,h.y-h.r*0.2,h.r*0.4,h.r*0.25,0,0,6.3); ctx.fill();
    });
  }

  function drawPlayer(){
    const s=player.size,x=player.x-s/2,y=player.y-s/2;
    R(x+3,y+2,s-6,s-2,"#2e8b57"); R(x+1,y+6,s-2,s-10,"#3ad07f");
    R(player.dir>0?x+s-7:x+3,y+6,3,3,"#fff"); R(player.dir>0?x+s-6:x+4,y+7,1,1,"#1A1A1A");
    // 들고 있는 것 머리 위에 나란히
    player.hold.forEach(function(id,i){ drawIcon(id, player.x + (i-(player.hold.length-1)/2)*16, player.y-s-4); });
  }

  function loop(ts){
    if(state!=="play") return;
    if(!lastTs)lastTs=ts; let dt=(ts-lastTs)/1000; lastTs=ts; if(dt>0.05)dt=0.05;
    update(dt); if(state!=="play") return;

    ctx.fillStyle="#7ec850"; ctx.fillRect(0,0,W,H);
    for(let gx=0;gx<W;gx+=40)for(let gy=0;gy<FIELD_BOTTOM;gy+=40){ if(((gx+gy)/40)%2===0){ctx.fillStyle="#74bd48";ctx.fillRect(gx,gy,40,40);} }
    R(0,FIELD_BOTTOM,W,H-FIELD_BOTTOM,"#5a6b3a");

    items.forEach(function(it){ it.bob+=dt*4; const yy=it.y+Math.sin(it.bob)*2; drawIcon(it.id,it.x,yy); label(ITEM_BY_ID[it.id].name,it.x,yy+18); });
    drawHazards();
    drawBins();
    drawPlayer();
    if(flash){ ctx.fillStyle=flash.c+Math.max(0,flash.a)+")"; ctx.fillRect(0,0,W,H); }
    requestAnimationFrame(loop);
  }

  function startGame(){
    reset(); state="play"; lastTs=0;
    document.getElementById("pr-overlay").style.display="none";
    document.getElementById("pr-toast").classList.remove("show");
    canvas.focus(); requestAnimationFrame(loop);
  }
  function endGame(){
    state="over"; if(score>best)best=score; updateHUD();
    const ov=document.getElementById("pr-overlay"); ov.style.display="flex";
    ov.innerHTML="<h3>⏱️ 시간 종료!</h3>"+
      "<div style='font-size:15px;'>분리수거 점수: <b style='color:#FF8FB1;'>"+score+"</b></div>"+
      "<div style='font-size:13px;color:#ccc;'>최고 점수: "+best+"</div>"+
      "<button class='pr-btn' id='pr-restart'>다시 하기 ↺</button>";
    document.getElementById("pr-restart").addEventListener("click", startGame);
  }

  document.getElementById("pr-start").addEventListener("click", startGame);
  ctx.fillStyle="#7ec850"; ctx.fillRect(0,0,W,H);
})();
</script>
"""

components.html(GAME_HTML, height=640, scrolling=False)

st.caption("💡 팁: 쓰레기를 3개까지 줍고, 알맞은 수거함 위에서 Space로 차례대로 내려놓으세요. 틀린 통이면 도로 바닥에 놓일 뿐 시간은 안 깎여요. Shift로 달리면 더 빠릅니다!")
