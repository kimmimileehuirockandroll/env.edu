import streamlit as st
import networkx as nx
import matplotlib
import matplotlib.font_manager as fm
# Mac
plt.rcParams['font.family'] = 'AppleGothic'
# Windows
# plt.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import math
import json
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="제주 에코 네트워크",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  (dark + green/mint theme)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

/* ── reset & base ── */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', 'Space Grotesk', sans-serif;
}
.stApp {
    background: #0a0f0d;
    color: #e8f5e9;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1a14 !important;
    border-right: 1px solid #1e3a2a;
}
[data-testid="stSidebar"] * { color: #b2dfdb !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 1rem; }

/* ── headings ── */
h1 { color: #69f0ae !important; letter-spacing: -1px; }
h2 { color: #40c4aa !important; }
h3 { color: #80cbc4 !important; }

/* ── metric cards ── */
[data-testid="stMetric"] {
    background: #0d2418;
    border: 1px solid #1b5e3b;
    border-radius: 12px;
    padding: 12px 18px;
}
[data-testid="stMetricValue"] { color: #69f0ae !important; font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { color: #80cbc4 !important; }
[data-testid="stMetricDelta"] { font-size: .85rem !important; }

/* ── buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00897b, #1de9b6) !important;
    color: #001a12 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    transition: transform .15s, box-shadow .15s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px #00bfa544;
}

/* ── selectbox / radio ── */
.stSelectbox label, .stRadio label { color: #b2dfdb !important; font-size: .93rem; }
div[data-baseweb="select"] > div {
    background: #0d2418 !important;
    border: 1px solid #1b5e3b !important;
    color: #e8f5e9 !important;
    border-radius: 8px !important;
}

/* ── progress bar ── */
.stProgress > div > div { background: linear-gradient(90deg,#00897b,#69f0ae) !important; }

/* ── divider ── */
hr { border-color: #1b3a2a !important; }

/* ── info / warning / success boxes ── */
.stAlert { border-radius: 10px !important; }

/* ── hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #003d1f 0%, #00251a 50%, #001a12 100%);
    border: 1px solid #1de9b655;
    border-radius: 20px;
    padding: 2.5rem 2.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, #1de9b622 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 900;
    color: #69f0ae;
    margin: 0 0 .4rem;
    line-height: 1.15;
}
.hero-sub {
    font-size: 1.05rem;
    color: #80cbc4;
    margin: 0;
}

/* ── game resource bar ── */
.res-bar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 1rem 0;
}
.res-chip {
    background: #0d2418;
    border: 1px solid #1b5e3b;
    border-radius: 50px;
    padding: 6px 18px;
    font-size: .9rem;
    color: #b2dfdb;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.res-chip .val { color: #69f0ae; font-weight: 700; }

/* ── card ── */
.eco-card {
    background: #0d1f17;
    border: 1px solid #1b3a2a;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}

/* ── node badge ── */
.node-badge {
    display: inline-block;
    background: #003d1f;
    border: 1px solid #00897b;
    color: #69f0ae;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: .82rem;
    margin: 2px;
}
.node-badge.visited {
    background: #1b5e20;
    border-color: #69f0ae;
}

/* ── survey question card ── */
.q-card {
    background: #0d1f17;
    border-left: 4px solid #00897b;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
.q-theory { font-size: .75rem; color: #4db6ac; margin-bottom: 4px; }
.q-text { font-size: 1rem; color: #e8f5e9; }

/* ── footer ── */
.eco-footer {
    text-align: center;
    color: #2e5945;
    font-size: .8rem;
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #1b3a2a;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        # Game state
        "game_started": False,
        "current_node": "제주공항",
        "visited": ["제주공항"],
        "path_edges": [],          # list of (from, to, transport)
        "time_left": 480,          # minutes
        "carbon_left": 3000,       # grams
        "budget_left": 80000,      # won
        "game_log": [],
        "game_over": False,
        "game_won": False,
        # Survey state
        "survey_responses": [],    # list of dicts
        "survey_submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
#  GAME DATA
# ─────────────────────────────────────────────
NODES = {
    "제주공항":       {"en": "Jeju Airport",       "lat": 33.511, "lng": 126.493, "icon": "✈️"},
    "협재해변":       {"en": "Hyeopjae Beach",      "lat": 33.394, "lng": 126.240, "icon": "🏖️"},
    "곶자왈도립공원": {"en": "Gotjawal Park",       "lat": 33.318, "lng": 126.320, "icon": "🌳"},
    "서귀포치유의숲": {"en": "Seogwipo Forest",     "lat": 33.252, "lng": 126.498, "icon": "🌲"},
    "성산일출봉":     {"en": "Seongsan Sunrise",    "lat": 33.459, "lng": 126.942, "icon": "🏔️"},
    "함덕해변":       {"en": "Hamdeok Beach",       "lat": 33.543, "lng": 126.669, "icon": "🌊"},
}

# Edge data: (nodeA, nodeB) -> {bus: (time,carbon,cost), ev: (time,carbon,cost)}
# time(min), carbon(g), cost(won)
EDGES = {
    ("제주공항", "협재해변"):       {"bus": (60, 120, 1500),  "ev": (35, 350, 12000)},
    ("제주공항", "함덕해변"):       {"bus": (30,  60, 1200),  "ev": (20, 250, 8000)},
    ("제주공항", "성산일출봉"):     {"bus": (90, 180, 3000),  "ev": (55, 450, 18000)},
    ("협재해변", "곶자왈도립공원"): {"bus": (40,  80, 1200),  "ev": (25, 300, 9000)},
    ("협재해변", "서귀포치유의숲"): {"bus": (80, 160, 2500),  "ev": (50, 420, 16000)},
    ("곶자왈도립공원", "서귀포치유의숲"): {"bus": (45, 90, 1500), "ev": (30, 310, 10000)},
    ("서귀포치유의숲", "성산일출봉"): {"bus": (100, 200, 3500), "ev": (65, 500, 20000)},
    ("성산일출봉", "함덕해변"):     {"bus": (50, 100, 1800),  "ev": (32, 320, 11000)},
    ("함덕해변", "협재해변"):       {"bus": (70, 140, 2000),  "ev": (45, 380, 14000)},
    ("곶자왈도립공원", "성산일출봉"): {"bus": (95, 190, 3200), "ev": (60, 470, 19000)},
    ("서귀포치유의숲", "함덕해변"): {"bus": (110, 220, 3800), "ev": (70, 520, 22000)},
}

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
#  GRAPH DRAWING (matplotlib / networkx)
# ─────────────────────────────────────────────
# Fixed positions based on approximate lat/lng mapped to canvas
NODE_POS = {
    "제주공항":       (0.42, 0.72),
    "협재해변":       (0.10, 0.45),
    "곶자왈도립공원": (0.25, 0.28),
    "서귀포치유의숲": (0.45, 0.10),
    "성산일출봉":     (0.90, 0.55),
    "함덕해변":       (0.72, 0.82),
}

def draw_game_graph():
    G = nx.Graph()
    for node in NODES:
        G.add_node(node)
    for (a, b) in EDGES:
        G.add_edge(a, b)

    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor("#0a0f0d")
    ax.set_facecolor("#0a0f0d")
    ax.axis("off")

    pos = NODE_POS

    # Draw background island silhouette hint
    ellipse = mpatches.Ellipse((0.5, 0.45), 0.92, 0.78,
                                angle=10, linewidth=0,
                                facecolor="#0d2418", alpha=0.5)
    ax.add_patch(ellipse)

    # Collect traversed edges
    traversed = set()
    for (frm, to, _) in st.session_state.path_edges:
        traversed.add((frm, to))
        traversed.add((to, frm))

    # Draw all edges (faint)
    for (a, b) in EDGES:
        x = [pos[a][0], pos[b][0]]
        y = [pos[a][1], pos[b][1]]
        ax.plot(x, y, color="#1b3a2a", linewidth=1.2, zorder=1, alpha=0.7)

    # Draw traversed edges (bright)
    for (a, b) in set([(f, t) for (f, t, _) in st.session_state.path_edges]):
        ed = get_edge(a, b)
        if ed is None: continue
        x = [pos[a][0], pos[b][0]]
        y = [pos[a][1], pos[b][1]]
        ax.plot(x, y, color="#69f0ae", linewidth=4, zorder=2, alpha=0.9)
        # Arrow mid-point
        mx, my = (x[0]+x[1])/2, (y[0]+y[1])/2
        ax.annotate("", xy=(x[1], y[1]), xytext=(mx, my),
                    arrowprops=dict(arrowstyle="->", color="#69f0ae", lw=1.5),
                    zorder=3)

    # Draw nodes
    for node, (nx_, ny_) in pos.items():
        visited = node in st.session_state.visited
        current = node == st.session_state.current_node

        outer_c = "#69f0ae" if current else ("#1de9b6" if visited else "#1b3a2a")
        inner_c = "#003d1f" if visited else "#0a0f0d"
        size_out = 280 if current else 200
        size_in  = 160 if current else 130

        ax.scatter(nx_, ny_, s=size_out, color=outer_c, zorder=4, alpha=0.95)
        ax.scatter(nx_, ny_, s=size_in,  color=inner_c, zorder=5)

        icon = NODES[node]["icon"]
        # Label: Korean + English
        short_en = NODES[node]["en"].replace(" ", "\n")
        label = f'{icon}\n{node}\n({NODES[node]["en"]})'
        yoff = -0.09 if ny_ > 0.5 else 0.09
        ax.text(nx_, ny_ + yoff, f"{icon} {node}", ha="center", va="center",
                fontsize=7.5, color="#e8f5e9",
                fontproperties=None,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#0d2418",
                          edgecolor="#1b3a2a", alpha=0.85),
                zorder=6)

    # Title
    ax.text(0.5, 0.97, "🗺️ 제주 에코 레이스 — 이동 경로", ha="center", va="top",
            transform=ax.transAxes, fontsize=11, color="#69f0ae", fontweight="bold")

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    plt.tight_layout(pad=0.5)
    return fig

# ─────────────────────────────────────────────
#  SURVEY DATA & NETWORK VIZ
# ─────────────────────────────────────────────
QUESTIONS = [
    {"theory": "NAM — 결과 인지 (Awareness of Consequences)",
     "text": "내가 비닐봉지를 많이 쓰면 바다 생물에게 직접적인 피해를 준다고 생각한다."},
    {"theory": "NAM — 책임 귀속 (Ascription of Responsibility)",
     "text": "환경 문제를 해결하는 것은 나를 포함한 모든 시민의 책임이다."},
    {"theory": "VBN — 생태적 가치관 (Biospheric Value)",
     "text": "자연은 인간의 이익과 상관없이 그 자체로 보호받아야 한다."},
    {"theory": "TPB — 주관적 규범 (Subjective Norm)",
     "text": "내 주변 친구들은 환경을 위한 행동(분리수거, 텀블러 사용 등)을 중요하게 생각한다."},
    {"theory": "TPB — 지각된 행동 통제감 (Perceived Behavioral Control)",
     "text": "나는 환경을 위한 행동을 실천하는 것이 어렵지 않다고 느낀다."},
]

LIKERT = ["① 매우 그렇지 않다", "② 그렇지 않다", "③ 보통이다", "④ 그렇다", "⑤ 매우 그렇다"]

def mock_responses(n=50):
    names_pool = [f"학생{i+1:03d}" for i in range(n)]
    profiles = [
        {"bias": [4,4,4,3,3], "label": "생태 시민형"},
        {"bias": [3,3,2,4,4], "label": "사회 규범형"},
        {"bias": [2,2,3,2,4], "label": "실천 자신감형"},
        {"bias": [1,2,1,2,2], "label": "무관심형"},
        {"bias": [3,4,4,2,3], "label": "책임 의식형"},
    ]
    responses = []
    for i, name in enumerate(names_pool):
        prof = profiles[i % len(profiles)]
        scores = []
        for bias in prof["bias"]:
            s = min(5, max(1, bias + random.randint(-1, 1)))
            scores.append(s)
        responses.append({
            "name": name,
            "scores": scores,
            "profile": prof["label"],
            "time": datetime.now().isoformat()
        })
    return responses

def build_response_network(responses):
    """Build a network where nodes = students, edges = similarity."""
    G = nx.Graph()
    for r in responses:
        G.add_node(r["name"], profile=r["profile"], scores=r["scores"])

    # Connect students with cosine similarity > threshold
    threshold = 0.92
    n = len(responses)
    for i in range(n):
        for j in range(i+1, n):
            a = np.array(responses[i]["scores"], dtype=float)
            b = np.array(responses[j]["scores"], dtype=float)
            sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
            if sim >= threshold:
                G.add_edge(responses[i]["name"], responses[j]["name"], weight=sim)
    return G

PROFILE_COLORS = {
    "생태 시민형":    "#69f0ae",
    "사회 규범형":    "#40c4ff",
    "실천 자신감형":  "#ffd740",
    "책임 의식형":    "#ff6e40",
    "무관심형":       "#b0bec5",
    "나(직접 참여)":  "#ea80fc",
}

def draw_response_network(responses):
    if not responses:
        return None
    G = build_response_network(responses)
    if G.number_of_nodes() == 0:
        return None

    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor("#0a0f0d")
    ax.set_facecolor("#0a0f0d")
    ax.axis("off")

    k_val = 1.2 / math.sqrt(max(G.number_of_nodes(), 1))
    pos = nx.spring_layout(G, k=k_val, seed=42, iterations=60)

    # Edge width by weight
    edges = G.edges(data=True)
    edge_list = list(edges)
    if edge_list:
        weights = [d.get("weight", 0.9) for _, _, d in edge_list]
        widths  = [w * 3.5 for w in weights]
        nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.35,
                               edge_color="#1de9b6", width=widths)

    # Node colors
    profiles = nx.get_node_attributes(G, "profile")
    node_colors = [PROFILE_COLORS.get(profiles.get(n, ""), "#80cbc4") for n in G.nodes()]
    sizes = [220 if profiles.get(n, "") == "나(직접 참여)" else 150 for n in G.nodes()]

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=sizes, alpha=0.9)

    # Labels only for direct participants
    direct = {n: n for n in G.nodes() if profiles.get(n, "") == "나(직접 참여)"}
    if direct:
        nx.draw_networkx_labels(G, pos, labels=direct, ax=ax,
                                font_size=7, font_color="#fff")

    # Legend
    legend_items = []
    seen_profiles = set(profiles.values())
    for prof, col in PROFILE_COLORS.items():
        if prof in seen_profiles:
            legend_items.append(mpatches.Patch(color=col, label=prof))
    if legend_items:
        ax.legend(handles=legend_items, loc="lower left",
                  facecolor="#0d2418", edgecolor="#1b3a2a",
                  labelcolor="#e8f5e9", fontsize=8,
                  framealpha=0.9)

    ax.set_title(f"우리 반 환경행동 네트워크 — 참여자 {G.number_of_nodes()}명 / 연결 {G.number_of_edges()}개",
                 color="#69f0ae", fontsize=11, pad=12)
    plt.tight_layout(pad=0.5)
    return fig

# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 제주 에코 네트워크")
    st.markdown("---")
    menu = st.radio(
        "메뉴 선택",
        ["🏠 홈 (소개)", "🎮 삼다수 에코 레이스", "📊 우리 반 환경행동 네트워크"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
<div style='font-size:.8rem; color:#2e7d5f; line-height:1.6;'>
네트워크 사이언스 × 환경 교육<br>
제주 중학생 대상 1시간 체험 프로그램<br><br>
동시 접속: 최대 100명<br>
제작: 에코 네트워크 연구팀
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: HOME
# ─────────────────────────────────────────────
if menu == "🏠 홈 (소개)":
    st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🌿 제주 에코 네트워크</div>
  <div class='hero-sub'>네트워크 사이언스 × 데이터 사이언스 × 환경 교육 — 1시간 체험 프로그램</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
<div class='eco-card'>
  <h3>🎮 삼다수 에코 레이스</h3>
  <p style='color:#80cbc4; font-size:.95rem;'>
  제주도의 6개 생태 거점을 탐험하는 네트워크 게임!<br>
  대중교통 vs. 전기 렌터카 중 최적의 이동 수단을 선택하며<br>
  <b style='color:#69f0ae;'>시간 · 탄소 · 비용</b> 세 가지 자원을 관리해보세요.<br><br>
  지름길이 항상 정답이 아닙니다. 트레이드오프를 분석해 가장 많은 생태 거점을 복구하세요!
  </p>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class='eco-card'>
  <h3>📊 우리 반 환경행동 네트워크</h3>
  <p style='color:#80cbc4; font-size:.95rem;'>
  5가지 학술 이론(NAM · VBN · TPB)에 기반한 환경 설문에 참여하면,<br>
  우리 반 친구들의 응답이 <b style='color:#69f0ae;'>실시간 네트워크 그래프</b>로 펼쳐집니다.<br><br>
  나와 비슷한 환경 가치관을 가진 친구는 누구일까요? 데이터가 직접 알려줍니다!
  </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔬 오늘 배우는 개념")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
<div class='eco-card' style='text-align:center;'>
  <div style='font-size:2rem;'>🕸️</div>
  <b style='color:#69f0ae;'>네트워크 사이언스</b>
  <p style='color:#80cbc4; font-size:.87rem; margin-top:.5rem;'>
  노드(점)와 링크(선)로 세상의 연결을 표현하는 과학. 우리의 사회 관계, 인터넷, 생태계 모두 네트워크입니다.
  </p>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class='eco-card' style='text-align:center;'>
  <div style='font-size:2rem;'>📈</div>
  <b style='color:#69f0ae;'>데이터 사이언스</b>
  <p style='color:#80cbc4; font-size:.87rem; margin-top:.5rem;'>
  수집된 데이터에서 숨겨진 패턴을 찾아내는 기술. 설문 데이터가 어떻게 시각화되는지 직접 경험해보세요.
  </p>
</div>
""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class='eco-card' style='text-align:center;'>
  <div style='font-size:2rem;'>🌏</div>
  <b style='color:#69f0ae;'>환경 행동 이론</b>
  <p style='color:#80cbc4; font-size:.87rem; margin-top:.5rem;'>
  NAM · VBN · TPB — 사람들이 왜 환경 행동을 하는지(또는 안 하는지) 설명하는 사회과학 이론입니다.
  </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='eco-footer'>
제주특별자치도 환경 교육 프로그램 · 네트워크 사이언스 & 데이터 사이언스 체험 수업
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: GAME — 삼다수 에코 레이스
# ─────────────────────────────────────────────
elif menu == "🎮 삼다수 에코 레이스":
    st.markdown("## 🎮 삼다수 에코 레이스")
    st.markdown("제주도 생태 거점을 최적의 경로로 탐험하세요. 탄소를 아끼고 시간과 비용도 관리해야 합니다!")

    # ── Resource display ──
    time_pct   = st.session_state.time_left   / 480  * 100
    carbon_pct = st.session_state.carbon_left / 3000 * 100
    budget_pct = st.session_state.budget_left / 80000 * 100

    col_t, col_c, col_b, col_v = st.columns(4)
    col_t.metric("⏱️ 남은 시간", f"{st.session_state.time_left}분",
                 delta=f"총 480분 중" if not st.session_state.game_started else None)
    col_c.metric("🌿 탄소 예산", f"{st.session_state.carbon_left:,}g",
                 delta="3,000g 시작" if not st.session_state.game_started else None)
    col_b.metric("💰 잔여 비용", f"₩{st.session_state.budget_left:,}",
                 delta="₩80,000 시작" if not st.session_state.game_started else None)
    col_v.metric("📍 방문 거점", f"{len(st.session_state.visited)}개 / 6개")

    # Progress bars
    st.markdown("**자원 현황**")
    bar_col1, bar_col2, bar_col3 = st.columns(3)
    with bar_col1:
        st.caption("⏱️ 시간")
        st.progress(max(0, min(1, time_pct/100)))
    with bar_col2:
        st.caption("🌿 탄소")
        st.progress(max(0, min(1, carbon_pct/100)))
    with bar_col3:
        st.caption("💰 비용")
        st.progress(max(0, min(1, budget_pct/100)))

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
            cls = "node-badge visited" if node in st.session_state.visited else "node-badge"
            icon = NODES[node]["icon"]
            visited_html += f'<span class="{cls}">{icon} {node}</span>'
        st.markdown(f"<div style='margin-top:.5rem;'>{visited_html}</div>", unsafe_allow_html=True)

    with ctrl_col:
        st.markdown("### 🧭 이동 제어판")

        if st.session_state.game_over:
            if st.session_state.game_won:
                st.success("🎉 모든 생태 거점을 복구했습니다! 에코 챔피언!")
            else:
                total_v = len(st.session_state.visited) - 1
                st.warning(f"⚠️ 자원 소진! {total_v}개 거점을 복구했습니다.")
            st.markdown(f"**최종 방문:** {len(st.session_state.visited)-1}개 생태 거점")
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
                st.markdown(f"**총 {len(st.session_state.visited)-1}개** 생태 거점을 복구했습니다! 🎉")
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
  <b style='color:#b2dfdb;'>예상 소모 자원 미리보기</b>
  <div style='margin-top:.5rem; font-size:.9rem;'>
    ⏱️ 시간: <span style='color:#69f0ae;'><b>{preview_time}분</b></span><br>
    🌿 탄소: <span style='color:#69f0ae;'><b>{base_carbon:,}g</b></span><br>
    💰 비용: <span style='color:#69f0ae;'><b>₩{base_cost:,}</b></span><br>
    <span style='color:#4db6ac; font-size:.83rem;'>{dice_note}</span>
  </div>
</div>
""", unsafe_allow_html=True)

                    if st.button(f"🚀 {dest}(으)로 이동하기!"):
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

                        # Check game over
                        if (st.session_state.time_left <= 0 or
                            st.session_state.carbon_left <= 0 or
                            st.session_state.budget_left <= 0):
                            st.session_state.game_over = True
                        if len(st.session_state.visited) == len(NODES):
                            st.session_state.game_won = True
                            st.session_state.game_over = True
                        st.rerun()

        # ── Travel log ──
        if st.session_state.game_log:
            st.markdown("---")
            st.markdown("### 📋 이동 기록")
            for entry in reversed(st.session_state.game_log[-6:]):
                st.markdown(f"<div style='font-size:.82rem; color:#80cbc4; padding:3px 0;'>{entry}</div>",
                            unsafe_allow_html=True)

    # ── Game rules ──
    with st.expander("📖 게임 규칙 & 힌트 보기"):
        st.markdown("""
**🎯 목표**: 제주공항에서 출발해 480분(8시간), 탄소 3,000g, 예산 ₩80,000 안에 최대한 많은 생태 거점을 방문하세요.

**🚌 대중교통 (버스)**
- 탄소 배출이 **매우 적음** (친환경 ✅)
- 대기 시간 패널티: 이동할 때마다 **0~30분**의 랜덤 추가 시간 발생 🎲
- 비용이 저렴함

**⚡ 전기 렌터카**
- 이동 시간이 **정확하고 빠름** (패널티 없음)
- 탄소 배출이 버스보다 **3~5배 많음**
- 비용이 비쌈 💸

**💡 전략 팁**
- 짧은 거리는 버스가 유리할 수 있어요 (시간 패널티가 적음)
- 탄소 예산을 아끼면 환경 점수 보너스!
- 거점 간 거리를 고려해 효율적인 순서를 계획하세요
""")

# ─────────────────────────────────────────────
#  PAGE: SURVEY & NETWORK
# ─────────────────────────────────────────────
elif menu == "📊 우리 반 환경행동 네트워크":
    st.markdown("## 📊 우리 반 환경행동 네트워크")
    st.markdown("5가지 환경 심리 이론 기반 설문에 답하면, 우리 반 환경행동 네트워크가 실시간으로 그려집니다!")

    tab1, tab2 = st.tabs(["✏️ 설문 참여", "🕸️ 네트워크 시각화"])

    # ── Tab 1: Survey ──
    with tab1:
        st.markdown("### ✏️ 환경행동 설문 (5문항)")
        st.markdown("""
<div class='eco-card'>
  <b style='color:#69f0ae;'>📚 이론 배경 간단 소개</b>
  <ul style='color:#80cbc4; font-size:.9rem; margin:.5rem 0 0;'>
    <li><b style='color:#b2dfdb;'>NAM (규범 활성화 이론)</b>: 결과를 인지하고 책임을 느낄수록 환경 행동을 한다</li>
    <li><b style='color:#b2dfdb;'>VBN (가치-신념-규범 이론)</b>: 생태적 가치관이 환경 행동의 기반이 된다</li>
    <li><b style='color:#b2dfdb;'>TPB (계획된 행동이론)</b>: 주변 사람들의 기대와 자신감이 행동을 결정한다</li>
  </ul>
</div>
""", unsafe_allow_html=True)

        nickname = st.text_input("📛 닉네임 (익명 가능, 예: 초록이23)", max_chars=20,
                                  placeholder="닉네임을 입력하세요")
        scores = []
        all_answered = True

        for i, q in enumerate(QUESTIONS):
            st.markdown(f"""
<div class='q-card'>
  <div class='q-theory'>📌 {q['theory']}</div>
  <div class='q-text'>Q{i+1}. {q['text']}</div>
</div>
""", unsafe_allow_html=True)
            val = st.radio(
                f"Q{i+1}",
                LIKERT,
                key=f"q_{i}",
                horizontal=True,
                label_visibility="collapsed",
                index=None,
            )
            if val is None:
                all_answered = False
                scores.append(0)
            else:
                scores.append(LIKERT.index(val) + 1)

        col_sub, col_reset = st.columns([2, 1])
        with col_sub:
            if st.button("✅ 설문 제출하기", disabled=(not all_answered or not nickname.strip())):
                # Check duplicate
                existing_names = [r["name"] for r in st.session_state.survey_responses]
                if nickname in existing_names:
                    st.warning("이미 같은 닉네임으로 제출되었습니다. 닉네임을 바꿔주세요.")
                else:
                    entry = {
                        "name": nickname.strip(),
                        "scores": scores,
                        "profile": "나(직접 참여)",
                        "time": datetime.now().isoformat(),
                    }
                    st.session_state.survey_responses.append(entry)
                    st.session_state.survey_submitted = True
                    st.success(f"🎉 {nickname}님의 응답이 제출되었습니다! '네트워크 시각화' 탭을 확인하세요.")

        with col_reset:
            if not all_answered:
                st.caption("⚠️ 모든 문항에 답해주세요")
            if not nickname.strip():
                st.caption("⚠️ 닉네임을 입력해주세요")

        st.markdown("---")
        st.markdown(f"**현재 누적 참여자:** {len(st.session_state.survey_responses)}명")

    # ── Tab 2: Network viz ──
    with tab2:
        st.markdown("### 🕸️ 환경행동 네트워크 시각화")

        btn_col1, btn_col2 = st.columns([2, 1])
        with btn_col1:
            if st.button("🤖 가상 데이터 생성 (Mock 50명)"):
                mock = mock_responses(50)
                # Merge with real, avoid duplicates
                existing = {r["name"] for r in st.session_state.survey_responses}
                new_mock = [r for r in mock if r["name"] not in existing]
                st.session_state.survey_responses.extend(new_mock)
                st.success(f"✅ 가상 학생 {len(new_mock)}명의 데이터가 추가되었습니다!")
                st.rerun()
        with btn_col2:
            if st.button("🗑️ 전체 데이터 초기화"):
                st.session_state.survey_responses = []
                st.session_state.survey_submitted = False
                st.rerun()

        responses = st.session_state.survey_responses
        if not responses:
            st.info("아직 데이터가 없습니다. 설문에 참여하거나 '가상 데이터 생성' 버튼을 눌러주세요!")
        else:
            # Stats
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            all_scores = np.array([r["scores"] for r in responses])
            avg_scores = all_scores.mean(axis=0)

            stat_col1.metric("👥 참여 인원", f"{len(responses)}명")
            stat_col2.metric("🌿 평균 생태 가치관(Q3)", f"{avg_scores[2]:.2f} / 5")
            stat_col3.metric("💪 평균 실천 자신감(Q5)", f"{avg_scores[4]:.2f} / 5")

            # Network graph
            with st.spinner("네트워크 그래프를 그리는 중..."):
                fig = draw_response_network(responses)
            if fig:
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            # Profile distribution
            st.markdown("---")
            st.markdown("### 📊 환경 성향 분포")
            from collections import Counter
            profile_counts = Counter(r["profile"] for r in responses)

            bar_data_labels = list(profile_counts.keys())
            bar_data_values = list(profile_counts.values())

            fig2, ax2 = plt.subplots(figsize=(8, 3))
            fig2.patch.set_facecolor("#0a0f0d")
            ax2.set_facecolor("#0a0f0d")
            colors = [PROFILE_COLORS.get(l, "#80cbc4") for l in bar_data_labels]
            bars = ax2.barh(bar_data_labels, bar_data_values, color=colors, height=0.5)
            ax2.set_xlabel("인원 수", color="#80cbc4")
            ax2.tick_params(colors="#b2dfdb", labelsize=9)
            ax2.spines[:].set_color("#1b3a2a")
            for bar, val in zip(bars, bar_data_values):
                ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                         str(val), va="center", color="#69f0ae", fontsize=9)
            plt.tight_layout(pad=0.5)
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)

            # Q-by-Q avg bar
            st.markdown("### 📈 문항별 평균 점수")
            q_labels = [f"Q{i+1}" for i in range(5)]
            fig3, ax3 = plt.subplots(figsize=(8, 2.5))
            fig3.patch.set_facecolor("#0a0f0d")
            ax3.set_facecolor("#0a0f0d")
            bar_colors = ["#69f0ae","#40c4ff","#ffd740","#ff6e40","#b39ddb"]
            bars3 = ax3.bar(q_labels, avg_scores, color=bar_colors, width=0.5)
            ax3.set_ylim(0, 5.5)
            ax3.set_ylabel("평균 점수", color="#80cbc4")
            ax3.tick_params(colors="#b2dfdb", labelsize=9)
            ax3.spines[:].set_color("#1b3a2a")
            for bar, val in zip(bars3, avg_scores):
                ax3.text(bar.get_x() + bar.get_width()/2, val + 0.1,
                         f"{val:.2f}", ha="center", color="#e8f5e9", fontsize=8.5)
            q_short = ["결과인지\n(NAM)", "책임귀속\n(NAM)", "생태가치\n(VBN)",
                       "주관규범\n(TPB)", "행동통제\n(TPB)"]
            ax3.set_xticks(range(5))
            ax3.set_xticklabels(q_short, fontsize=7.5, color="#b2dfdb")
            plt.tight_layout(pad=0.5)
            st.pyplot(fig3, use_container_width=True)
            plt.close(fig3)

            # Data table (expander)
            with st.expander("📋 원시 데이터 테이블 보기"):
                import pandas as pd
                rows = []
                for r in responses:
                    row = {"닉네임": r["name"], "성향": r["profile"]}
                    for i, s in enumerate(r["scores"]):
                        row[f"Q{i+1}"] = s
                    rows.append(row)
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)

    st.markdown("""
<div class='eco-footer'>
NAM: Norm Activation Model (Schwartz, 1977) &nbsp;·&nbsp;
VBN: Value-Belief-Norm Theory (Stern, 2000) &nbsp;·&nbsp;
TPB: Theory of Planned Behavior (Ajzen, 1991)
</div>
""", unsafe_allow_html=True)
