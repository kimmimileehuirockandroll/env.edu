import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from shared import apply_css

apply_css()

SHEET_ID   = "1M7VPCfhe4A4PZY2e8BBgRqW2J9YGoIWypiroIi611Y0"
QUIZ_GID   = "0"
EFFECT_GID = "1746431369"


def _csv_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"


def _s(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ""
    return str(v).strip()


@st.cache_data(ttl=300)
def load_data():
    q = pd.read_csv(_csv_url(QUIZ_GID))
    q.columns = [str(c).strip() for c in q.columns]
    if "주제" in q.columns:
        q["주제"] = q["주제"].ffill()
    q = q[q["문제"].notna() & (q["문제"].astype(str).str.strip() != "")]
    quizzes = [
        {"t": _s(r.get("주제")), "q": _s(r.get("문제")), "d": _s(r.get("난이도")),
         "a": _s(r.get("답")), "e": _s(r.get("해설"))}
        for _, r in q.iterrows()
    ]

    e = pd.read_csv(_csv_url(EFFECT_GID))
    e.columns = [str(c).strip() for c in e.columns]
    pcol = next((c for c in e.columns if "긍정" in c), None)
    ncol = next((c for c in e.columns if "부정" in c), None)
    pos = [_s(x) for x in e[pcol].dropna() if _s(x)] if pcol else []
    neg = [_s(x) for x in e[ncol].dropna() if _s(x)] if ncol else []
    return quizzes, pos, neg


st.markdown("## 🧊 아이스브레이킹")
st.markdown("문제를 **앞뒤로 넘기며** 출제하고, 옆의 **타로 카드**로 긍정/부정 효과를 뽑아 진행하세요.")

try:
    quizzes, pos_effects, neg_effects = load_data()
    err = None
except Exception as ex:
    quizzes, pos_effects, neg_effects, err = [], [], [], str(ex)

if err:
    st.error(f"구글 시트를 불러오지 못했습니다: {err}")
elif not quizzes:
    st.warning("문제가 없습니다.")
else:
    DATA = json.dumps({"quizzes": quizzes, "pos": pos_effects, "neg": neg_effects}, ensure_ascii=False)

    HTML = r"""
<div id="bq-root">
  <style>
    @import url('https://cdn.jsdelivr.net/npm/galmuri/dist/galmuri.css');
    #bq-root * { box-sizing:border-box; }
    #bq-root { font-family:'Galmuri11','Noto Sans KR',monospace; }
    .bq-wrap { display:flex; gap:18px; align-items:stretch; flex-wrap:wrap; }
    .bq-quiz { flex:5 1 460px; position:relative; border:5px solid #1A1A1A; border-radius:18px;
               overflow:hidden; min-height:580px; box-shadow:0 10px 0 rgba(0,0,0,.18); }
    canvas#bqBg { position:absolute; inset:0; width:100%; height:100%; image-rendering:pixelated; }
    .bq-q-overlay { position:absolute; inset:0; display:flex; flex-direction:column; padding:22px; }
    .bq-badge { align-self:flex-start; background:#1A1A1A; color:#ffe; border:2px solid #fff;
                padding:7px 16px; border-radius:5px; font-size:18px; box-shadow:3px 3px 0 rgba(0,0,0,.35); }
    .bq-qbox { flex:1; display:flex; align-items:center; justify-content:center; margin:16px 0; }
    .bq-qtext { background:rgba(255,255,255,.88); border:4px solid #1A1A1A; border-radius:12px;
                padding:24px 26px; font-size:23px; line-height:1.7; color:#1A1A1A; text-align:center;
                max-height:360px; overflow:auto; box-shadow:5px 5px 0 rgba(0,0,0,.25); width:100%; }
    .bq-nav { display:flex; gap:12px; justify-content:center; }
    .bq-btn { font-family:inherit; font-size:19px; padding:13px 22px; border:4px solid #1A1A1A; border-radius:10px;
              background:#fff; color:#1A1A1A; cursor:pointer; box-shadow:4px 4px 0 #1A1A1A; }
    .bq-btn:active { transform:translate(2px,2px); box-shadow:2px 2px 0 #1A1A1A; }
    .bq-btn.primary { background:#FF2D6B; color:#fff; }
    .bq-count { position:absolute; top:18px; right:18px; background:rgba(26,26,26,.8); color:#fff;
                font-size:16px; padding:5px 12px; border-radius:5px; }

    /* 정답 팝업 */
    .bq-ans { position:absolute; inset:0; background:rgba(20,12,20,.93); color:#fff; display:none;
              flex-direction:column; padding:28px; overflow:auto; }
    .bq-ans.show { display:flex; }
    .bq-ans .ans-x { align-self:flex-end; background:none; border:2px solid #fff; color:#fff;
                     width:38px; height:38px; border-radius:8px; cursor:pointer; font-size:19px; }
    .bq-ans .ans-big { font-size:40px; color:#FF8FB1; margin:10px 0 18px; }
    .bq-ans .ans-exp { font-size:21px; line-height:1.8; color:#e8e8e8; }

    /* 타로 효과 카드 */
    .bq-card { flex:1 1 320px; perspective:1400px; min-height:580px; }
    .bq-card-inner { position:relative; width:100%; height:100%; min-height:580px;
                     transition:transform .7s cubic-bezier(.4,.2,.2,1); transform-style:preserve-3d; }
    .bq-card.flipped .bq-card-inner { transform:rotateY(180deg); }
    .bq-face { position:absolute; inset:0; backface-visibility:hidden; border-radius:16px;
               border:4px solid #2a1840; overflow:hidden; }
    /* 뒷면 (몽환 보라) */
    .bq-back { background:
        radial-gradient(circle at 30% 25%, #6b3fa0 0%, transparent 45%),
        radial-gradient(circle at 70% 75%, #3a1d6e 0%, transparent 50%),
        linear-gradient(160deg, #2a1450, #150a2e);
        display:flex; flex-direction:column; align-items:center; justify-content:center; cursor:pointer;
        box-shadow:0 8px 0 rgba(0,0,0,.25), inset 0 0 40px rgba(150,90,220,.35); }
    .bq-back .moon { font-size:68px; filter:drop-shadow(0 0 14px #b98cff); }
    .bq-back .title { color:#e9d8ff; font-size:24px; margin-top:14px; letter-spacing:1px; }
    .bq-back .hint { color:#b79be0; font-size:16px; margin-top:8px; }
    .bq-back .stars { position:absolute; inset:0; pointer-events:none; }
    .bq-back .st { position:absolute; width:3px; height:3px; background:#fff; box-shadow:0 0 6px #fff; opacity:.8; }
    .bq-back .frame { position:absolute; inset:8px; border:2px dashed rgba(200,170,255,.5); border-radius:12px; pointer-events:none; }

    /* 앞면 (효과 공개) */
    .bq-front { transform:rotateY(180deg); display:flex; flex-direction:column; padding:16px;
        background:linear-gradient(160deg,#241141,#160a2c); color:#f0e8ff; }
    .bq-front .fx-x { align-self:flex-end; background:none; border:2px solid #b79be0; color:#e9d8ff;
                      width:38px; height:38px; border-radius:8px; cursor:pointer; font-size:19px; }
    .bq-front .fx-label { font-size:22px; font-weight:700; margin:6px 0 14px; letter-spacing:1px; }
    .bq-front .fx-text { font-size:19px; line-height:1.85; white-space:pre-line; overflow:auto; flex:1;
                         background:rgba(0,0,0,.2); border-radius:12px; padding:16px; }
    .bq-front.pos .fx-label { color:#9af2c0; }
    .bq-front.neg .fx-label { color:#ff9ab0; }
  </style>

  <div class="bq-wrap">
    <!-- 퀴즈 -->
    <div class="bq-quiz">
      <canvas id="bqBg" width="560" height="560"></canvas>
      <div class="bq-count" id="bq-count"></div>
      <div class="bq-q-overlay">
        <div class="bq-badge" id="bq-badge"></div>
        <div class="bq-qbox"><div class="bq-qtext" id="bq-qtext"></div></div>
        <div class="bq-nav">
          <button class="bq-btn" id="bq-prev">◀ 이전</button>
          <button class="bq-btn primary" id="bq-show">👀 정답 보기</button>
          <button class="bq-btn" id="bq-next">다음 ▶</button>
        </div>
      </div>
      <div class="bq-ans" id="bq-ans">
        <button class="ans-x" id="bq-ans-x">✕</button>
        <div style="font-size:13px;color:#b79be0;">정답</div>
        <div class="ans-big" id="bq-ans-big"></div>
        <div style="font-size:13px;color:#b79be0;">해설</div>
        <div class="ans-exp" id="bq-ans-exp"></div>
      </div>
    </div>

    <!-- 타로 효과 카드 -->
    <div class="bq-card" id="bq-card">
      <div class="bq-card-inner">
        <div class="bq-face bq-back" id="bq-back">
          <div class="frame"></div>
          <div class="stars" id="bq-stars"></div>
          <div class="moon">🌙</div>
          <div class="title">효과 카드</div>
          <div class="hint">탭하여 운명을 뽑기</div>
        </div>
        <div class="bq-face bq-front" id="bq-front">
          <button class="fx-x" id="bq-fx-x">✕</button>
          <div class="fx-label" id="bq-fx-label"></div>
          <div class="fx-text" id="bq-fx-text"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
(function(){
  const DATA = __DATA__;
  const Q = DATA.quizzes, POS = DATA.pos, NEG = DATA.neg;
  const canvas = document.getElementById("bqBg"), ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  let idx = 0;

  // ── 주제별 픽셀 배경 ──
  function px(x,y,w,h,c){ ctx.fillStyle=c; ctx.fillRect(x,y,w,h); }
  function sky(a,b){ const g=ctx.createLinearGradient(0,0,0,H); g.addColorStop(0,a); g.addColorStop(1,b); ctx.fillStyle=g; ctx.fillRect(0,0,W,H); }
  function scene(topic){
    if(topic.indexOf("바다")>=0||topic.indexOf("해변")>=0||topic.indexOf("사계")>=0){
      sky("#aee3ff","#dff6ff"); px(0,H*0.66,W,H,"#f2e2b8"); // 모래
      px(0,H*0.5,W,H*0.18,"#4aa3d8"); for(let i=0;i<W;i+=24) px(i,H*0.5,12,3,"#bfe6ff"); // 물결
      px(W-90,40,42,42,"#ffd95c"); // 해
      for(let i=0;i<5;i++){ px(40+i*80,H*0.72,10,10,"#e8d49a"); } // 조개/돌
    } else if(topic.indexOf("물")>=0){
      sky("#cdeeff","#eaf8ff"); px(0,H*0.6,W,H,"#3f8fb8");
      for(let y=H*0.6;y<H;y+=14) for(let i=0;i<W;i+=28) px(i+((y/14)%2?14:0),y,14,4,"#67b3d6");
      for(let i=0;i<6;i++) px(30+i*75,H*0.5,8,8,"#bfe9ff"); // 물방울
    } else if(topic.indexOf("쓰레기")>=0){
      sky("#dfeecd","#f3f8ea"); px(0,H*0.66,W,H,"#7ec85a");
      const cols=["#9aa0a6","#4aa3ff","#ff7043","#ffd166"];
      for(let i=0;i<4;i++){ const x=70+i*100; px(x-14,H*0.66-44,28,44,"#2b2b2b"); px(x-11,H*0.66-40,22,38,cols[i]); px(x-16,H*0.66-50,32,8,"#1A1A1A"); }
    } else { // 생태(숲/동물) + 기본
      sky("#bfe8ff","#eafff0"); px(0,H*0.66,W,H,"#6fbf52");
      for(let i=0;i<6;i++){ const x=30+i*80; px(x,H*0.45,10,H*0.22,"#7b4a26"); ctx.fillStyle="#2f8f3f"; ctx.beginPath(); ctx.arc(x+5,H*0.42,20,0,6.3); ctx.fill(); }
      px(W-110,60,40,26,"#fff"); px(W-80,52,40,30,"#fff"); // 구름
    }
  }

  function makeStars(){
    const box=document.getElementById("bq-stars"); box.innerHTML="";
    for(let i=0;i<22;i++){ const s=document.createElement("div"); s.className="st";
      s.style.left=Math.random()*100+"%"; s.style.top=Math.random()*100+"%";
      s.style.opacity=(0.4+Math.random()*0.6); box.appendChild(s); }
  }

  function render(){
    const q=Q[idx];
    scene(q.t||"");
    document.getElementById("bq-badge").textContent=(q.t||"주제")+" · 난이도 "+(q.d||"?");
    document.getElementById("bq-qtext").textContent=q.q;
    document.getElementById("bq-count").textContent=(idx+1)+" / "+Q.length;
    document.getElementById("bq-ans").classList.remove("show");
  }

  document.getElementById("bq-prev").onclick=function(){ idx=(idx-1+Q.length)%Q.length; render(); };
  document.getElementById("bq-next").onclick=function(){ idx=(idx+1)%Q.length; render(); };
  document.getElementById("bq-show").onclick=function(){
    const q=Q[idx];
    document.getElementById("bq-ans-big").textContent=q.a||"—";
    document.getElementById("bq-ans-exp").textContent=q.e||"(해설 없음)";
    document.getElementById("bq-ans").classList.add("show");
  };
  document.getElementById("bq-ans-x").onclick=function(){ document.getElementById("bq-ans").classList.remove("show"); };

  // ── 효과 카드 ──
  const card=document.getElementById("bq-card");
  function drawCard(){
    const usePos = Math.random()<0.5;
    let kind = usePos?"pos":"neg";
    let pool = usePos?POS:NEG;
    if(!pool.length){ kind = usePos?"neg":"pos"; pool = usePos?NEG:POS; }
    if(!pool.length) return;
    const text = pool[Math.floor(Math.random()*pool.length)];
    const front=document.getElementById("bq-front");
    front.classList.remove("pos","neg"); front.classList.add(kind);
    document.getElementById("bq-fx-label").textContent = kind==="pos" ? "☀  긍정적 효과" : "☾  부정적 효과";
    document.getElementById("bq-fx-text").textContent = text;
    card.classList.add("flipped");
  }
  document.getElementById("bq-back").onclick=drawCard;
  document.getElementById("bq-fx-x").onclick=function(e){ e.stopPropagation(); card.classList.remove("flipped"); };

  makeStars();
  render();
})();
</script>
"""
    HTML = HTML.replace("__DATA__", DATA)
    components.html(HTML, height=650, scrolling=True)

    st.caption(f"📚 문제 {len(quizzes)}개 · 효과 카드 긍정 {len(pos_effects)} · 부정 {len(neg_effects)} (구글 시트 자동 연동, 5분 캐시)")
