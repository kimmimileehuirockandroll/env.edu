import os
import random
import streamlit as st
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.image import imread
from shared import apply_css, _korean_font, get_chart_colors
apply_css()

# ─────────────────────────────────────────────
#  GAME 1 전용 데이터 (이 게임만 사용)
# ─────────────────────────────────────────────
NODES = {
    "제주공항":       {"en": "Jeju Airport",     "lat": 33.511, "lng": 126.493, "icon": "✈️"},
    "협재해변":       {"en": "Hyeopjae Beach",   "lat": 33.394, "lng": 126.240, "icon": "🏖️"},
    "대정중학교":     {"en": "Daejeong Middle",  "lat": 33.218, "lng": 126.250, "icon": "🏫"},
    "서귀포치유의숲": {"en": "Seogwipo Forest",  "lat": 33.252, "lng": 126.498, "icon": "🌲"},
    "성산일출봉":     {"en": "Seongsan Sunrise", "lat": 33.459, "lng": 126.942, "icon": "🏔️"},
    "함덕해변":       {"en": "Hamdeok Beach",    "lat": 33.543, "lng": 126.669, "icon": "🌊"},
}

# 거점 간 실제 도로 거리(km)
# 버스: 27g/km, 기본1200원+100원/km, 3분/km + 10분 + 평균 대기(랜덤)
# 전기차: 79g/km, 200원/km, 1분/km
ROAD_KM = {
    ("제주공항",       "협재해변"):         34.9,
    ("제주공항",       "함덕해변"):         21.8,
    ("제주공항",       "성산일출봉"):       54.8,
    ("협재해변",       "대정중학교"):       25.5,
    ("협재해변",       "서귀포치유의숲"):   32.9,
    ("대정중학교",     "서귀포치유의숲"):   37.4,
    ("서귀포치유의숲", "성산일출봉"):       54.3,
    ("성산일출봉",     "함덕해변"):         35.1,
    ("함덕해변",       "협재해변"):         56.1,
    ("대정중학교",     "성산일출봉"):       90.6,
    ("서귀포치유의숲", "함덕해변"):         32.8,
}

def _make_edge(km):
    return {
        "bus": (round(km * 3) + 10, round(km * 27), 1200 + round(km * 100)),
        "ev":  (round(km * 1),      round(km * 79), round(km * 200)),
    }

EDGES = {k: _make_edge(v) for k, v in ROAD_KM.items()}


def get_edge(a, b):
    if (a, b) in EDGES: return EDGES[(a, b)]
    if (b, a) in EDGES: return EDGES[(b, a)]
    return None


def get_neighbors(node):
    neighbors = []
    for (a, b) in EDGES:
        if a == node and b not in st.session_state.visited:
            neighbors.append(b)
        elif b == node and a not in st.session_state.visited:
            neighbors.append(a)
    return neighbors


# ─────────────────────────────────────────────
#  GRAPH DRAWING — 제주 지도 이미지 배경 오버레이
# ─────────────────────────────────────────────

# 이미지 내 노드 픽셀 위치 → matplotlib 정규화 좌표 (y 반전)
# 원본 이미지 해상도: 2816 x 1536
NODE_POS = {
    "제주공항":       (0.476, 0.720),  # 핀 위쪽 (하늘)
    "협재해변":       (0.194, 0.490),  # 핀 왼쪽 (바다)
    "대정중학교":     (0.297, 0.317),
    "서귀포치유의숲": (0.562, 0.294),
    "성산일출봉":     (0.837, 0.628),
    "함덕해변":       (0.758, 0.830),  # 핀 위쪽 (바다)
}

# 배경 이미지 경로 (소스코드와 같은 폴더에 jeju_map.png 있어야 함)
MAP_IMG_PATHS = [
    "jeju_map.png",
    os.path.join(os.path.dirname(__file__) if "__file__" in dir() else ".", "jeju_map.png"),
]

def load_map_img():
    for p in MAP_IMG_PATHS:
        if os.path.exists(p):
            return imread(p)
    return None


def draw_game_graph():
    G = nx.Graph()
    for node in NODES:
        G.add_node(node)
    for (a, b) in EDGES:
        G.add_edge(a, b)

    # 이미지 비율에 맞춰 figsize 설정 (2816:1536 ≈ 11:6)
    fig, ax = plt.subplots(figsize=(11, 6))
    ch = get_chart_colors()
    fig.patch.set_facecolor(ch["bg"])
    ax.set_facecolor(ch["bg"])
    ax.axis("off")

    pos = NODE_POS

    # ── 배경 이미지 렌더링 ──
    map_img = load_map_img()
    if map_img is not None:
        ax.imshow(map_img, extent=[0, 1, 0, 1], aspect="auto",
                  zorder=0, alpha=0.92)
    else:
        # 이미지 없을 때 기존 섬 모양 폴백
        ellipse = mpatches.Ellipse((0.4, 0.58), 0.75, 0.60,
                                    angle=8, linewidth=0,
                                    facecolor=ch["card"], alpha=0.6)
        ax.add_patch(ellipse)

    # ── 전체 엣지 (반투명 흰 점선) ──
    for (a, b) in EDGES:
        x = [pos[a][0], pos[b][0]]
        y = [pos[a][1], pos[b][1]]
        ax.plot(x, y, color="white", linewidth=1.5, zorder=2,
                alpha=0.35, linestyle="--")

    # ── 이동한 엣지 (밝은 민트/블루 실선 + 화살표) ──
    for (frm, to, transport) in st.session_state.path_edges:
        x = [pos[frm][0], pos[to][0]]
        y = [pos[frm][1], pos[to][1]]
        color = "#69f0ae" if transport == "bus" else "#40c4ff"
        # 굵은 발광 효과 (shadow)
        ax.plot(x, y, color=color, linewidth=7, zorder=3, alpha=0.3)
        ax.plot(x, y, color=color, linewidth=3, zorder=4, alpha=1.0)
        # 화살표
        mx, my = (x[0]+x[1])/2, (y[0]+y[1])/2
        ax.annotate("", xy=(x[1], y[1]), xytext=(mx, my),
                    arrowprops=dict(arrowstyle="-|>", color=color,
                                   lw=2, mutation_scale=14),
                    zorder=5)

    # ── 노드 마커 + 라벨 ──
    for node, (nx_, ny_) in pos.items():
        visited = node in st.session_state.visited
        current = node == st.session_state.current_node

        # 마커 색상 결정
        if current:
            ring_color  = "#FFD740"
            dot_color   = "#FF6F00"
            ring_size   = 460
            dot_size    = 190
        elif visited:
            ring_color  = "#69f0ae"
            dot_color   = "#00695c"
            ring_size   = 300
            dot_size    = 120
        else:
            ring_color  = "white"
            dot_color   = "#cccccc"
            ring_size   = 240
            dot_size    = 80

        # 외곽 링 (glow 효과)
        ax.scatter(nx_, ny_, s=ring_size * 1.5, color=ring_color,
                   zorder=6, alpha=0.25, linewidths=0)
        # 메인 링
        ax.scatter(nx_, ny_, s=ring_size, color=ring_color,
                   zorder=7, edgecolors="white", linewidths=2.2, alpha=0.95)
        # 내부 점
        ax.scatter(nx_, ny_, s=dot_size, color=dot_color, zorder=8)

        # ── 이름 라벨: 흰색 반투명 라운드 박스 ──
        yoff = -0.08 if ny_ > 0.60 else 0.08
        border_color = "#FFD740" if current else ("#4caf50" if visited else "#cccccc")
        txt_kwargs = dict(
            ha="center", va="center",
            color="#1a1a1a",
            bbox=dict(
                boxstyle="round,pad=0.4",
                facecolor="white",
                edgecolor=border_color,
                linewidth=2.0,
                alpha=0.85,
            ),
            zorder=9,
        )
        if _korean_font:
            ax.text(nx_, ny_ + yoff, node,
                    fontproperties=_korean_font, **txt_kwargs)
        else:
            # 폰트 없을 때: 영문 이름으로 fallback
            fallback = NODES[node]["en"]
            ax.text(nx_, ny_ + yoff, fallback,
                    fontsize=7.5, fontweight="bold", **txt_kwargs)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout(pad=0.2)
    fig.patch.set_alpha(0.0)
    return fig


def init_state():
    """게임 진행에 필요한 session_state 기본값을 설정 (이미 있으면 건너뜀)."""
    defaults = {
        "game_started": False,
        "current_node": "대정중학교",
        "visited":      ["대정중학교"],
        "path_edges":   [],
        "time_left":    480,
        "carbon_left":  10000,
        "budget_left":  60000,
        "game_log":     [],
        "game_over":    False,
        "game_won":     False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# ─────────────────────────────────────────────
#  화면 구성
# ─────────────────────────────────────────────
st.markdown("## 🎮 삼다수 에코 레이스")
st.markdown("제주도 랜드마크를 최적의 경로로 탐험하세요. 탄소를 아끼고 시간과 비용도 관리해야 합니다!")

# ── Resource display ──
time_pct   = st.session_state.time_left   / 480   * 100
carbon_pct = st.session_state.carbon_left / 10000 * 100
budget_pct = st.session_state.budget_left / 60000 * 100

col_t, col_c, col_b, col_v = st.columns(4)
col_t.metric("⏱️ 남은 시간", f"{st.session_state.time_left}분",
             delta=f"총 480분 중" if not st.session_state.game_started else None)
col_c.metric("🌿 탄소 예산", f"{st.session_state.carbon_left:,}g",
             delta="10,000g 시작" if not st.session_state.game_started else None)
col_b.metric("💰 잔여 비용", f"₩{st.session_state.budget_left:,}",
             delta="₩60,000 시작" if not st.session_state.game_started else None)
col_v.metric("📍 방문 거점", f"{len(st.session_state.visited)}개 / 6개")

# Progress bars
st.markdown("**자원 현황**")
bar_col1, bar_col2, bar_col3 = st.columns(3)

def progress_bar(label, pct):
    pct = max(0, min(100, pct))
    color = "#6B6B6B" if pct > 30 else "#FF8C00"  # 30% 이하면 주황 경고
    return f"""
<div style="margin-bottom:0.5rem;">
  <div style="font-size:0.8rem; color:var(--text-caption); margin-bottom:4px;">{label}</div>
  <div style="background:#E8E8E8; border-radius:99px; height:8px; overflow:hidden;">
    <div style="width:{pct}%; background:{color}; height:8px; border-radius:99px;
                transition:width 0.4s ease;"></div>
  </div>
</div>
"""

with bar_col1:
    st.markdown(progress_bar("⏱️ 시간", time_pct), unsafe_allow_html=True)
with bar_col2:
    st.markdown(progress_bar("🌿 탄소", carbon_pct), unsafe_allow_html=True)
with bar_col3:
    st.markdown(progress_bar("💰 비용", budget_pct), unsafe_allow_html=True)

st.markdown("---")

# ── Map ──
map_col, ctrl_col = st.columns([3, 2])

with map_col:
    st.markdown("### 🗺️ 네트워크 지도")
    fig = draw_game_graph()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Visited nodes badges
    visited_html = ""
    for node in NODES:
        if node in st.session_state.visited:
            style = "background:#FFF0F5; border:1.5px solid var(--accent-primary); color:var(--accent-primary);"
        else:
            style = "background:#FFFFFF; border:1.5px solid #E0E0E0; color:var(--text-muted);"
        icon = NODES[node]["icon"]
        visited_html += f'<span style="display:inline-block; {style} border-radius:8px; padding:3px 10px; font-size:.82rem; margin:2px;">{icon} {node}</span>'
    st.markdown(f"<div style='margin-top:.5rem;'>{visited_html}</div>", unsafe_allow_html=True)

with ctrl_col:
    st.markdown("### 🧭 이동 제어판")

    if st.session_state.game_over:
        if st.session_state.game_won:
            st.success("🎉 모든 랜드마크를 방문했습니다! 에코 챔피언!")
        else:
            # 어떤 자원이 초과됐는지 표시
            reasons = []
            if st.session_state.time_left   < 0: reasons.append(f"시간 초과 ({abs(st.session_state.time_left)}분 오버)")
            if st.session_state.carbon_left < 0: reasons.append(f"탄소 초과 ({abs(st.session_state.carbon_left):,}g 오버)")
            if st.session_state.budget_left < 0: reasons.append(f"예산 초과 (₩{abs(st.session_state.budget_left):,} 오버)")
            reason_str = " / ".join(reasons) if reasons else "자원 소진"
            st.error(f"❌ 실패! {reason_str}")
        st.markdown(f"**최종 방문:** {len(st.session_state.visited)}개 생태 거점")
        st.markdown(f"**남은 탄소:** {st.session_state.carbon_left:,}g")
        if st.button("🔄 다시 시작"):
            for k in ["game_started","current_node","visited","path_edges",
                      "time_left","carbon_left","budget_left","game_log",
                      "game_over","game_won"]:
                del st.session_state[k]
            init_state()
            st.rerun()
    else:
        st.markdown(f"**현재 위치:** {NODES[st.session_state.current_node]['icon']} **{st.session_state.current_node}**")
        neighbors = get_neighbors(st.session_state.current_node)

        if not neighbors:
            st.info("더 이상 방문할 수 있는 미방문 거점이 없습니다.")
            st.markdown(f"**총 {len(st.session_state.visited)}개** 랜드마크를 방문했습니다! 🎉")
            if len(st.session_state.visited) == len(NODES):
                st.session_state.game_won = True
            st.session_state.game_over = True
            st.rerun()
        else:
            dest = st.selectbox(
                "🏁 다음 목적지",
                neighbors,
                format_func=lambda x: f"{NODES[x]['icon']} {x} ({NODES[x]['en']})"
            )
            transport = st.radio(
                "🚌 이동 수단",
                ["🚌 대중교통 (버스)", "⚡ 전기 렌터카"],
                key="transport_choice"
            )

            # Preview costs
            edge = get_edge(st.session_state.current_node, dest)
            if edge:
                t_key = "bus" if "대중교통" in transport else "ev"
                base_time, base_carbon, base_cost = edge[t_key]

                # Bus random time penalty (dice)
                if t_key == "bus":
                    dice_bonus = random.randint(0, 30)
                    preview_time = base_time + dice_bonus
                    dice_note = f"🎲 대기 패널티 +{dice_bonus}분 (랜덤)"
                else:
                    preview_time = base_time
                    dice_note = "✅ 정확한 시간 (패널티 없음)"

                st.markdown(f"""
<div class='eco-card' style='margin-top:.8rem;'>
  <b style='color:var(--text-base);'>예상 소모 자원 미리보기</b>
  <div style='margin-top:.5rem; font-size:.9rem;'>
⏱️ 시간: <span style='color:var(--accent-primary);'><b>{preview_time}분</b></span>
🌿 탄소: <span style='color:var(--accent-primary);'><b>{base_carbon:,}g</b></span><br>
💰 비용: <span style='color:var(--accent-primary);'><b>₩{base_cost:,}</b></span><br>
<span style='color:var(--text-caption); font-size:.83rem;'>{dice_note}</span>
  </div>
</div>
""", unsafe_allow_html=True)

                if st.button(f"🚀 {dest}(으)로 이동하기!"):

                    moving_box = st.empty()
                
                    if t_key == "bus":
                        moving_messages = [
                            "🚌 버스 정류장으로 이동 중...",
                            "🎫 교통카드 태그!",
                            "🚏 버스 대기 시간 반영 중...",
                            "🌿 탄소 절감 효과 계산 중...",
                            f"📍 {dest} 도착!",
                        ]
                    else:
                        moving_messages = [
                            "⚡ 전기차 시동 ON!",
                            "🔋 배터리 상태 확인 중...",
                            "🛣️ 최적 경로 탐색 중...",
                            "🌿 탄소 배출량 계산 중...",
                            f"📍 {dest} 도착!",
                        ]
                
                    for msg in moving_messages:
                        moving_box.markdown(f"""
                <div style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: rgba(10, 15, 13, 0.94);
                    border: 2px solid #69f0ae;
                    border-radius: 24px;
                    padding: 2rem 3rem;
                    z-index: 999999;
                    box-shadow: 0 0 40px rgba(105, 240, 174, 0.35);
                    text-align: center;
                    min-width: 360px;
                ">
                    <div style="font-size: 3rem; margin-bottom: .8rem;">🚀</div>
                    <div style="
                        color: #69f0ae;
                        font-size: 1.5rem;
                        font-weight: 800;
                        margin-bottom: .5rem;
                    ">
                        열심히 이동 중!
                    </div>
                    <div style="
                        color:var(--text-base);
                        font-size: 1rem;
                        line-height: 1.6;
                    ">
                        {msg}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                        time.sleep(0.55)
                
                    moving_box.empty()
                
                                    
                    # Apply costs
                    st.session_state.time_left -= preview_time
                    st.session_state.carbon_left -= base_carbon
                    st.session_state.budget_left -= base_cost
    
                    # Apply costs
                    st.session_state.time_left   -= preview_time
                    st.session_state.carbon_left -= base_carbon
                    st.session_state.budget_left -= base_cost

                    # Log
                    log_entry = (
                        f"{'🚌' if t_key=='bus' else '⚡'} "
                        f"{st.session_state.current_node} → {dest} | "
                        f"⏱️{preview_time}분 🌿{base_carbon}g 💰₩{base_cost:,}"
                    )
                    st.session_state.game_log.append(log_entry)
                    st.session_state.path_edges.append(
                        (st.session_state.current_node, dest, t_key))
                    st.session_state.visited.append(dest)
                    st.session_state.current_node = dest
                    st.session_state.game_started = True

                    # 자원 초과 먼저 체크 (탄소/시간/예산 마이너스면 무조건 실패)
                    resource_fail = (
                        st.session_state.time_left   < 0 or
                        st.session_state.carbon_left < 0 or
                        st.session_state.budget_left < 0
                    )
                    if resource_fail:
                        st.session_state.game_over = True
                        st.session_state.game_won  = False
                    elif len(st.session_state.visited) == len(NODES):
                        # 자원 여유 있고 전체 방문 완료 → 진짜 승리
                        st.session_state.game_won  = True
                        st.session_state.game_over = True
                    st.rerun()

    # ── Travel log ──
    if st.session_state.game_log:
        st.markdown("---")
        st.markdown("### 📋 이동 기록")
        for entry in reversed(st.session_state.game_log[-6:]):
            st.markdown(f"<div style='font-size:.82rem; color:var(--text-muted); padding:3px 0;'>{entry}</div>",
                        unsafe_allow_html=True)

# ── Game rules ──
with st.expander("📖 게임 규칙 & 힌트 보기"):
    st.markdown("""
**🎯 목표**: 대정중학교에서 출발해 480분, 탄소 10,000g, 예산 ₩60,000 안에 최대한 많은 랜드마크를 방문하세요.

**🚌 대중교통 (버스)**
- 탄소 배출: **27g/km** (친환경 ✅)
- 비용: **기본 1,200원 + 100원/km**
- 시간: **3분/km + 10분 + 평균 대기** 🎲

**⚡ 전기 렌터카**
- 탄소 배출: **79g/km** (버스의 약 3배 ⚠️)
- 비용: **200원/km**
- 시간: **1분/km** (빠르고 정확)

**💡 전략 팁**
- 전기차만 타면 탄소 10,000g을 금방 초과해요!
- 탄소가 0 아래로 떨어지는 순간 즉시 실패
- 버스와 전기차를 잘 섞어야 전체 거점 방문이 가능해요
""")
