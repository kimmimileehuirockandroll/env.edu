import math
import json
import random
from collections import Counter
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import pandas as pd
from shared import apply_css, _korean_font, get_chart_colors
apply_css()
# ─────────────────────────────────────────────
#  구글 시트 설정
# ─────────────────────────────────────────────
SHEET_ID  = "19d21nSYeHSTF1AlQkk4bFJAYm6Ld8hbmxRE27Ka6pwI"
GID       = "259232966"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

Q_COLS      = [str(i) for i in range(1, 16)]   # "1" ~ "15"
REVERSE_Q   = {"4", "11"}                       # 역채점 문항

CONSTRUCT_MAP = {
    "인지적 태도 (IA)":   ["1", "2"],
    "감정적 태도 (AA)":   ["3", "4"],
    "명령적 규범 (INJ)":  ["5", "6"],
    "서술적 규범 (DESC)": ["7", "8"],
    "자기효능감 (SE)":    ["9", "10"],
    "통제가능성 (CTR)":   ["11", "12"],
    "행동 의도 (INT)":    ["13", "14", "15"],
}

LIKERT_MAP = {
    "① 매우 그렇지 않다": 1, "매우 그렇지 않다": 1, "1": 1,
    "② 그렇지 않다":      2, "그렇지 않다":      2, "2": 2,
    "③ 약간 그렇지 않다": 3, "약간 그렇지 않다": 3, "3": 3,
    "④ 보통이다":         4, "보통이다":         4, "4": 4,
    "⑤ 약간 그렇다":      5, "약간 그렇다":       5, "5": 5,
    "⑥ 그렇다":           6, "그렇다":           6, "6": 6,
    "⑦ 매우 그렇다":      7, "매우 그렇다":       7, "7": 7,
}

PROFILE_COLORS = {
    "적극 실천형": "#69f0ae",
    "사회 규범형": "#40c4ff",
    "자신감형":    "#ffd740",
    "가치 인식형": "#ff6e40",
    "무관심형":    "#b0bec5",
}

# ─────────────────────────────────────────────
#  데이터 로드 & 전처리
# ─────────────────────────────────────────────
@st.cache_data # (ttl=60)
def load_sheet():
    try:
        df = pd.read_csv(SHEET_URL)
    except Exception as e:
        return None, f"시트 읽기 실패: {e}"

    cols = list(df.columns)
    rename = {cols[0]: "timestamp"}
    for i, col in enumerate(cols[1:16], start=1):
        rename[col] = str(i)
    df = df.rename(columns=rename)

    responses = []
    for _, row in df.iterrows():
        scores = []
        valid = True
        for q in Q_COLS:
            raw = str(row.get(q, "")).strip()
            val = LIKERT_MAP.get(raw)
            if val is None:
                try:
                    val = int(float(raw))
                    if not (1 <= val <= 5):
                        valid = False
                        break
                except Exception:
                    valid = False
                    break
            if q in REVERSE_Q:
                val = 8 - val
            scores.append(val)

        if not valid or len(scores) != 15:
            continue

        profile = _classify_profile(scores)
        responses.append({
            "name":    f"응답자_{len(responses)+1:03d}",
            "scores":  scores,
            "profile": profile,
            "time":    str(row.get("timestamp", "")),
        })

    return responses, None


def _classify_profile(scores):
    avg      = sum(scores) / len(scores)
    attitude = sum(scores[0:4]) / 4
    norm     = sum(scores[4:8]) / 4
    pbc      = sum(scores[8:12]) / 4
    intent   = sum(scores[12:]) / 3

    if avg >= 4.0 and intent >= 4.0:
        return "적극 실천형"
    elif norm >= 4.0:
        return "사회 규범형"
    elif pbc >= 4.0:
        return "자신감형"
    elif attitude >= 3.5 and avg < 3.5:
        return "가치 인식형"
    else:
        return "무관심형"


# ─────────────────────────────────────────────
#  네트워크 함수
# ─────────────────────────────────────────────
def build_response_network(responses, threshold=0.92):
    G = nx.Graph()
    for r in responses:
        G.add_node(r["name"], profile=r["profile"], scores=r["scores"])
    n = len(responses)
    for i in range(n):
        for j in range(i + 1, n):
            a = np.array(responses[i]["scores"], dtype=float)
            b = np.array(responses[j]["scores"], dtype=float)
            sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
            if sim >= threshold:
                G.add_edge(responses[i]["name"], responses[j]["name"], weight=sim)
    return G


def draw_dynamic_network(responses, height=620):
    if not responses:
        return
    G = build_response_network(responses)

    nodes = []
    for node, data in G.nodes(data=True):
        profile = data.get("profile", "")
        nodes.append({
            "id": node, "label": node, "profile": profile,
            "size": 8, "color": PROFILE_COLORS.get(profile, "#80cbc4"),
        })

    edges = []
    for src, tgt, data in G.edges(data=True):
        edges.append({"source": src, "target": tgt,
                      "weight": float(data.get("weight", 1.0))})

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)

    legend_items = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:4px;margin-right:10px;">'
        f'<span style="width:12px;height:12px;border-radius:50%;background:{col};display:inline-block;"></span>'
        f'<span style="font-size:12px;color:var(--text-base);">{prof}</span></span>'
        for prof, col in PROFILE_COLORS.items()
    )

    html = f"""
<div style="background:var(--bg-card);border:1px solid var(--border-main);border-radius:14px;padding:14px;">
  <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:10px;">
    <b style="font-size:13px;color:var(--text-base);">성향 범례</b>
    {legend_items}
  </div>
  <div id="sigma-container" style="width:100%;height:{height}px;background:var(--bg-base);border:1px solid var(--border-main);border-radius:10px;overflow:hidden;position:relative;"></div>
  <div style="font-size:11px;color:var(--text-caption);margin-top:6px;text-align:right;">
    노드 {G.number_of_nodes()}명 &nbsp;|&nbsp; 연결 {G.number_of_edges()}개 &nbsp;|&nbsp; 코사인 유사도 ≥ 0.92
  </div>
</div>
<script type="module">
import Graph from "https://cdn.jsdelivr.net/npm/graphology@0.26.0/+esm";
import {{ Sigma }} from "https://cdn.jsdelivr.net/npm/sigma@2.4.0/+esm";
import forceAtlas2 from "https://cdn.jsdelivr.net/npm/graphology-layout-forceatlas2@0.10.1/+esm";

const nodes = {nodes_json};
const edges = {edges_json};
const container = document.getElementById("sigma-container");
const graph = new Graph();

nodes.forEach(n => {{
    graph.addNode(n.id, {{
        label: n.label, profile: n.profile,
        x: Math.random()*2-1, y: Math.random()*2-1,
        size: n.size, color: n.color, hidden: false
    }});
}});
edges.forEach((e, i) => {{
    if (graph.hasNode(e.source) && graph.hasNode(e.target))
        graph.addEdgeWithKey("e"+i, e.source, e.target,
            {{ size: e.weight, color: "#90caf9" }});
}});

const renderer = new Sigma(graph, container, {{
    labelColor: {{ color: "#1b3a2a" }},
    labelSize: 10, labelWeight: "bold",
}});

const settings = forceAtlas2.inferSettings(graph);
let running = true;
(function animate() {{
    if (running) forceAtlas2.assign(graph, {{
        iterations: 1,
        settings: {{ ...settings, gravity:0.08, scalingRatio:15, slowDown:6 }}
    }});
    renderer.refresh();
    requestAnimationFrame(animate);
}})();

let dragged = null, dragging = false;
renderer.on("downNode", e => {{ dragging=true; dragged=e.node; running=false; }});
renderer.getMouseCaptor().on("mousemovebody", e => {{
    if (!dragging||!dragged) return;
    const p = renderer.viewportToGraph(e);
    graph.setNodeAttribute(dragged,"x",p.x);
    graph.setNodeAttribute(dragged,"y",p.y);
    e.preventSigmaDefault(); e.original.preventDefault(); e.original.stopPropagation();
}});
renderer.getMouseCaptor().on("mouseup", () => {{ dragging=false; dragged=null; }});
</script>
"""
    components.html(html, height=height + 120)
    
def draw_construct_bar(responses):
    ch = get_chart_colors()
    all_s = np.array([r["scores"] for r in responses])
    labels, values, colors_list = [], [], []
    bar_colors = [ch["accent"], ch["accent"],
                  ch["accent2"], ch["accent2"],
                  "#ffd740", "#ffd740",
                  "#ff6e40"]
    for idx, (name, q_list) in enumerate(CONSTRUCT_MAP.items()):
        idxs = [int(q)-1 for q in q_list]
        labels.append(name)
        values.append(float(all_s[:, idxs].mean()))
        colors_list.append(bar_colors[idx % len(bar_colors)])

    fig, ax = plt.subplots(figsize=(9, 3.2))
    fig.patch.set_facecolor(ch["bg"])
    ax.set_facecolor(ch["bg"])
    bars = ax.barh(labels, values, color=colors_list, height=0.55)
    ax.set_xlim(0, 7.5)
    ax.spines[:].set_color(ch["spine"])
    ax.set_yticks(range(len(labels))) 
    ax.tick_params(colors=ch["tick"], labelsize=8.5)
    for bar, val in zip(bars, values):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                f"{val:.2f}", va="center", color=ch["accent"], fontsize=9)
    if _korean_font:
        ax.set_xlabel("평균 점수 (1~7)", color=ch["axis"], fontproperties=_korean_font)
        ax.set_yticklabels(labels, fontproperties=_korean_font,
                           color=ch["tick"], fontsize=8.5)
    else:
        ax.set_xlabel("평균 점수 (1~7)", color=ch["axis"])
    plt.tight_layout(pad=0.5)
    return fig

def draw_profile_bar(responses):
    ch = get_chart_colors()
    counts = Counter(r["profile"] for r in responses)
    labels = list(counts.keys())
    values = list(counts.values())
    colors = [PROFILE_COLORS.get(l, ch["muted"]) for l in labels]

    fig, ax = plt.subplots(figsize=(7, 2.5))
    fig.patch.set_facecolor(ch["bg"])
    ax.set_facecolor(ch["bg"])
    bars = ax.barh(labels, values, color=colors, height=0.5)
    ax.spines[:].set_color(ch["spine"])
    ax.set_yticks(range(len(labels))) 
    ax.tick_params(colors=ch["tick"], labelsize=8.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
                str(val), va="center", color=ch["accent"], fontsize=9)
    if _korean_font:
        ax.set_xlabel("인원 수", color=ch["axis"], fontproperties=_korean_font)
        ax.set_yticklabels(labels, fontproperties=_korean_font,
                           color=ch["tick"], fontsize=8.5)
    else:
        ax.set_xlabel("인원 수", color=ch["axis"])
    plt.tight_layout(pad=0.5)
    return fig

# ─────────────────────────────────────────────
#  화면 구성
# ─────────────────────────────────────────────
st.markdown("## 📊 1반 환경행동 네트워크")
st.markdown("구글 시트에 수집된 TPB 설문 응답을 실시간으로 불러와 네트워크로 시각화합니다.")

with st.spinner("📡 구글 시트에서 데이터를 불러오는 중..."):
    responses, err = load_sheet()

if err:
    st.error(f"❌ {err}")
    st.stop()

if not responses:
    st.warning("아직 유효한 응답이 없습니다. 구글 폼에 응답이 제출되면 자동으로 표시됩니다.")
    st.stop()

# 상단 지표
all_scores_np = np.array([r["scores"] for r in responses])
avg_all       = all_scores_np.mean(axis=0)

c1, c2, c3 = st.columns(3)
c1.metric("👥 총 응답자", f"{len(responses)}명")
c2.metric("🌿 평균 태도", f"{avg_all[0:4].mean():.2f} / 7")
c3.metric("💪 평균 행동 의도", f"{avg_all[12:].mean():.2f} / 7")

st.caption("⏱️ 데이터는 60초마다 자동 갱신됩니다.")
if st.button("🔄 지금 갱신"):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")
tab1, tab2 = st.tabs(["🕸️ 네트워크", "📊 구인별 분석"])
# tab1, tab2, tab3 = st.tabs(["🕸️ 네트워크", "📊 구인별 분석", "📋 원시 데이터"])

with tab1:
    st.markdown("### 🕸️ 환경행동 유사도 네트워크")
    st.caption("응답 벡터 간 코사인 유사도 ≥ 0.92인 학생끼리 연결됩니다. 노드를 드래그해 이동할 수 있습니다.")
    draw_dynamic_network(responses)

with tab2:
    st.markdown("### 📊 TPB 구인별 평균 점수")
    fig_c = draw_construct_bar(responses)
    st.pyplot(fig_c, use_container_width=True)
    plt.close(fig_c)

    st.markdown("### 👤 환경 성향 분포")
    fig_p = draw_profile_bar(responses)
    st.pyplot(fig_p, use_container_width=True)
    plt.close(fig_p)

# with tab3:
#     st.markdown("### 📋 원시 데이터")
#     rows = []
#     for r in responses:
#         row = {"성향": r["profile"], "시간": r["time"]}
#         for i, s in enumerate(r["scores"], start=1):
#             row[f"Q{i}"] = s
#         rows.append(row)
#     df_view = pd.DataFrame(rows)
#     st.dataframe(df_view, use_container_width=True)
#     st.caption(f"총 {len(df_view)}행")

st.markdown("""
<div class='eco-footer'>
태도(Attitude) · 주관적 규범(Subjective Norm) · 지각된 행동통제감(PBC) · 행동의도(Intention)
— Ajzen, Theory of Planned Behavior (1991)
</div>
""", unsafe_allow_html=True)
