import math
import random
import json
from collections import Counter
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
from shared import apply_css, _korean_font, get_chart_colors, show_theory

apply_css()

# ─────────────────────────────────────────────
#  GAME 2 전용 데이터 (이 게임만 사용)
# ─────────────────────────────────────────────

# 15문항: 태도(A1-3) · 주관적 규범(SN1-3) · 지각된 행동통제감(PBC1-3) · 행동의도(I1)
QUESTIONS = [
    # ── 태도: 인지적 태도 (Instrumental Attitude) ──
    {"theory": "IA1 · 인지적 태도",
     "text": "분리수거, 텀블러 사용 같은 환경 행동은 가치 있는 일이라고 생각한다.",
     "reverse": False},
    {"theory": "IA2 · 인지적 태도",
     "text": "환경을 위해 불편함을 감수하는 것은 의미 있는 일이다.",
     "reverse": False},

    # ── 태도: 감정적 태도 (Affective Attitude) ──
    {"theory": "AA1 · 감정적 태도",
     "text": "환경 행동을 실천하고 나면 뿌듯하고 기분이 좋다.",
     "reverse": False},
    {"theory": "AA2 · 감정적 태도",
     "text": "내가 환경 행동을 해도 지구에 별 도움이 안 될 것 같아 허무하다.",
     "reverse": True},

    # ── 주관적 규범: 명령적 규범 (Injunctive Norm) ──
    {"theory": "INJ1 · 명령적 규범",
     "text": "우리 가족은 내가 환경을 위한 행동을 실천하길 바란다.",
     "reverse": False},
    {"theory": "INJ2 · 명령적 규범",
     "text": "선생님이나 어른들이 환경 행동을 강조할 때 나도 해야겠다는 생각이 든다.",
     "reverse": False},

    # ── 주관적 규범: 서술적 규범 (Descriptive Norm) ──
    {"theory": "DESC1 · 서술적 규범",
     "text": "내 친구들 대부분은 실제로 환경을 위한 행동을 실천하고 있다.",
     "reverse": False},
    {"theory": "DESC2 · 서술적 규범",
     "text": "우리 반 대부분의 학생들은 분리수거나 일회용품 줄이기를 잘 실천한다.",
     "reverse": False},

    # ── 지각된 행동통제: 자기효능감 (Self-Efficacy) ──
    {"theory": "SE1 · 자기효능감",
     "text": "나는 분리수거, 텀블러 사용 같은 환경 행동을 실천하는 것이 어렵지 않다.",
     "reverse": False},
    {"theory": "SE2 · 자기효능감",
     "text": "나는 환경을 위한 행동을 꾸준히 실천할 자신이 있다.",
     "reverse": False},

    # ── 지각된 행동통제: 통제가능성 (Controllability) ──
    {"theory": "CTR1 · 통제가능성",
     "text": "환경 행동을 하고 싶어도 귀찮거나 불편해서 못 하는 경우가 많다.",
     "reverse": True},
    {"theory": "CTR2 · 통제가능성",
     "text": "환경 행동을 하느냐 마느냐는 전적으로 나의 선택과 의지에 달려 있다.",
     "reverse": False},

    # ── 행동 의도 (Behavioral Intention) ──
    {"theory": "INT1 · 행동 의도",
     "text": "나는 앞으로 환경을 위한 행동을 더 자주 실천할 것이다.",
     "reverse": False},
    {"theory": "INT2 · 행동 의도",
     "text": "이번 제주 여행 이후에도 환경 행동을 계속 실천할 계획이다.",
     "reverse": False},
    {"theory": "INT3 · 행동 의도",
     "text": "나는 주변 친구들에게도 환경 행동을 함께 하자고 권유할 것이다.",
     "reverse": False},
]

LIKERT = ["① 매우 그렇지 않다", "② 그렇지 않다", "③ 보통이다", "④ 그렇다", "⑤ 매우 그렇다"]

# 환경 성향 프로필 → 색상
PROFILE_COLORS = {
    "적극 실천형":   "#69f0ae",
    "사회 규범형":   "#40c4ff",
    "자신감형":      "#ffd740",
    "가치 인식형":   "#ff6e40",
    "무관심형":      "#b0bec5",
    "나(직접 참여)": "#ea80fc",
}


def mock_responses(n=50):
    """가상 학생 n명의 설문 응답을 생성한다 (5가지 성향 프로필 기반)."""
    names_pool = [f"학생{i+1:03d}" for i in range(n)]
    profiles = [
        {"bias": [5,5,2,4,4,4,5,2,5,5], "label": "적극 실천형"},
        {"bias": [4,4,3,5,5,5,3,3,3,4], "label": "사회 규범형"},
        {"bias": [3,3,3,2,2,2,4,2,4,3], "label": "자신감형"},
        {"bias": [2,2,4,3,3,2,2,4,2,2], "label": "무관심형"},
        {"bias": [4,3,2,3,4,4,2,3,2,3], "label": "가치 인식형"},
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
            "time": datetime.now().isoformat(),
        })
    return responses


def build_response_network(responses):
    """응답 벡터의 코사인 유사도가 높은 학생들끼리 연결되는 네트워크 그래프를 생성한다."""
    G = nx.Graph()
    for r in responses:
        G.add_node(r["name"], profile=r["profile"], scores=r["scores"])

    threshold = 0.92
    n = len(responses)
    for i in range(n):
        for j in range(i + 1, n):
            a = np.array(responses[i]["scores"], dtype=float)
            b = np.array(responses[j]["scores"], dtype=float)
            sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
            if sim >= threshold:
                G.add_edge(responses[i]["name"], responses[j]["name"], weight=sim)
    return G


def draw_response_network(responses):
    """환경행동 네트워크 그래프를 그린다. 응답이 없으면 None 반환."""
    ch = get_chart_colors() 
    if not responses:
        return None
    G = build_response_network(responses)
    if G.number_of_nodes() == 0:
        return None

    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")
    ax.axis("off")

    k_val = 1.2 / math.sqrt(max(G.number_of_nodes(), 1))
    pos = nx.spring_layout(G, k=k_val, seed=42, iterations=60)

    # Edge width by weight
    edge_list = list(G.edges(data=True))
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
        leg = ax.legend(handles=legend_items, loc="lower left",
                        facecolor=ch["card"], edgecolor=ch["spine"],
                        labelcolor=ch["text"], fontsize=8, framealpha=0.9)
        if _korean_font:
            for text in leg.get_texts():
                text.set_fontproperties(_korean_font)
                text.set_fontsize(8)

    title_str = f"우리 반 환경행동 네트워크 — 참여자 {G.number_of_nodes()}명 / 연결 {G.number_of_edges()}개"
    if _korean_font:
        ax.set_title(title_str, fontproperties=_korean_font, color=ch["accent"], fontsize=11, pad=12)
    else:
        ax.set_title(title_str, color=ch["accent"], fontsize=11, pad=12)

    plt.tight_layout(pad=0.5)
    return fig

def draw_dynamic_response_network(responses, height=650):
    if not responses:
        return

    G = build_response_network(responses)

    nodes = []
    for node, data in G.nodes(data=True):
        profile = data.get("profile", "")
        nodes.append({
            "id": node,
            "label": node if profile == "나(직접 참여)" else node,
            "profile": profile,
            "size": 12 if profile == "나(직접 참여)" else 6,
            "color": PROFILE_COLORS.get(profile, "#80cbc4"),
        })

    edges = []
    for source, target, data in G.edges(data=True):
        edges.append({
            "source": source,
            "target": target,
            "weight": float(data.get("weight", 1.0)),
        })

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)

    html = """
    <div style="
        background:#ffffff;
        border:1px solid #d9e8df;
        border-radius:16px;
        padding:12px;
    ">
        <div style="font-size:18px; font-weight:800; color:#1b3a2a; margin-bottom:10px; font-family:'Noto Sans KR',sans-serif;">
            🎨 유형 버튼을 눌러보세요 — 고른 유형만 선명하게, 나머지는 흐려집니다
        </div>
        <div id="chips" style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px;"></div>

        <div id="sigma-container" style="
            width:100%;
            height:__HEIGHT__px;
            background:#ffffff;
            border:1px solid #d9e8df;
            border-radius:12px;
            overflow:hidden;
            position:relative;
        "></div>

        <div id="fx-explain" style="margin-top:14px; padding:14px 16px; border-radius:12px;
            background:#f3f7f4; color:#1b3a2a; font-size:18px; line-height:1.6;
            font-family:'Noto Sans KR',sans-serif;">👆 위 유형 버튼을 누르면, 그 유형 설명이 여기에 나타나요.</div>
    </div>

    <script type="module">
    import Graph from "https://cdn.jsdelivr.net/npm/graphology@0.26.0/+esm";
    import { Sigma } from "https://cdn.jsdelivr.net/npm/sigma@2.4.0/+esm";
    import forceAtlas2 from "https://cdn.jsdelivr.net/npm/graphology-layout-forceatlas2@0.10.1/+esm";
    
    const nodes = __NODES__;
    const edges = __EDGES__;
    
    const container = document.getElementById("sigma-container");
    const graph = new Graph();
    
    nodes.forEach((node) => {
        graph.addNode(node.id, {
            label: node.label,
            profile: node.profile,
            x: Math.random() * 2 - 1,
            y: Math.random() * 2 - 1,
            size: node.size,
            color: node.color,
            origColor: node.color,
            origSize: node.size,
            hidden: false
        });
    });
    
    edges.forEach((edge, i) => {
        if (graph.hasNode(edge.source) && graph.hasNode(edge.target)) {
            graph.addEdgeWithKey("edge-" + i, edge.source, edge.target, {
                size: edge.weight * 1,
                color: "#90a4ae"
            });
        }
    });
    
    const renderer = new Sigma(graph, container, {
        renderEdgeLabels: "#90a4ae",
        defaultEdgeColor: false,
        labelColor: { color: "#1b3a2a" },
        labelSize: 15,
        labelWeight: "bold"
    });
    
    const settings = forceAtlas2.inferSettings(graph);
    let layoutRunning = true;
    
    function animate() {
        if (layoutRunning) {
            forceAtlas2.assign(graph, {
                iterations: 1,
                settings: {
                    ...settings,
                    gravity: 0.08,
                    scalingRatio: 15,
                    slowDown: 5,
                    strongGravityMode: false
                }
            });
        }
    
        renderer.refresh();
        requestAnimationFrame(animate);
    }
    
    animate();
    
    const COLORS = {"적극 실천형":"#69f0ae","사회 규범형":"#40c4ff","자신감형":"#ffd740","가치 인식형":"#ff6e40","무관심형":"#b0bec5","나(직접 참여)":"#ea80fc"};
    const EXPLAIN = {
      "적극 실천형":{e:"💪",d:"텀블러 쓰기·일회용품 안 쓰기처럼 친환경 행동을 실제로 꾸준히 실천하는 유형! 앞으로도 계속하고 친구에게도 권하는 아주 훌륭한 친구들이에요 ㅎㅎ"},
      "사회 규범형":{e:"👥",d:"가족·친구가 실천하길 바라고, 어른들이 강조하면 '나도 해야지' 도덕심이 드는 유형. 사회의 규칙을 잘 지키는 멋진 친구들이죠."},
      "자신감형":{e:"✨",d:"마음만 먹으면 분리수거·텀블러쯤 어렵지 않게 할 수 있다는 자신감이 있는 유형. 매번 지키긴 어려워도 웬만하면 지키려 노력해요~"},
      "가치 인식형":{e:"💡",d:"분리수거 같은 불편함도 '의미 있는 일'이라 여겨, 실천하고 나면 뿌듯하고 기분 좋은 유형! 어때요, 잘 맞나요?"},
      "무관심형":{e:"🍃",d:"아직 환경에 관심이 적은 유형이에요. 만약 나왔다면, 지금부터 환경을 아끼고 지키려는 작은 노력을 시작해봐요!"},
      "나(직접 참여)":{e:"🙋",d:"직접 설문에 참여한 '나'의 위치예요. 나와 가장 가까운 친구는 누구인지 찾아보세요."},
    };
    const ORDER = ["적극 실천형","사회 규범형","자신감형","가치 인식형","무관심형","나(직접 참여)"];
    const present = new Set(nodes.map((n) => n.profile));
    const chipBox = document.getElementById("chips");
    const explainBox = document.getElementById("fx-explain");
    const chipEls = {};
    let active = null;

    ORDER.filter((p) => present.has(p)).forEach((p) => {
        const b = document.createElement("button");
        b.textContent = (EXPLAIN[p] ? EXPLAIN[p].e : "") + " " + p;
        b.style.cssText = "font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:800;" +
            "padding:9px 16px;border-radius:999px;border:3px solid " + (COLORS[p]||"#ccc") + ";" +
            "background:" + (COLORS[p]||"#eee") + ";color:#123;cursor:pointer;";
        b.onclick = () => select(active === p ? null : p);
        chipBox.appendChild(b); chipEls[p] = b;
    });

    function select(p) {
        active = p;
        ORDER.forEach((q) => {
            if (!chipEls[q]) return;
            chipEls[q].style.opacity = (!p || q === p) ? "1" : "0.45";
            chipEls[q].style.boxShadow = (q === p) ? "0 0 0 4px rgba(27,58,42,.35)" : "none";
        });
        graph.forEachNode((n, a) => {
            const on = !p || a.profile === p;
            graph.setNodeAttribute(n, "color", on ? a.origColor : "#e6e6e6");
            graph.setNodeAttribute(n, "size", on ? a.origSize : a.origSize * 0.55);
        });
        graph.forEachEdge((e, a, s, t) => {
            const on = !p || graph.getNodeAttribute(s, "profile") === p || graph.getNodeAttribute(t, "profile") === p;
            graph.setEdgeAttribute(e, "color", on ? "#90a4ae" : "#eeeeee");
        });
        if (!p) {
            explainBox.innerHTML = "👆 위 유형 버튼을 누르면, 그 유형 설명이 여기에 나타나요.";
            explainBox.style.background = "#f3f7f4";
        } else {
            const ex = EXPLAIN[p] || {e:"", d:""};
            explainBox.innerHTML = "<span style='font-size:24px;'>" + ex.e + "</span> <b style='font-size:20px;'>" + p + "</b><br>" + ex.d;
            explainBox.style.background = (COLORS[p]||"#f3f7f4") + "33";
        }
        renderer.refresh();
    }
    
    let draggedNode = null;
    let isDragging = false;
    
    renderer.on("downNode", (e) => {
        isDragging = true;
        draggedNode = e.node;
        layoutRunning = false;
    });
    
    renderer.getMouseCaptor().on("mousemovebody", (e) => {
        if (!isDragging || !draggedNode) return;
    
        const pos = renderer.viewportToGraph(e);
        graph.setNodeAttribute(draggedNode, "x", pos.x);
        graph.setNodeAttribute(draggedNode, "y", pos.y);
    
        e.preventSigmaDefault();
        e.original.preventDefault();
        e.original.stopPropagation();
    });
    
    renderer.getMouseCaptor().on("mouseup", () => {
        isDragging = false;
        draggedNode = null;
    });
    </script>
    """
    
    html = (
        html
        .replace("__HEIGHT__", str(height))
        .replace("__NODES__", nodes_json)
        .replace("__EDGES__", edges_json)
    )
    
    components.html(html, height=height + 250)

def init_state():
    """설문 데이터를 담을 session_state 기본값을 설정 (이미 있으면 건너뜀)."""
    if "survey_responses" not in st.session_state:
        st.session_state.survey_responses = []
    if "survey_submitted" not in st.session_state:
        st.session_state.survey_submitted = False


init_state()

# ─────────────────────────────────────────────
#  화면 구성
# ─────────────────────────────────────────────
st.markdown("## 📊 우리 반 환경행동 네트워크")
st.markdown("5가지 환경 심리 이론 기반 설문에 답하면, 우리 반 환경행동 네트워크가 실시간으로 그려집니다!")

tab1, tab2 = st.tabs(["✏️ 설문 참여", "🕸️ 네트워크 시각화"])

# ── Tab 1: Survey ──
with tab1:
    st.markdown("### ✏️ 환경행동 설문 (15문항)")
    # 학습자 레벨에 따라 안내 콘텐츠를 분기 (설문 문항 자체는 동일)
    if show_theory():
        # 전체 · 고등 · 대학/성인 → 학술 이론(TPB) 버전
        st.markdown("""
<div class='eco-card'>
  <b style='color:var(--accent-primary);'>📚 이론 배경 간단 소개 (계획된 행동이론, TPB)</b>
  <ul style='color:var(--text-muted); font-size:.9rem; margin:.5rem 0 0;'>
<li><b style='color:var(--text-base);'>태도 (Attitude)</b>: 환경 행동을 가치 있게 여길수록 실천 의도가 높아진다</li>
<li><b style='color:var(--text-base);'>주관적 규범 (Subjective Norm)</b>: 주변 사람들의 기대가 행동에 영향을 준다</li>
<li><b style='color:var(--text-base);'>지각된 행동통제감 (PBC)</b>: 실천이 쉽다고 느낄수록 행동으로 이어진다</li>
  </ul>
</div>
""", unsafe_allow_html=True)
    else:
        # 초등 · 중등만 선택 → 용어를 쉽게 풀어쓴 버전
        st.markdown("""
<div class='eco-card'>
  <b style='color:var(--accent-primary);'>🌱 어떤 설문이에요?</b>
  <ul style='color:var(--text-muted); font-size:.9rem; margin:.5rem 0 0;'>
<li><b style='color:var(--text-base);'>내 생각</b>: 환경을 지키는 행동이 얼마나 중요하다고 느끼는지</li>
<li><b style='color:var(--text-base);'>주변 친구들</b>: 가족·친구가 하면 나도 따라 하게 되는지</li>
<li><b style='color:var(--text-base);'>할 수 있다는 마음</b>: 실천이 쉽다고 느끼는지</li>
  </ul>
  <div style='color:var(--text-caption); font-size:.82rem; margin-top:.5rem;'>편하게 솔직히 답해주면 돼요! 정답은 없어요 😊</div>
</div>
""", unsafe_allow_html=True)

    import uuid
    nickname = "익명_" + str(uuid.uuid4())[:6].upper()
    
    scores = []
    all_answered = True

    for i, q in enumerate(QUESTIONS):
        # 고등·성인 레벨에서만 학술 이론 라벨(IA1, TPB 구성요소 등) 노출
        theory_html = f"<div class='q-theory'>📌 {q['theory']}</div>" if show_theory() else ""
        st.markdown(f"""
<div class='q-card'>
  {theory_html}
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
            raw = LIKERT.index(val) + 1
            scores.append(6 - raw if q.get("reverse") else raw)

    col_sub, col_reset = st.columns([2, 1])
    with col_sub:
        if st.button("✅ 설문 제출하기", disabled=(not all_answered)):
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

    st.markdown("---")
    st.markdown(f"**현재 누적 참여자:** {len(st.session_state.survey_responses)}명")

# ── Tab 2: Network viz ──
with tab2:
    # ── 인트로 ──
    st.markdown("""
<div style="font-size:1.3rem; line-height:1.7; background:var(--bg-card); border:1px solid var(--border-main);
     border-radius:16px; padding:1.3rem 1.5rem; margin-bottom:.8rem;">
<b style="color:var(--accent-primary); font-size:1.5rem;">🌱 3일 동안 열심히 환경 교육에 참여한 우리 반!</b><br>
이제 우리 반은 환경을 어떻게 생각하고 있을까요? 설문에 답하면 <b>우리 반 '생각의 지도'</b>가 그려집니다. 함께 알아봐요!
</div>
""", unsafe_allow_html=True)
    # ── 목표 ──
    st.markdown("""
<div style="font-size:1.25rem; line-height:1.7; background:var(--bg-metric); border-radius:14px;
     padding:1rem 1.4rem; margin-bottom:1rem;">
🎯 <b>목표</b> — 우리 반이 환경에 대해 <b>어떻게 생각하는지</b>, 그리고 <b>누구와 생각이 비슷한지</b> 알아보기
</div>
""", unsafe_allow_html=True)

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
        stat_col2.metric("🌿 평균 태도", f"{(avg_scores[0]+avg_scores[1]+avg_scores[2])/3:.2f} / 5")
        stat_col3.metric("💪 평균 행동 의도", f"{avg_scores[9]:.2f} / 5")

       # Dynamic ForceAtlas2 Network graph
        st.markdown("#### 🧬 실시간 ForceAtlas2 네트워크")
        
        with st.spinner("동적 네트워크를 불러오는 중..."):
            draw_dynamic_response_network(responses)

        # ── 네트워크 읽는 법 ──
        st.markdown("""
<div class='eco-card' style="font-size:1.18rem; line-height:1.95;">
<b style="color:var(--accent-primary); font-size:1.4rem;">🕸️ 네트워크(생각의 지도) 읽는 법</b>
<ul style="margin:.6rem 0 0;">
<li><b>점 = 우리 반 친구 한 명</b></li>
<li><b>점끼리 가까우면 = 생각(응답)이 비슷하다</b> ← 가장 중요!</li>
<li><b>색깔 = 5가지 환경 유형</b> (위 버튼으로 골라보세요)</li>
<li><b>뭉쳐 있는 무리 = 생각이 비슷한 친구들의 모임</b></li>
<li><b>가운데 = 우리 반 평균에 가까운 생각 / 바깥 외톨이 = 남과 다른 독특한 생각</b></li>
</ul>
<div style="margin-top:.6rem;">👉 그래서 <b>"누가 누구와 가까운지"</b>, <b>"우리 반에 어떤 생각 그룹이 있는지"</b>를 한눈에 볼 수 있어요.</div>
</div>
""", unsafe_allow_html=True)

        # ── 우리 반 유형 요약 ──
        _pc = Counter(r["profile"] for r in responses if r["profile"] != "나(직접 참여)")
        if _pc:
            top_t = max(_pc, key=_pc.get)
            low_t = min(_pc, key=_pc.get)
            good = top_t != "무관심형"
            tone = "환경에 관심이 많은 <b>훌륭한 반</b>" if good else "<b>조금 더 노력이 필요한 반</b>"
            st.markdown(f"""
<div class='eco-card' style="font-size:1.18rem; line-height:1.85; margin-top:1rem;">
<b style="color:var(--accent-primary); font-size:1.35rem;">🏫 우리 반 요약</b><br>
우리 반은 <b>{top_t}</b>이(가) 가장 많고, <b>{low_t}</b>이(가) 가장 적어요.<br>
그러니까 {tone}이네요! 3일 동안 환경을 배운 만큼, 앞으로도 관심을 갖고 노력하면
훨씬 더 살기 좋은 지구를 가꾸어 나갈 수 있을 거예요 🌍
</div>
""", unsafe_allow_html=True)

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

    # ── 주의사항 ──
    st.markdown("""
<div class='eco-card' style="font-size:1.18rem; line-height:1.85; border:2px solid var(--accent-primary);">
<b style="color:var(--accent-primary); font-size:1.4rem;">🙏 주의사항</b><br>
• <b>솔직하게</b> 답해주세요 — 정답은 없어요!<br>
• 완전 <b>익명</b>이라 누가 어떤 답을 했는지 알 수 없어요.<br>
• 좋아 보이려고 하지 말고 <b>진짜 내 생각</b>을 골라야, 우리 반의 진짜 모습이 보여요.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='eco-footer'>
태도(Attitude) · 주관적 규범(Subjective Norm) · 지각된 행동통제감(PBC) · 행동의도(Intention) — Ajzen, Theory of Planned Behavior (1991)
</div>
""", unsafe_allow_html=True)
