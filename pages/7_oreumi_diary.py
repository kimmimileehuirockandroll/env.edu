import streamlit as st
import streamlit.components.v1 as components
from shared import apply_css, lesson_flow

apply_css()

st.markdown("## 🦌 오름이와 마른 샘물의 비밀")

lesson_flow(
    "oreumi",
    concept=[
        {"title": "📘 Chapter 1 · 환경 문제는 왜 복잡할까?", "body": """
<p style='line-height:1.8'>
환경 문제는 대부분 <b>'증상'과 '원인'이 다릅니다</b>. 샘물이 마르는 것은 눈에 보이는 <b>증상</b>일 뿐,
진짜 <b>원인</b>은 그 뒤에 숨어 있어요. 게다가 원인은 보통 <b>하나가 아니라 여럿(다인과)</b>이
얽혀 있습니다.
</p>
<ul style='line-height:1.9; color:var(--text-muted)'>
<li>가뭄·기후변화 같은 <b>자연적 요인</b></li>
<li>상류의 무단 용수 사용 같은 <b>인간 활동</b></li>
<li>외래종 유입 같은 <b>생태적 교란</b></li>
</ul>
<p style='color:var(--text-caption); font-size:.85rem'>그래서 "누구 탓"이라고 단정하기 전에 <b>추적</b>이 필요합니다.</p>
"""},
        {"title": "📗 Chapter 2 · 원인을 추적하는 방법", "body": """
<p style='line-height:1.8'>
과학적 문제 해결은 <b>탐정의 수사</b>와 비슷해요. 증거를 모으고, 가설을 세우고, 검증합니다.
</p>
<ul style='line-height:1.9; color:var(--text-muted)'>
<li><b>① 관찰:</b> 현장을 직접 살피기 (샘물 상류를 따라가 보기)</li>
<li><b>② 자료:</b> 데이터 찾기 (강수량 기록, 통계)</li>
<li><b>③ 증언:</b> 사람들에게 묻기 (마을 어른의 경험)</li>
<li><b>④ 검증:</b> 여러 단서를 맞춰 가설을 확인·기각하기</li>
</ul>
<p style='color:var(--text-caption); font-size:.85rem'>💡 한 가지 증거만으로 결론짓지 않는 것이 중요해요.</p>
"""},
        {"title": "📙 Chapter 3 · 갈등을 조율해 해결하기", "body": """
<p style='line-height:1.8'>
원인을 찾아도 끝이 아닙니다. 대부분의 환경 문제엔 <b>이해관계자(관련된 사람들)</b>가 있어요.
샘물을 많이 쓴 펜션 사장에게도 <b>사정</b>이 있죠. 그래서 해결 방식이 여럿입니다.
</p>
<ul style='line-height:1.9; color:var(--text-muted)'>
<li><b>설득:</b> 데이터를 보여주며 차분히 협조를 구하기 (관계 유지)</li>
<li><b>규제·신고:</b> 제도로 강제하기 (빠르지만 반발 가능)</li>
<li><b>타협:</b> 양쪽 이익을 함께 살리는 방법 찾기 (지원금 연계 등)</li>
</ul>
<p style='color:var(--text-caption); font-size:.85rem'>🎯 문제: 곶자왈 샘물이 마르는 진짜 원인은? 그리고 어떻게 해결할까?</p>
"""},
    ],
    discuss=[
        "당신은 어떤 단서로 원인을 좁혀갔나요?",
        "원인 제공자(펜션)와의 갈등을 어떻게 풀었나요? 설득·신고·타협 중 무엇이 나았을까요?",
        "환경 문제 해결에서 '증거(데이터)'와 '관계(설득)' 중 무엇이 더 중요할까요?",
        "우리 주변에서 원인을 추적해볼 만한 환경 변화가 있나요?",
    ],
    present="""
<div class='eco-card'>
<b style='color:var(--accent-primary)'>🎤 발표: 사건 해결 스토리</b>
<ul style='color:var(--text-muted); line-height:1.8'>
<li>내가 밝혀낸 <b>원인</b>과 결정적 단서</li>
<li>선택한 <b>해결 방식</b>과 그 결과(엔딩)</li>
<li>현실에 적용할 교훈 한 가지</li>
</ul>
</div>
""",
)

st.markdown("곶자왈 요정 **오름이**와 함께 말라가는 샘물의 원인을 추적하는 5장 분량의 픽셀 비주얼노블입니다.")

st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🔍 사건을 추적하세요</div>
  <div class='hero-sub'>
  대화와 선택으로 이야기가 진행됩니다. 선택에 따라 오름이와의 호감도, 그리고 환경실천도가 달라지고 결말이 바뀝니다.
  </div>
</div>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<div id="vn-root" style="font-family:'Press Start 2P','Noto Sans KR',monospace; max-width:760px; margin:0 auto;">
  <style>
    #vn-root * { box-sizing: border-box; }
    #vn-root { --vn-accent: #FF2D6B; }
    .vn-hud { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:10px; font-family:'Noto Sans KR',sans-serif; }
    .vn-chip {
      background:#1A1A1A; color:#F0F0F0; border-radius:50px; padding:6px 14px;
      font-size:13px; display:flex; align-items:center; gap:6px;
    }
    .vn-chip b { color:#FF5C8A; font-size:14px; }
    .vn-stage-wrap {
      position:relative; border-radius:14px; overflow:hidden; border:3px solid #1A1A1A;
      box-shadow:0 6px 18px rgba(0,0,0,0.25);
    }
    canvas#vnCanvas { display:block; width:100%; image-rendering: pixelated; background:#222; }
    .vn-chapter-tag {
      position:absolute; top:8px; left:8px; background:rgba(0,0,0,0.55); color:#FFD9E6;
      font-size:11px; padding:4px 10px; border-radius:6px; font-family:'Noto Sans KR',sans-serif;
      letter-spacing:.5px;
    }
    .vn-textbox {
      margin-top:-6px; background:#1A1A1A; color:#F0F0F0; border:3px solid #FF5C8A;
      border-radius:0 0 12px 12px; padding:14px 16px; min-height:64px;
      font-family:'Noto Sans KR',sans-serif; font-size:14.5px; line-height:1.6; position:relative;
    }
    .vn-speaker { color:#FF8FB1; font-weight:700; font-size:12px; margin-bottom:4px; letter-spacing:.5px; }
    .vn-skip-hint { position:absolute; right:10px; bottom:8px; font-size:10px; color:#777; }
    .vn-choices { display:flex; flex-direction:column; gap:8px; margin-top:12px; }
    .vn-choice-btn {
      font-family:'Noto Sans KR',sans-serif; text-align:left; padding:10px 14px; border-radius:8px;
      border:2px solid #1A1A1A; background:#fff; cursor:pointer; font-size:14px; font-weight:600;
      box-shadow:0 3px 0 #1A1A1A; transition: all .1s; color:#1A1A1A;
    }
    .vn-choice-btn:hover { background:#FFE4EE; border-color:#FF2D6B; transform:translateY(1px); box-shadow:0 2px 0 #1A1A1A; }
    .vn-choice-btn:disabled { opacity:.4; cursor:not-allowed; }
    .vn-next-btn {
      margin-top:12px; padding:10px 18px; border-radius:8px; border:2px solid #1A1A1A;
      background:#FF2D6B; color:#fff; font-weight:700; cursor:pointer; box-shadow:0 3px 0 #1A1A1A;
      font-family:'Noto Sans KR',sans-serif; font-size:14px;
    }
    .vn-restart-btn { margin-top:10px; }
  </style>

  <div class="vn-hud">
    <div class="vn-chip">💗 호감도 <b id="vn-affinity">50</b></div>
    <div class="vn-chip">🌱 환경실천도 <b id="vn-eco">50</b></div>
  </div>

  <div class="vn-stage-wrap">
    <canvas id="vnCanvas" width="480" height="280"></canvas>
    <div class="vn-chapter-tag" id="vn-chapter-tag">1장 · 마른 샘물</div>
  </div>
  <div class="vn-textbox">
    <div class="vn-speaker" id="vn-speaker">오름이</div>
    <div id="vn-text"></div>
    <div class="vn-skip-hint">텍스트 클릭: 빠르게 보기</div>
  </div>
  <div class="vn-choices" id="vn-choices"></div>
</div>

<script>
(function() {
  const canvas = document.getElementById("vnCanvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;

  const BACKDROPS = {
    spring: { sky: ["#cfe8ff", "#eaf7ff"], ground: "#3f7d3f", accent: "#2f5f33" },
    village: { sky: ["#ffe9c7", "#fff6e8"], ground: "#9c8a63", accent: "#6e5d3f" },
    pension: { sky: ["#ffd9c2", "#ffeede"], ground: "#8a8a8a", accent: "#5a5a5a" },
    restore: { sky: ["#cdeedd", "#eafff3"], ground: "#4d8f55", accent: "#2f5f33" },
    epilogue: { sky: ["#bfe3ff", "#f3fbff"], ground: "#3f9d6a", accent: "#246b46" },
  };

  const MOODS = {
    normal:  { eye: "•", mouth: "flat",  tint: "#caa06b" },
    happy:   { eye: "^", mouth: "smile", tint: "#d7b07a" },
    worried: { eye: "o", mouth: "wave",  tint: "#b89060" },
    angryish:{ eye: "><", mouth: "frown",tint: "#a87f55" },
  };

  let bobFrame = 0;

  function drawBackdrop(key) {
    const b = BACKDROPS[key] || BACKDROPS.spring;
    const grad = ctx.createLinearGradient(0, 0, 0, H * 0.6);
    grad.addColorStop(0, b.sky[0]);
    grad.addColorStop(1, b.sky[1]);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H * 0.62);

    ctx.fillStyle = b.ground;
    ctx.fillRect(0, H * 0.6, W, H * 0.4);
    ctx.fillStyle = b.accent;
    for (let i = 0; i < 14; i++) {
      const x = (i * 47 + 13) % W;
      const y = H * 0.6 + ((i * 29) % (H * 0.35));
      ctx.fillRect(x, y, 6, 6);
    }

    if (key === "spring") {
      ctx.fillStyle = "#9fd6e8";
      ctx.fillRect(W * 0.32, H * 0.66, W * 0.36, H * 0.18);
      ctx.fillStyle = "#6fb8cf";
      ctx.fillRect(W * 0.34, H * 0.7, W * 0.32, 4);
      for (let i = 0; i < 5; i++) {
        ctx.fillStyle = "#2f5f33";
        ctx.fillRect(40 + i * 80, H * 0.5, 8, H * 0.16);
        ctx.beginPath();
        ctx.arc(44 + i * 80, H * 0.46, 16, 0, Math.PI * 2);
        ctx.fill();
      }
    } else if (key === "village") {
      ctx.fillStyle = "#caa873";
      ctx.fillRect(60, H * 0.46, 70, H * 0.2);
      ctx.fillStyle = "#8a5a3a";
      ctx.fillRect(60, H * 0.4, 70, 14);
      ctx.fillStyle = "#caa873";
      ctx.fillRect(W - 150, H * 0.5, 60, H * 0.16);
      ctx.fillStyle = "#8a5a3a";
      ctx.fillRect(W - 150, H * 0.44, 60, 12);
    } else if (key === "pension") {
      ctx.fillStyle = "#e3d3c2";
      ctx.fillRect(W * 0.25, H * 0.32, W * 0.5, H * 0.32);
      ctx.fillStyle = "#a9846a";
      ctx.fillRect(W * 0.22, H * 0.26, W * 0.56, 12);
      ctx.fillStyle = "#5a8fb0";
      ctx.fillRect(W * 0.32, H * 0.42, 30, 26);
      ctx.fillRect(W * 0.58, H * 0.42, 30, 26);
      ctx.fillStyle = "#3a3a3a";
      ctx.fillRect(W * 0.62, H * 0.56, 60, 12);
      ctx.fillStyle = "#cfe0ea";
      for (let i = 0; i < 3; i++) {
        ctx.fillRect(W * 0.63 + i * 18, H * 0.5, 6, 10);
      }
    } else if (key === "restore") {
      for (let i = 0; i < 4; i++) {
        ctx.fillStyle = "#2f5f33";
        ctx.fillRect(50 + i * 100, H * 0.5, 8, H * 0.18);
        ctx.beginPath();
        ctx.arc(54 + i * 100, H * 0.46, 14, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.fillStyle = "#9fd6e8";
      ctx.fillRect(W * 0.38, H * 0.7, W * 0.24, H * 0.12);
    } else if (key === "epilogue") {
      for (let i = 0; i < 6; i++) {
        ctx.fillStyle = "#246b46";
        ctx.fillRect(20 + i * 75, H * 0.48, 8, H * 0.2);
        ctx.beginPath();
        ctx.arc(24 + i * 75, H * 0.44, 16, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.fillStyle = "#9fe0ea";
      ctx.fillRect(W * 0.3, H * 0.68, W * 0.4, H * 0.18);
    }
  }

  function drawSprite(mood) {
    const m = MOODS[mood] || MOODS.normal;
    const bob = Math.sin(bobFrame / 18) * 4;
    const cx = W * 0.78, cy = H * 0.52 + bob;

    ctx.fillStyle = m.tint;
    ctx.beginPath();
    ctx.ellipse(cx, cy, 34, 38, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = m.tint;
    ctx.beginPath();
    ctx.moveTo(cx - 26, cy - 30);
    ctx.lineTo(cx - 38, cy - 56);
    ctx.lineTo(cx - 14, cy - 38);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(cx + 26, cy - 30);
    ctx.lineTo(cx + 38, cy - 56);
    ctx.lineTo(cx + 14, cy - 38);
    ctx.fill();

    ctx.fillStyle = "#fff5e8";
    ctx.beginPath();
    ctx.ellipse(cx, cy + 6, 16, 18, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#1A1A1A";
    ctx.font = "16px monospace";
    ctx.textAlign = "center";
    if (mood === "angryish") {
      ctx.fillText(">", cx - 11, cy - 4);
      ctx.fillText("<", cx + 11, cy - 4);
    } else if (mood === "worried") {
      ctx.beginPath(); ctx.arc(cx - 10, cy - 4, 3, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(cx + 10, cy - 4, 3, 0, Math.PI * 2); ctx.fill();
    } else {
      ctx.fillRect(cx - 12, cy - 5, 4, 4);
      ctx.fillRect(cx + 8, cy - 5, 4, 4);
    }

    ctx.strokeStyle = "#1A1A1A";
    ctx.lineWidth = 2;
    ctx.beginPath();
    if (mood === "happy") {
      ctx.arc(cx, cy + 12, 8, 0, Math.PI);
    } else if (mood === "worried") {
      ctx.moveTo(cx - 8, cy + 18); ctx.quadraticCurveTo(cx, cy + 12, cx + 8, cy + 18);
    } else if (mood === "angryish") {
      ctx.moveTo(cx - 8, cy + 16); ctx.lineTo(cx + 8, cy + 16);
    } else {
      ctx.moveTo(cx - 7, cy + 15); ctx.lineTo(cx + 7, cy + 15);
    }
    ctx.stroke();
  }

  let currentBackdrop = "spring";
  let currentMood = "normal";

  function loop() {
    bobFrame++;
    drawBackdrop(currentBackdrop);
    drawSprite(currentMood);
    requestAnimationFrame(loop);
  }
  loop();

  // ── Story data ──────────────────────────────
  const SCENES = [
    {
      tag: "1장 · 마른 샘물",
      backdrop: "spring",
      mood: "worried",
      lines: [
        "오름이: \"저기 봐, 샘물이 이상해... 일주일 전보다 절반도 안 남았어.\"",
        "오름이: \"동물들도 요즘 물 마시러 더 멀리까지 가더라. 뭔가 이상한 일이 벌어지고 있어.\"",
        "오름이: \"네가 같이 원인을 찾아줄 수 있을까?\""
      ],
      choices: [
        { text: "샘물 상류까지 직접 따라가본다", affinity: 6, eco: 5, reply: "오름이: \"오, 발로 직접 확인하는 타입이구나. 좋아, 따라와!\"" },
        { text: "마을 기록보관소에서 강수량 자료를 찾아본다", affinity: 4, eco: 7, reply: "오름이: \"데이터로 접근하는 것도 좋지. 침착한 스타일이네.\"" },
        { text: "마을 어르신들께 옛날 샘물 얘기를 여쭤본다", affinity: 7, eco: 3, reply: "오름이: \"사람들 얘기부터 듣는 거 좋아, 단서가 거기 숨어있을 때가 많거든.\"" },
      ],
    },
    {
      tag: "2장 · 단서 추적",
      backdrop: "village",
      mood: "normal",
      lines: [
        "오름이: \"단서를 모아보니 의심되는 게 세 가지야.\"",
        "오름이: \"상류에 새로 지어진 펜션, 요즘 부쩍 줄어든 강수량, 그리고 최근에 들어온 낯선 식물.\"",
        "오름이: \"어떤 쪽부터 캐볼래?\""
      ],
      choices: [
        { text: "펜션 쪽 용수 사용량을 확인해본다", affinity: 5, eco: 6, reply: "오름이: \"펜션이 좀 의심스럽긴 했어. 가보자.\"" },
        { text: "기후 데이터로 강수량 추세를 분석한다", affinity: 4, eco: 8, reply: "오름이: \"숫자는 거짓말 안 하지. 좋은 접근이야.\"" },
        { text: "낯선 식물의 정체부터 알아본다", affinity: 6, eco: 4, reply: "오름이: \"그 풀 나도 본 적 없는 거였어. 같이 살펴보자!\"" },
      ],
    },
    {
      tag: "3장 · 펜션 사장과의 대면",
      backdrop: "pension",
      mood: "angryish",
      lines: [
        "펜션 사장: \"우리가 물을 좀 많이 쓰는 건 맞지만... 손님 받으려면 어쩔 수 없잖아요.\"",
        "오름이: \"(작게) 화내지 말고 차분히 얘기해보자, 알겠지?\""
      ],
      choices: [
        { text: "데이터를 보여주며 차분히 설득한다", affinity: 8, eco: 9, reply: "오름이: \"멋졌어! 화내지 않고 풀어가는 모습, 진짜 어른스럽다.\"" },
        { text: "바로 환경청에 신고한다", affinity: -3, eco: 5, reply: "오름이: \"음... 효과는 있겠지만 사장님이 많이 놀라셨겠다.\"" },
        { text: "사용량을 줄이는 대신 마을 지원금을 연결해주겠다고 제안한다", affinity: 7, eco: 7, reply: "오름이: \"양쪽 다 살리는 방법이네! 너 진짜 영리하다.\"" },
      ],
    },
    {
      tag: "4장 · 복원 활동",
      backdrop: "restore",
      mood: "happy",
      lines: [
        "오름이: \"펜션도 협조하기로 했고, 이제 샘물이 다시 차오르게 도와줘야 해.\"",
        "오름이: \"어떤 방식으로 복원에 참여하고 싶어?\""
      ],
      choices: [
        { text: "주말마다 직접 와서 정화 작업을 돕는다", affinity: 9, eco: 9, reply: "오름이: \"네가 직접 와주는 게 제일 든든해!\"" },
        { text: "친구들을 모아서 캠페인을 연다", affinity: 7, eco: 8, reply: "오름이: \"혼자보다 다 같이! 더 멀리까지 소문이 나겠다.\"" },
        { text: "전문가에게 연락해 장기 모니터링을 제안한다", affinity: 5, eco: 9, reply: "오름이: \"오래 지속되게 만드는 방법, 똑똑한데?\"" },
      ],
    },
    {
      tag: "5장 · 다시 차오른 샘물",
      backdrop: "epilogue",
      mood: "happy",
      lines: [
        "오름이: \"봐봐, 샘물이 다시 차오르고 있어! 동물들도 돌아왔어.\"",
        "오름이: \"이번 사건, 너랑 같이 풀어서 더 기억에 남을 것 같아.\"",
        "오름이: \"우리... 앞으로도 같이 곶자왈을 지켜볼까?\""
      ],
      choices: [
        { text: "당연하지, 또 무슨 일이 생기면 불러줘", affinity: 10, eco: 6, reply: "오름이: \"약속이다! 다음엔 또 어떤 모험이 기다릴까.\"" },
        { text: "이번 일로 환경 동아리를 만들어보고 싶어", affinity: 6, eco: 10, reply: "오름이: \"우와, 그거 정말 멋진 생각이야!\"" },
        { text: "이제 좀 쉬고 싶다, 충분히 한 것 같아", affinity: 2, eco: 3, reply: "오름이: \"그래, 고생했어. 천천히 또 만나자.\"" },
      ],
    },
  ];

  let sceneIdx = 0;
  let affinity = 50, eco = 50;
  let typing = null;
  let lineIdx = 0;

  function clamp(v) { return Math.max(0, Math.min(100, v)); }

  function updateHUD() {
    document.getElementById("vn-affinity").textContent = affinity;
    document.getElementById("vn-eco").textContent = eco;
  }

  function typeLine(text, onDone) {
    const el = document.getElementById("vn-text");
    el.textContent = "";
    let i = 0;
    clearInterval(typing);
    typing = setInterval(function() {
      i++;
      el.textContent = text.slice(0, i);
      if (i >= text.length) {
        clearInterval(typing);
        if (onDone) onDone();
      }
    }, 22);
    el.onclick = function() {
      clearInterval(typing);
      el.textContent = text;
      if (onDone) onDone();
    };
  }

  function showChoices(scene) {
    const wrap = document.getElementById("vn-choices");
    wrap.innerHTML = "";
    scene.choices.forEach(function(choice) {
      const btn = document.createElement("button");
      btn.className = "vn-choice-btn";
      btn.textContent = choice.text;
      btn.onclick = function() {
        affinity = clamp(affinity + choice.affinity);
        eco = clamp(eco + choice.eco);
        updateHUD();
        wrap.innerHTML = "";
        typeLine(choice.reply, function() {
          const nextBtn = document.createElement("button");
          nextBtn.className = "vn-next-btn";
          nextBtn.textContent = (sceneIdx < SCENES.length - 1) ? "다음으로 ▶" : "결말 보기 ▶";
          nextBtn.onclick = function() {
            sceneIdx++;
            if (sceneIdx < SCENES.length) {
              playScene(sceneIdx);
            } else {
              showEnding();
            }
          };
          wrap.appendChild(nextBtn);
        });
      };
      wrap.appendChild(btn);
    });
  }

  function playScene(idx) {
    const scene = SCENES[idx];
    currentBackdrop = scene.backdrop;
    currentMood = scene.mood;
    document.getElementById("vn-chapter-tag").textContent = scene.tag;
    document.getElementById("vn-speaker").textContent = scene.lines[0].split(":")[0];
    document.getElementById("vn-choices").innerHTML = "";
    lineIdx = 0;

    function playNextLine() {
      if (lineIdx >= scene.lines.length) {
        showChoices(scene);
        return;
      }
      const raw = scene.lines[lineIdx];
      const sep = raw.indexOf(":");
      const speaker = sep > -1 ? raw.slice(0, sep) : "";
      const text = sep > -1 ? raw.slice(sep + 1).trim() : raw;
      document.getElementById("vn-speaker").textContent = speaker;
      lineIdx++;
      typeLine(text, function() {
        if (lineIdx < scene.lines.length) {
          const cont = document.createElement("button");
          cont.className = "vn-next-btn";
          cont.textContent = "계속 ▶";
          cont.onclick = function() {
            document.getElementById("vn-choices").innerHTML = "";
            playNextLine();
          };
          document.getElementById("vn-choices").innerHTML = "";
          document.getElementById("vn-choices").appendChild(cont);
        } else {
          document.getElementById("vn-choices").innerHTML = "";
          showChoices(scene);
        }
      });
    }
    playNextLine();
  }

  function ending() {
    if (affinity >= 75 && eco >= 75) {
      return ["💚 곶자왈의 파트너 엔딩", "샘물도 되살리고, 오름이와도 진짜 단짝이 되었습니다. 둘은 앞으로도 곶자왈 구석구석을 함께 지켜나갑니다.", "epilogue", "happy"];
    }
    if (affinity >= 75 && eco < 50) {
      return ["🤝 다정한 탐정 엔딩", "오름이는 너를 정말 좋아하게 됐지만, 환경 실천은 아직 한 걸음 더 필요해 보인다고 살짝 웃으며 말합니다.", "epilogue", "normal"];
    }
    if (eco >= 75 && affinity < 50) {
      return ["🌱 냉철한 조사관 엔딩", "사건은 완벽하게 해결했지만, 오름이는 네가 조금 더 다정했으면 좋았을 거라 생각합니다.", "epilogue", "worried"];
    }
    if (affinity < 35 && eco < 35) {
      return ["🍃 미완의 사건 엔딩", "샘물은 간신히 회복됐지만, 어딘가 아쉬움이 남는 결말. 오름이는 다음 기회를 기다리기로 합니다.", "village", "worried"];
    }
    return ["🌤️ 함께 성장하는 엔딩", "완벽하진 않았지만, 오름이와 너는 이번 사건을 통해 서로 조금씩 더 가까워졌습니다.", "epilogue", "happy"];
  }

  function showEnding() {
    const [title, desc, bg, mood] = ending();
    currentBackdrop = bg;
    currentMood = mood;
    document.getElementById("vn-chapter-tag").textContent = "결말";
    document.getElementById("vn-speaker").textContent = title;
    document.getElementById("vn-choices").innerHTML = "";
    typeLine(desc, function() {
      const wrap = document.getElementById("vn-choices");
      const restartBtn = document.createElement("button");
      restartBtn.className = "vn-next-btn vn-restart-btn";
      restartBtn.textContent = "다시 플레이하기 ↺";
      restartBtn.onclick = function() {
        sceneIdx = 0; affinity = 50; eco = 50;
        updateHUD();
        playScene(0);
      };
      wrap.appendChild(restartBtn);
    });
  }

  updateHUD();
  playScene(0);
})();
</script>
"""

components.html(GAME_HTML, height=720, scrolling=False)

st.caption("💡 텍스트를 클릭하면 타이프라이터 효과를 건너뛰고 바로 전체 대사를 볼 수 있어요.")
