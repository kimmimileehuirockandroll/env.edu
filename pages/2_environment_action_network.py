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
from shared import apply_css, _korean_font

apply_css()

# ─────────────────────────────────────────────
#  GAME 2 전용 데이터 (이 게임만 사용)
# ─────────────────────────────────────────────

# 10문항: 태도(A1-3) · 주관적 규범(SN1-3) · 지각된 행동통제감(PBC1-3) · 행동의도(I1)
QUESTIONS = [
    # 태도 (Attitude)
    {"theory": "A1",
     "text": "분리수거, 텀블러 사용 같은 환경 행동은 가치 있는 일이라고 생각한다.",
     "reverse": False},
    {"theory": "A2",
     "text": "환경을 위해 불편함을 감수하는 것은 의미 있는 일이다.",
     "reverse": False},
    {"theory": "A3",
     "text": "내가 환경 행동을 해도 지구 환경에 별 도움이 안 된다.",
     "reverse": True},
    # 주관적 규범 (Subjective Norm)
    {"theory": "SN1",
     "text": "내 친구들 대부분은 환경을 위한 행동을 중요하게 생각한다.",
     "reverse": False},
    {"theory": "SN2",
     "text": "우리 가족은 나에게 환경을 위한 행동을 실천하길 바란다.",
     "reverse": False},
    {"theory": "N3",
     "text": "선생님이나 어른들이 환경 행동을 강조할 때 나도 해야겠다는 생각이 든다.",
     "reverse": False},
    # 지각된 행동통제감 (PBC)
    {"theory": "PBC1",
     "text": "나는 분리수거, 텀블러 사용 같은 환경 행동을 실천하는 것이 어렵지 않다.",
     "reverse": False},
    {"theory": "PBC2",
     "text": "환경 행동을 하고 싶어도 귀찮거나 불편해서 못 하는 경우가 많다.",
     "reverse": True},
    {"theory": "PBC3",
     "text": "나는 환경을 위한 행동을 꾸준히 실천할 자신이 있다.",
     "reverse": False},
    # 행동 의도 (Intention)
    {"theory": "1",
     "text": "나는 앞으로 환경을 위한 행동을 더 자주 실천할 것이다.",
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
                        facecolor="#0d2418", edgecolor="#1b3a2a",
                        labelcolor="#e8f5e9", fontsize=8, framealpha=0.9)
        if _korean_font:
            for text in leg.get_texts():
                text.set_fontproperties(_korean_font)
                text.set_fontsize(8)

    title_str = f"우리 반 환경행동 네트워크 — 참여자 {G.number_of_nodes()}명 / 연결 {G.number_of_edges()}개"
    if _korean_font:
        ax.set_title(title_str, fontproperties=_korean_font, color="#69f0ae", fontsize=11, pad=12)
    else:
        ax.set_title(title_str, color="#69f0ae", fontsize=11, pad=12)

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
        <div style="
            display:flex;
            gap:10px;
            flex-wrap:wrap;
            align-items:center;
            margin-bottom:10px;
            font-family:sans-serif;
            color:#1b3a2a;
            font-size:13px;
        ">
            <b>색상 필터</b>
            <label><input type="checkbox" class="profile-filter" value="적극 실천형" checked> 적극 실천형</label>
            <label><input type="checkbox" class="profile-filter" value="사회 규범형" checked> 사회 규범형</label>
            <label><input type="checkbox" class="profile-filter" value="자신감형" checked> 자신감형</label>
            <label><input type="checkbox" class="profile-filter" value="가치 인식형" checked> 가치 인식형</label>
            <label><input type="checkbox" class="profile-filter" value="무관심형" checked> 무관심형</label>
            <label><input type="checkbox" class="profile-filter" value="나(직접 참여)" checked> 나</label>
        </div>
    
        <div id="sigma-container" style="
            width:100%;
            height:__HEIGHT__px;
            background:#ffffff;
            border:1px solid #d9e8df;
            border-radius:12px;
            overflow:hidden;
            position:relative;
        "></div>
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
            hidden: false
        });
    });
    
    edges.forEach((edge, i) => {
        if (graph.hasNode(edge.source) && graph.hasNode(edge.target)) {
            graph.addEdgeWithKey("edge-" + i, edge.source, edge.target, {
                size: Math.max(0.5, edge.weight * 2.5),
                color: "#7fdac955",
                hidden: false
            });
        }
    });
    
    const renderer = new Sigma(graph, container, {
        renderEdgeLabels: false,
        defaultEdgeColor: "#7fdac955",
        labelColor: { color: "#1b3a2a" },
        labelSize: 10,
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
    
    function applyProfileFilter() {
        const checkedProfiles = new Set(
            Array.from(document.querySelectorAll(".profile-filter:checked"))
                .map((el) => el.value)
        );
    
        graph.forEachNode((node, attrs) => {
            graph.setNodeAttribute(node, "hidden", !checkedProfiles.has(attrs.profile));
        });
    
        graph.forEachEdge((edge, attrs, source, target) => {
            const sourceHidden = graph.getNodeAttribute(source, "hidden");
            const targetHidden = graph.getNodeAttribute(target, "hidden");
            graph.setEdgeAttribute(edge, "hidden", sourceHidden || targetHidden);
        });
    
        renderer.refresh();
    }
    
    document.querySelectorAll(".profile-filter").forEach((checkbox) => {
        checkbox.addEventListener("change", applyProfileFilter);
    });
    
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
    
    components.html(html, height=height + 80)

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
    st.markdown("### ✏️ 환경행동 설문 (10문항)")
    st.markdown("""
<div class='eco-card'>
  <b style='color:#69f0ae;'>📚 이론 배경 간단 소개</b>
  <ul style='color:#80cbc4; font-size:.9rem; margin:.5rem 0 0;'>
<li><b style='color:#b2dfdb;'>태도 (Attitude)</b>: 환경 행동을 가치 있게 여길수록 실천 의도가 높아진다</li>
<li><b style='color:#b2dfdb;'>주관적 규범 (Subjective Norm)</b>: 주변 사람들의 기대가 행동에 영향을 준다</li>
<li><b style='color:#b2dfdb;'>지각된 행동통제감 (PBC)</b>: 실천이 쉽다고 느낄수록 행동으로 이어진다</li>
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
            raw = LIKERT.index(val) + 1
            scores.append(6 - raw if q.get("reverse") else raw)

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
        stat_col2.metric("🌿 평균 태도", f"{(avg_scores[0]+avg_scores[1]+avg_scores[2])/3:.2f} / 5")
        stat_col3.metric("💪 평균 행동 의도", f"{avg_scores[9]:.2f} / 5")

       # Dynamic ForceAtlas2 Network graph
        st.markdown("#### 🧬 실시간 ForceAtlas2 네트워크")
        
        with st.spinner("동적 네트워크를 불러오는 중..."):
            draw_dynamic_response_network(responses)

        # Profile distribution
        st.markdown("---")
        st.markdown("### 📊 환경 성향 분포")
        profile_counts = Counter(r["profile"] for r in responses)

        bar_data_labels = list(profile_counts.keys())
        bar_data_values = list(profile_counts.values())

        fig2, ax2 = plt.subplots(figsize=(8, 3))
        fig2.patch.set_facecolor("#0a0f0d")
        ax2.set_facecolor("#0a0f0d")
        colors = [PROFILE_COLORS.get(l, "#80cbc4") for l in bar_data_labels]
        bars = ax2.barh(bar_data_labels, bar_data_values, color=colors, height=0.5)
        if _korean_font:
            ax2.set_xlabel("인원 수", color="#80cbc4", fontproperties=_korean_font)
            ax2.set_yticklabels(bar_data_labels, fontproperties=_korean_font,
                                color="#b2dfdb", fontsize=9)
            ax2.tick_params(axis='x', colors="#b2dfdb", labelsize=9)
        else:
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
        q_labels = [f"Q{i+1}" for i in range(len(QUESTIONS))]
        fig3, ax3 = plt.subplots(figsize=(11, 2.5))
        fig3.patch.set_facecolor("#0a0f0d")
        ax3.set_facecolor("#0a0f0d")
        bar_colors = ["#69f0ae","#69f0ae","#69f0ae",
                      "#40c4ff","#40c4ff","#40c4ff",
                      "#ffd740","#ffd740","#ffd740",
                      "#ff6e40"]
        bars3 = ax3.bar(q_labels, avg_scores, color=bar_colors, width=0.5)
        ax3.set_ylim(0, 5.5)
        ax3.spines[:].set_color("#1b3a2a")
        ax3.tick_params(colors="#b2dfdb", labelsize=9)
        for bar, val in zip(bars3, avg_scores):
            ax3.text(bar.get_x() + bar.get_width()/2, val + 0.1,
                     f"{val:.2f}", ha="center", color="#e8f5e9", fontsize=8.5)
        q_short = ["태도\nA1", "태도\nA2", "태도\nA3",
                   "규범\nSN1", "규범\nSN2", "규범\nSN3",
                   "통제\nPBC1", "통제\nPBC2", "통제\nPBC3",
                   "의도\nI1"]
        ax3.set_xticks(range(len(QUESTIONS)))
        ax3.set_xticklabels(q_short, fontsize=7.5, color="#b2dfdb")
        if _korean_font:
            ax3.set_ylabel("평균 점수", color="#80cbc4", fontproperties=_korean_font)
            for tick in ax3.get_xticklabels():
                tick.set_fontproperties(_korean_font)
                tick.set_fontsize(7.5)
                tick.set_color("#b2dfdb")
        else:
            ax3.set_ylabel("평균 점수", color="#80cbc4")
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
태도(Attitude) · 주관적 규범(Subjective Norm) · 지각된 행동통제감(PBC) · 행동의도(Intention) — Ajzen, Theory of Planned Behavior (1991)
</div>
""", unsafe_allow_html=True)
