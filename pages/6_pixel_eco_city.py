import streamlit as st
import streamlit.components.v1 as components
from shared import apply_css, lesson_flow

apply_css()

st.markdown("## 🏙️ 픽셀 에코시티")

lesson_flow(
    "pixel_city",
    concept=[
        {"title": "📘 Chapter 1 · 시스템 사고란?", "body": """
<p style='line-height:1.8'>
<b>시스템 사고(Systems Thinking)</b>는 어떤 것을 <b>따로 노는 부품이 아니라, 서로 연결된
하나의 전체</b>로 보는 관점입니다.<br><br>
도시가 대표적인 시스템이에요. 공장 하나를 지으면 → <b>일자리·수입</b>이 늘지만 → <b>대기오염</b>이
심해지고 → <b>주민 건강·만족도</b>가 떨어지고 → 다시 도시 매력이 줄어듭니다. 이렇게
<b>한 곳을 건드리면 다른 곳이 연쇄적으로 움직이는</b> 것이 시스템의 핵심 특징입니다.
</p>
<p style='color:var(--text-caption); font-size:.85rem'>💡 그래서 "좋아 보이는 선택"도 다른 곳에 부작용을 남길 수 있어요.</p>
"""},
        {"title": "📗 Chapter 2 · 도시의 환경 요소들", "body": """
<p style='line-height:1.8'>
이 게임의 도시는 세 가지 지표로 움직여요. 각 건물이 이 지표들을 서로 다르게 바꿉니다.
</p>
<ul style='line-height:1.9; color:var(--text-muted)'>
<li><b>🌫️ 오염도:</b> 공장이 늘리고, 태양광·공원·재활용센터가 낮춥니다.</li>
<li><b>😊 주민만족도:</b> 공원·재활용·편의시설이 올리고, 오염이 낮춥니다.</li>
<li><b>☀️ 에너지자립:</b> 태양광이 올리고, 공장이 전력을 소모합니다.</li>
</ul>
<p style='line-height:1.8'>
친환경 인프라(태양광·공원·재활용)는 도시를 맑게 하지만 <b>돈(예산)</b>이 듭니다.
공장은 <b>수입</b>을 주지만 오염을 남기죠.
</p>
"""},
        {"title": "📙 Chapter 3 · 친환경 전환의 비용과 편익", "body": """
<p style='line-height:1.8'>
환경을 지키는 데는 <b>비용</b>이 들지만, 그 <b>편익</b>은 시간이 지나며 돌아옵니다.
깨끗한 도시는 주민을 모으고, 관광·투자를 부르며, 장기적으로 더 튼튼해져요.<br><br>
문제는 <b>예산이 한정</b>되어 있다는 것. 그래서 "지금 무엇을 먼저 지을지" 순서와 우선순위를
정하는 <b>전략적 판단</b>이 필요합니다. 오염을 한 번에 없애려다 예산이 바닥나면 도시가 멈추니까요.
</p>
<p style='color:var(--text-caption); font-size:.85rem'>🎯 문제: 예산 안에서 어떤 건물을 배치해 오염을 줄이고 만족도를 지킬 것인가?</p>
"""},
    ],
    discuss=[
        "오염도를 낮추면서 주민만족도를 유지하려면 어떤 순서로 지어야 할까요?",
        "공장을 완전히 없애는 게 최선일까요? 무엇을 잃게 되나요?",
        "'한 곳을 건드리면 다른 곳이 움직인다'를 게임에서 느낀 순간은?",
        "우리 실제 도시(제주)에 적용한다면 가장 먼저 바꿀 한 가지는?",
    ],
    present="""
<div class='eco-card'>
<b style='color:var(--accent-primary)'>🎤 발표: 우리 도시 설계안</b>
<ul style='color:var(--text-muted); line-height:1.8'>
<li>최종 도시의 <b>오염·만족·에너지</b> 수치와 스크린샷</li>
<li>핵심 <b>설계 전략</b> (무엇을 우선했나)</li>
<li>더 발전시킨다면 추가할 정책</li>
</ul>
</div>
""",
)

st.markdown("오염된 마을을 직접 도시 계획해서 살려보세요. 친환경 건물을 지을수록 도시의 색과 분위기가 실시간으로 바뀝니다.")

st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🧱 도시를 디자인하세요</div>
  <div class='hero-sub'>
  아래 도구 중 하나를 고르고 타일을 클릭해서 건물을 짓거나 철거하세요.<br>
  공장이 많으면 스모그가 짙어지고, 태양광·공원·자전거도로·재활용센터가 많으면 도시가 맑고 푸르게 바뀝니다.
  </div>
</div>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<div id="eco-city-root" style="font-family:'Noto Sans KR',sans-serif; max-width:760px; margin:0 auto;">
  <style>
    #eco-city-root * { box-sizing: border-box; }
    .ec-hud {
      display:flex; gap:10px; flex-wrap:wrap; margin-bottom:10px;
    }
    .ec-chip {
      background:#1A1A1A; color:#F0F0F0; border-radius:50px; padding:6px 14px;
      font-size:13px; display:flex; align-items:center; gap:6px;
    }
    .ec-chip b { color:#FF5C8A; font-size:14px; }
    .ec-canvas-wrap {
      border-radius:14px; overflow:hidden; border:3px solid #1A1A1A;
      box-shadow:0 6px 18px rgba(0,0,0,0.25);
    }
    canvas#ecoCanvas { display:block; width:100%; image-rendering: pixelated; background:#222; cursor:pointer; }
    .ec-toolbar {
      display:flex; gap:8px; margin-top:12px; flex-wrap:wrap;
    }
    .ec-tool {
      flex:1; min-width:96px; border:2px solid #ddd; border-radius:10px; padding:8px 6px;
      text-align:center; cursor:pointer; background:#fff; font-size:12px; user-select:none;
      transition: all .15s;
    }
    .ec-tool .ec-icon { font-size:20px; display:block; margin-bottom:2px; }
    .ec-tool .ec-cost { color:#888; font-size:11px; }
    .ec-tool.selected { border-color:#FF2D6B; background:#FFE4EE; box-shadow:0 2px 8px rgba(255,45,107,0.25); }
    .ec-msg {
      margin-top:10px; padding:8px 14px; border-radius:10px; font-size:14px; font-weight:700;
      text-align:center; transition: all .3s;
    }
  </style>

  <div class="ec-hud">
    <div class="ec-chip">💰 자금 <b id="ec-coins">300</b></div>
    <div class="ec-chip">🌫️ 오염도 <b id="ec-pollution">70</b></div>
    <div class="ec-chip">😊 만족도 <b id="ec-happiness">40</b></div>
    <div class="ec-chip">☀️ 에너지자립 <b id="ec-energy">5</b></div>
  </div>

  <div class="ec-canvas-wrap">
    <canvas id="ecoCanvas" width="480" height="320"></canvas>
  </div>

  <div class="ec-toolbar" id="ec-toolbar"></div>
  <div class="ec-msg" id="ec-msg" style="background:#eee; color:#444;">도구를 선택하고 타일을 클릭해 도시를 설계해보세요.</div>
</div>

<script>
(function() {
  const GRID_W = 12, GRID_H = 8, TILE = 40;
  const canvas = document.getElementById("ecoCanvas");
  const ctx = canvas.getContext("2d");

  const TOOLS = [
    { id: "bulldoze", name: "철거", icon: "🪓", cost: 0 },
    { id: "factory",  name: "공장", icon: "🏭", cost: 40 },
    { id: "solar",    name: "태양광", icon: "🔆", cost: 60 },
    { id: "park",     name: "공원", icon: "🌳", cost: 30 },
    { id: "bike",     name: "자전거도로", icon: "🚲", cost: 20 },
    { id: "recycle",  name: "재활용센터", icon: "♻️", cost: 50 },
  ];

  const COLORS = {
    empty:   { base: "#8fd17a", detail: "#6ab85a" },
    factory: { base: "#5a5a5a", detail: "#333333", glass: "#f4c542" },
    solar:   { base: "#22325c", detail: "#4fc3f7" },
    park:    { base: "#3f7d3f", trunk: "#7b4a26", leaf: "#5fae5f" },
    bike:    { base: "#777777", stripe: "#ffffff" },
    recycle: { base: "#2e8b57", arrow: "#ffffff" },
  };

  let grid = [];
  for (let y = 0; y < GRID_H; y++) {
    let row = [];
    for (let x = 0; x < GRID_W; x++) {
      row.push((x + y) % 5 === 0 ? "factory" : "empty");
    }
    grid.push(row);
  }

  let coins = 300;
  let selectedTool = "factory";
  let particles = [];
  let frame = 0;
  let stats = { pollution: 70, happiness: 40, energy: 5 };

  const toolbar = document.getElementById("ec-toolbar");
  TOOLS.forEach(t => {
    const div = document.createElement("div");
    div.className = "ec-tool" + (t.id === selectedTool ? " selected" : "");
    div.id = "tool-" + t.id;
    div.innerHTML = "<span class='ec-icon'>" + t.icon + "</span>" + t.name +
      "<div class='ec-cost'>" + (t.cost > 0 ? (t.cost + "코인") : "무료") + "</div>";
    div.onclick = function() {
      selectedTool = t.id;
      document.querySelectorAll(".ec-tool").forEach(el => el.classList.remove("selected"));
      div.classList.add("selected");
    };
    toolbar.appendChild(div);
  });

  function toolCost(id) {
    const t = TOOLS.find(t => t.id === id);
    return t ? t.cost : 0;
  }

  function computeStats() {
    let counts = { factory: 0, solar: 0, park: 0, bike: 0, recycle: 0, empty: 0 };
    for (let y = 0; y < GRID_H; y++) {
      for (let x = 0; x < GRID_W; x++) {
        counts[grid[y][x]]++;
      }
    }
    let pollution = 20 + counts.factory * 9 - counts.solar * 5 - counts.park * 4 - counts.bike * 2 - counts.recycle * 4;
    let happiness = 50 + counts.park * 4 + counts.recycle * 3 + counts.bike * 2 - counts.factory * 5;
    let energy = counts.solar * 9 - counts.factory * 2;
    pollution = Math.max(0, Math.min(100, pollution));
    happiness = Math.max(0, Math.min(100, happiness));
    energy = Math.max(0, Math.min(100, energy));
    stats = { pollution, happiness, energy, counts };
    document.getElementById("ec-pollution").textContent = pollution;
    document.getElementById("ec-happiness").textContent = happiness;
    document.getElementById("ec-energy").textContent = energy;

    const msg = document.getElementById("ec-msg");
    if (pollution <= 15 && happiness >= 70) {
      msg.textContent = "🌿 탄소중립 에코시티 달성! 주민들이 행복해합니다.";
      msg.style.background = "#E3FCEF"; msg.style.color = "#1B7A43";
    } else if (pollution >= 80) {
      msg.textContent = "🌫️ 스모그가 도시를 뒤덮고 있어요. 친환경 건물이 필요합니다.";
      msg.style.background = "#FFE4E4"; msg.style.color = "#B3261E";
    } else if (happiness <= 25) {
      msg.textContent = "😢 주민 만족도가 너무 낮아요. 공원이나 재활용센터를 늘려보세요.";
      msg.style.background = "#FFF2CC"; msg.style.color = "#8A6D00";
    } else {
      msg.textContent = "🏗️ 도시가 변화하고 있습니다. 계속 균형을 잡아보세요.";
      msg.style.background = "#EEE"; msg.style.color = "#444";
    }
  }

  function placeAt(gx, gy) {
    const current = grid[gy][gx];
    const newType = selectedTool === "bulldoze" ? "empty" : selectedTool;
    if (current === newType) return;
    const cost = toolCost(selectedTool);
    if (coins < cost) {
      flashInsufficient();
      return;
    }
    coins -= cost;
    grid[gy][gx] = newType;
    document.getElementById("ec-coins").textContent = coins;
    computeStats();
  }

  function flashInsufficient() {
    const msg = document.getElementById("ec-msg");
    const prevBg = msg.style.background, prevColor = msg.style.color, prevText = msg.textContent;
    msg.textContent = "💸 자금이 부족합니다!";
    msg.style.background = "#FFE4E4"; msg.style.color = "#B3261E";
    setTimeout(() => { msg.textContent = prevText; msg.style.background = prevBg; msg.style.color = prevColor; }, 900);
  }

  canvas.addEventListener("click", function(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;
    const gx = Math.floor(x / TILE), gy = Math.floor(y / TILE);
    if (gx >= 0 && gx < GRID_W && gy >= 0 && gy < GRID_H) placeAt(gx, gy);
  });

  function drawTile(x, y, type) {
    const px = x * TILE, py = y * TILE;
    const c = COLORS[type];
    ctx.fillStyle = c.base;
    ctx.fillRect(px, py, TILE, TILE);

    if (type === "empty") {
      ctx.fillStyle = c.detail;
      for (let i = 0; i < 4; i++) {
        const dx = px + 6 + (i % 2) * 18;
        const dy = py + 8 + Math.floor(i / 2) * 18;
        ctx.fillRect(dx, dy, 4, 4);
      }
    } else if (type === "factory") {
      ctx.fillStyle = c.detail;
      ctx.fillRect(px + 6, py + 4, 8, 10);
      ctx.fillRect(px + 4, py + 12, TILE - 8, TILE - 16);
      ctx.fillStyle = c.glass;
      ctx.fillRect(px + 10, py + 18, 6, 6);
      ctx.fillRect(px + 22, py + 18, 6, 6);
      if (frame % 30 < 15) {
        particles.push({ x: px + 10, y: py + 4, vy: -0.4, vx: (Math.random() - 0.5) * 0.3, life: 60, type: "smoke" });
      }
    } else if (type === "solar") {
      ctx.fillStyle = c.detail;
      for (let r = 0; r < 3; r++) {
        for (let col = 0; col < 3; col++) {
          ctx.fillRect(px + 5 + col * 11, py + 6 + r * 10, 9, 8);
        }
      }
      if (frame % 40 < 4 && Math.random() < 0.5) {
        particles.push({ x: px + 5 + Math.random() * 30, y: py + 6 + Math.random() * 24, vy: -0.1, vx: 0, life: 20, type: "sparkle" });
      }
    } else if (type === "park") {
      ctx.fillStyle = c.trunk;
      ctx.fillRect(px + TILE / 2 - 2, py + 22, 4, 12);
      ctx.fillStyle = c.leaf;
      ctx.beginPath();
      ctx.arc(px + TILE / 2, py + 16, 12, 0, Math.PI * 2);
      ctx.fill();
      if (frame % 50 < 2) {
        particles.push({ x: px + TILE / 2, y: py + 16, vy: 0.3, vx: (Math.random() - 0.5) * 0.4, life: 50, type: "leaf" });
      }
    } else if (type === "bike") {
      ctx.fillStyle = c.stripe;
      for (let i = 0; i < 4; i++) {
        ctx.fillRect(px + 4 + i * 9, py + TILE / 2 - 2, 5, 4);
      }
    } else if (type === "recycle") {
      ctx.strokeStyle = c.arrow;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(px + TILE / 2, py + TILE / 2, 11, (frame / 20) % (Math.PI * 2), (frame / 20) % (Math.PI * 2) + Math.PI * 1.5);
      ctx.stroke();
    }
  }

  function drawSky() {
    const p = stats.pollution / 100;
    const top = lerpColor([135, 206, 250], [120, 110, 100], p);
    const bottom = lerpColor([255, 255, 255], [160, 150, 140], p);
    const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    grad.addColorStop(0, rgb(top));
    grad.addColorStop(1, rgb(bottom));
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  function lerpColor(a, b, t) {
    return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
  }
  function rgb(c) { return "rgb(" + c.map(v => Math.round(v)).join(",") + ")"; }

  function drawParticles() {
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy; p.life -= 1;
      const alpha = Math.max(0, p.life / 60);
      if (p.type === "smoke") {
        ctx.fillStyle = "rgba(180,180,180," + alpha * 0.6 + ")";
        ctx.fillRect(p.x, p.y, 4, 4);
      } else if (p.type === "sparkle") {
        ctx.fillStyle = "rgba(255,255,180," + alpha + ")";
        ctx.fillRect(p.x, p.y, 2, 2);
      } else if (p.type === "leaf") {
        ctx.fillStyle = "rgba(95,174,95," + alpha + ")";
        ctx.fillRect(p.x, p.y, 3, 3);
      }
    });
    particles = particles.filter(p => p.life > 0);
  }

  function drawSmog() {
    const p = stats.pollution / 100;
    if (p > 0.15) {
      ctx.fillStyle = "rgba(120,120,110," + (p * 0.35) + ")";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
  }

  function loop() {
    frame++;
    drawSky();
    for (let y = 0; y < GRID_H; y++) {
      for (let x = 0; x < GRID_W; x++) {
        drawTile(x, y, grid[y][x]);
      }
    }
    ctx.strokeStyle = "rgba(0,0,0,0.08)";
    for (let x = 0; x <= GRID_W; x++) {
      ctx.beginPath(); ctx.moveTo(x * TILE, 0); ctx.lineTo(x * TILE, canvas.height); ctx.stroke();
    }
    for (let y = 0; y <= GRID_H; y++) {
      ctx.beginPath(); ctx.moveTo(0, y * TILE); ctx.lineTo(canvas.width, y * TILE); ctx.stroke();
    }
    drawParticles();
    drawSmog();
    requestAnimationFrame(loop);
  }

  setInterval(function() {
    const income = stats.counts ? stats.counts.factory * 3 + 4 : 4;
    const cleanBonus = stats.pollution < 30 ? 8 : 0;
    coins += income + cleanBonus;
    document.getElementById("ec-coins").textContent = coins;
  }, 2000);

  computeStats();
  loop();
})();
</script>
"""

components.html(GAME_HTML, height=660, scrolling=False)

st.caption("💡 진행 팁: 처음엔 공장이 섞여 있어 오염도가 높습니다. 태양광·공원·재활용센터로 점차 교체하면서 만족도와 자금 균형을 맞춰보세요.")
