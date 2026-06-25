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
st.markdown("문제를 **앞뒤로 넘기며** 출제하고, **정답이면 위(긍정) 카드 · 오답이면 아래(부정) 카드**를 뽑으세요.")

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
    .bq-quiz { flex:10 1 460px; position:relative; border:5px solid #1A1A1A; border-radius:18px;
               overflow:hidden; min-height:720px; box-shadow:0 10px 0 rgba(0,0,0,.18); }
    canvas#bqBg { position:absolute; inset:0; width:100%; height:100%; image-rendering:pixelated; }
    .bq-q-overlay { position:absolute; inset:0; display:flex; flex-direction:column; padding:22px; }
    .bq-badge { align-self:flex-start; background:#1A1A1A; color:#ffe; border:2px solid #fff;
                padding:7px 16px; border-radius:5px; font-size:18px; box-shadow:3px 3px 0 rgba(0,0,0,.35); }
    .bq-qbox { flex:1; display:flex; align-items:center; justify-content:center; margin:16px 0; }
    .bq-qtext { background:rgba(255,255,255,.88); border:4px solid #1A1A1A; border-radius:12px;
            padding:24px 26px; font-size:26px; line-height:1.7; color:#1A1A1A; text-align:center;
            white-space:pre-line; max-height:520px; overflow:auto; box-shadow:5px 5px 0 rgba(0,0,0,.25); width:100%; }
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
    .bq-ans .ans-exp { font-size:21px; line-height:1.8; color:#e8e8e8; white-space:pre-line; }

    /* ── 효과 카드 2개 (위:긍정 / 아래:부정) ── */
    .bq-cards { flex:1 1 320px; display:flex; flex-direction:column; gap:18px; min-height:720px; }
    .bq-card { perspective:1400px; flex:1; min-height:340px; }
    .bq-card-inner { position:relative; width:100%; height:100%; min-height:340px;
                     transition:transform .7s cubic-bezier(.4,.2,.2,1); transform-style:preserve-3d; }
    .bq-card.flipped .bq-card-inner { transform:rotateY(180deg); }
    .bq-face { position:absolute; inset:0; backface-visibility:hidden; border-radius:16px;
               border:4px solid #2a1840; overflow:hidden; }

    /* 뒷면 공통 */
    .bq-back { display:flex; flex-direction:column; align-items:center; justify-content:center; cursor:pointer; }
    .bq-back .moon { font-size:58px; }
    .bq-back .title { font-size:22px; margin-top:12px; letter-spacing:1px; }
    .bq-back .hint { font-size:15px; margin-top:6px; }
    .bq-back .stars { position:absolute; inset:0; pointer-events:none; }
    .bq-back .st { position:absolute; width:3px; height:3px; background:#fff; box-shadow:0 0 6px #fff; opacity:.8; }
    .bq-back .frame { position:absolute; inset:8px; border:2px dashed rgba(255,255,255,.4); border-radius:12px; pointer-events:none; }
    /* 긍정 뒷면 (금/초록 몽환) */
    .bq-back.pos { border-color:#1f5a3a; background:
        radial-gradient(circle at 30% 25%, #d9a441 0%, transparent 45%),
        radial-gradient(circle at 70% 75%, #2e8b57 0%, transparent 50%),
        linear-gradient(160deg, #15402b, #08200f);
        box-shadow:0 8px 0 rgba(0,0,0,.25), inset 0 0 40px rgba(120,220,150,.30); }
    .bq-back.pos .moon { filter:drop-shadow(0 0 14px #ffe08a); }
    .bq-back.pos .title { color:#d8ffe6; }
    .bq-back.pos .hint { color:#9be0b6; }
    /* 부정 뒷면 (보라 몽환) */
    .bq-back.neg { border-color:#2a1840; background:
        radial-gradient(circle at 30% 25%, #6b3fa0 0%, transparent 45%),
        radial-gradient(circle at 70% 75%, #3a1d6e 0%, transparent 50%),
        linear-gradient(160deg, #2a1450, #150a2e);
        box-shadow:0 8px 0 rgba(0,0,0,.25), inset 0 0 40px rgba(150,90,220,.35); }
    .bq-back.neg .moon { filter:drop-shadow(0 0 14px #b98cff); }
    .bq-back.neg .title { color:#e9d8ff; }
    .bq-back.neg .hint { color:#b79be0; }

    /* 앞면 (효과 공개) */
    .bq-front { transform:rotateY(180deg); display:flex; flex-direction:column; padding:16px; }
    .bq-front.pos { background:linear-gradient(160deg,#123524,#08200f); color:#eafff2; border-color:#1f5a3a; }
    .bq-front.neg { background:linear-gradient(160deg,#241141,#160a2c); color:#f0e8ff; }
    .bq-front .fx-x { align-self:flex-end; background:none; border:2px solid rgba(255,255,255,.6); color:#fff;
                      width:36px; height:36px; border-radius:8px; cursor:pointer; font-size:18px; }
    .bq-front .fx-label { font-size:21px; font-weight:700; margin:6px 0 12px; letter-spacing:1px; }
    .bq-front.pos .fx-label { color:#9af2c0; }
    .bq-front.neg .fx-label { color:#ff9ab0; }
    .bq-front .fx-text { font-size:18px; line-height:1.85; white-space:pre-line; overflow:auto; flex:1;
                         background:rgba(0,0,0,.2); border-radius:12px; padding:14px; }
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

    <!-- 효과 카드 2개 -->
    <div class="bq-cards">
      <!-- 긍정 (정답 시) -->
      <div class="bq-card" id="bq-card-pos">
        <div class="bq-card-inner">
          <div class="bq-face bq-back pos" id="bq-back-pos">
            <div class="frame"></div><div class="stars" id="bq-stars-pos"></div>
            <div class="moon">☀️</div>
            <div class="title">긍정 카드</div>
            <div class="hint">정답! 탭하여 뽑기</div>
          </div>
          <div class="bq-face bq-front pos">
            <button class="fx-x" id="bq-fx-x-pos">✕</button>
            <div class="fx-label">🍀 긍정적 효과</div>
            <div class="fx-text" id="bq-fx-text-pos"></div>
          </div>
        </div>
      </div>
      <!-- 부정 (오답 시) -->
      <div class="bq-card" id="bq-card-neg">
        <div class="bq-card-inner">
          <div class="bq-face bq-back neg" id="bq-back-neg">
            <div class="frame"></div><div class="stars" id="bq-stars-neg"></div>
            <div class="moon">🌙</div>
            <div class="title">부정 카드</div>
            <div class="hint">오답… 탭하여 뽑기</div>
          </div>
          <div class="bq-face bq-front neg">
            <button class="fx-x" id="bq-fx-x-neg">✕</button>
            <div class="fx-label">⚠️ 부정적 효과</div>
            <div class="fx-text" id="bq-fx-text-neg"></div>
          </div>
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

  function px(x,y,w,h,c){ ctx.fillStyle=c; ctx.fillRect(x,y,w,h); }
  function sky(a,b){ const g=ctx.createLinearGradient(0,0,0,H); g.addColorStop(0,a); g.addColorStop(1,b); ctx.fillStyle=g; ctx.fillRect(0,0,W,H); }
  function scene(topic){
    if(topic.indexOf("바다")>=0||topic.indexOf("해변")>=0||topic.indexOf("사계")>=0){
      sky("#aee3ff","#dff6ff"); px(0,H*0.66,W,H,"#f2e2b8");
      px(0,H*0.5,W,H*0.18,"#4aa3d8"); for(let i=0;i<W;i+=24) px(i,H*0.5,12,3,"#bfe6ff");
      px(W-90,40,42,42,"#ffd95c");
      for(let i=0;i<5;i++){ px(40+i*80,H*0.72,10,10,"#e8d49a"); }
    } else if(topic.indexOf("물")>=0){
      sky("#cdeeff","#eaf8ff"); px(0,H*0.6,W,H,"#3f8fb8");
      for(let y=H*0.6;y<H;y+=14) for(let i=0;i<W;i+=28) px(i+((y/14)%2?14:0),y,14,4,"#67b3d6");
      for(let i=0;i<6;i++) px(30+i*75,H*0.5,8,8,"#bfe9ff");
    } else if(topic.indexOf("쓰레기")>=0){
      sky("#dfeecd","#f3f8ea"); px(0,H*0.66,W,H,"#7ec85a");
      const cols=["#9aa0a6","#4aa3ff","#ff7043","#ffd166"];
      for(let i=0;i<4;i++){ const x=70+i*100; px(x-14,H*0.66-44,28,44,"#2b2b2b"); px(x-11,H*0.66-40,22,38,cols[i]); px(x-16,H*0.66-50,32,8,"#1A1A1A"); }
    } else {
      sky("#bfe8ff","#eafff0"); px(0,H*0.66,W,H,"#6fbf52");
      for(let i=0;i<6;i++){ const x=30+i*80; px(x,H*0.45,10,H*0.22,"#7b4a26"); ctx.fillStyle="#2f8f3f"; ctx.beginPath(); ctx.arc(x+5,H*0.42,20,0,6.3); ctx.fill(); }
      px(W-110,60,40,26,"#fff"); px(W-80,52,40,30,"#fff");
    }
  }

  function makeStars(id){
    const box=document.getElementById(id); box.innerHTML="";
    for(let i=0;i<18;i++){ const s=document.createElement("div"); s.className="st";
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

  // ── 효과 카드 2개 (각자 자기 종류만 뽑음) ──
  function setupCard(kind, pool){
    const card=document.getElementById("bq-card-"+kind);
    const back=document.getElementById("bq-back-"+kind);
    const textEl=document.getElementById("bq-fx-text-"+kind);
    const x=document.getElementById("bq-fx-x-"+kind);
    back.onclick=function(){
      if(!pool.length){ textEl.textContent="(효과 데이터 없음)"; }
      else { textEl.textContent = pool[Math.floor(Math.random()*pool.length)]; }
      card.classList.add("flipped");
    };
    x.onclick=function(e){ e.stopPropagation(); card.classList.remove("flipped"); };
  }
  setupCard("pos", POS);
  setupCard("neg", NEG);

  makeStars("bq-stars-pos");
  makeStars("bq-stars-neg");
  render();
})();
</script>
"""
    HTML = HTML.replace("__DATA__", DATA)
    components.html(HTML, height=780, scrolling=True)

    st.caption(f"📚 문제 {len(quizzes)}개 · 긍정 효과 {len(pos_effects)} · 부정 효과 {len(neg_effects)} (구글 시트 자동 연동, 5분 캐시)")
