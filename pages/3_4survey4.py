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
SHEET_ID  = "1M_dHUGwn3IO23DqKRtafr5HV3qTGBuUqRDbJJSfj8A0"
GID       = "336530920"
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
@st.cache_data(ttl=60)
def load_sheet():
    try:
        df = pd.read_csv(SHEET_URL)
    except Exception as e:
        return None, f"시트 읽기 실패: {e}"

    cols = list(df.columns)
    # 마지막 '별명 또는 이름' 열 자동 탐지 (헤더에 별명/이름 포함)
    name_col = next((c for c in cols if ("별명" in str(c)) or ("이름" in str(c))), None)
    rename = {cols[0]: "timestamp"}
    for i, col in enumerate(cols[1:16], start=1):
        rename[col] = str(i)
    df = df.rename(columns=rename)

    responses = []
    used_names = set()
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

        # 별명/이름 → 노드 라벨 (빈 값은 익명N, 중복은 _2, _3 …)
        raw_name = str(row.get(name_col, "")).strip() if name_col else ""
        if not raw_name or raw_name.lower() == "nan":
            raw_name = f"익명{len(responses) + 1}"
        disp = raw_name
        _k = 2
        while disp in used_names:
            disp = f"{raw_name}_{_k}"
            _k += 1
        used_names.add(disp)

        responses.append({
            "name":    disp,
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

    html = """
<div style="background:var(--bg-card);border:1px solid var(--border-main);border-radius:14px;padding:14px;">
  <div style="font-size:18px;font-weight:800;color:var(--text-base);margin-bottom:10px;font-family:'Noto Sans KR',sans-serif;">
    🎨 유형 버튼을 눌러보세요 — 고른 유형만 선명하게, 나머지는 흐려집니다
  </div>
  <div id="chips" style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;"></div>
  <div id="sigma-container" style="width:100%;height:__HEIGHT__px;background:var(--bg-base);border:1px solid var(--border-main);border-radius:10px;overflow:hidden;position:relative;"></div>
  <div id="fx-explain" style="margin-top:14px;padding:14px 16px;border-radius:12px;background:#f3f7f4;color:#1b3a2a;font-size:18px;line-height:1.6;font-family:'Noto Sans KR',sans-serif;">👆 위 유형 버튼을 누르면, 그 유형 설명이 여기에 나타나요.</div>
</div>
<script type="module">
import Graph from "https://cdn.jsdelivr.net/npm/graphology@0.26.0/+esm";
import { Sigma } from "https://cdn.jsdelivr.net/npm/sigma@2.4.0/+esm";
import forceAtlas2 from "https://cdn.jsdelivr.net/npm/graphology-layout-forceatlas2@0.10.1/+esm";

const nodes = __NODES__;
const edges = __EDGES__;
const container = document.getElementById("sigma-container");
const graph = new Graph();
nodes.forEach(n => {
    graph.addNode(n.id, {
        label: n.label, profile: n.profile,
        x: Math.random()*2-1, y: Math.random()*2-1,
        size: n.size, color: n.color, origColor: n.color, origSize: n.size, hidden: false
    });
});
edges.forEach((e, i) => {
    if (graph.hasNode(e.source) && graph.hasNode(e.target))
        graph.addEdgeWithKey("e"+i, e.source, e.target, { size: e.weight, color: "#90caf9" });
});
const renderer = new Sigma(graph, container, { labelColor:{color:"#1b3a2a"}, labelSize:15, labelWeight:"bold" });
const settings = forceAtlas2.inferSettings(graph);
let running = true;
(function animate(){
    if (running) forceAtlas2.assign(graph, { iterations:1, settings:{...settings, gravity:0.08, scalingRatio:15, slowDown:6} });
    renderer.refresh();
    requestAnimationFrame(animate);
})();

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
const present = new Set(nodes.map(n => n.profile));
const chipBox = document.getElementById("chips");
const explainBox = document.getElementById("fx-explain");
const chipEls = {};
let active = null;
ORDER.filter(p => present.has(p)).forEach(p => {
    const b = document.createElement("button");
    b.textContent = (EXPLAIN[p] ? EXPLAIN[p].e : "") + " " + p;
    b.style.cssText = "font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:800;padding:9px 16px;border-radius:999px;border:3px solid " + (COLORS[p]||"#ccc") + ";background:" + (COLORS[p]||"#eee") + ";color:#123;cursor:pointer;";
    b.onclick = () => select(active === p ? null : p);
    chipBox.appendChild(b); chipEls[p] = b;
});
function select(p){
    active = p;
    ORDER.forEach(q => { if(!chipEls[q]) return; chipEls[q].style.opacity=(!p||q===p)?"1":"0.45"; chipEls[q].style.boxShadow=(q===p)?"0 0 0 4px rgba(27,58,42,.35)":"none"; });
    graph.forEachNode((n,a) => { const on = !p || a.profile===p; graph.setNodeAttribute(n,"color", on?a.origColor:"#e6e6e6"); graph.setNodeAttribute(n,"size", on?a.origSize:a.origSize*0.55); });
    graph.forEachEdge((e,a,s,t) => { const on = !p || graph.getNodeAttribute(s,"profile")===p || graph.getNodeAttribute(t,"profile")===p; graph.setEdgeAttribute(e,"color", on?"#90caf9":"#eeeeee"); });
    if(!p){ explainBox.innerHTML="👆 위 유형 버튼을 누르면, 그 유형 설명이 여기에 나타나요."; explainBox.style.background="#f3f7f4"; }
    else { const ex=EXPLAIN[p]||{e:"",d:""}; explainBox.innerHTML="<span style='font-size:24px;'>"+ex.e+"</span> <b style='font-size:20px;'>"+p+"</b><br>"+ex.d; explainBox.style.background=(COLORS[p]||"#f3f7f4")+"33"; }
    renderer.refresh();
}

let dragged = null, dragging = false;
renderer.on("downNode", e => { dragging=true; dragged=e.node; running=false; });
renderer.getMouseCaptor().on("mousemovebody", e => {
    if (!dragging||!dragged) return;
    const p = renderer.viewportToGraph(e);
    graph.setNodeAttribute(dragged,"x",p.x);
    graph.setNodeAttribute(dragged,"y",p.y);
    e.preventSigmaDefault(); e.original.preventDefault(); e.original.stopPropagation();
});
renderer.getMouseCaptor().on("mouseup", () => { dragging=false; dragged=null; });
</script>
"""
    html = (html.replace("__HEIGHT__", str(height))
                .replace("__NODES__", nodes_json)
                .replace("__EDGES__", edges_json))
    components.html(html, height=height + 250)
    
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
st.markdown("## 📊 4반 환경행동 네트워크")
st.markdown("구글 시트에 수집된 TPB 설문 응답을 실시간으로 불러와 네트워크로 시각화합니다.")

with st.spinner("📡 구글 시트에서 데이터를 불러오는 중..."):
    responses, err = load_sheet()

if err:
    st.error(f"❌ {err}")
    st.stop()

if not responses:
    st.warning("아직 유효한 응답이 없습니다. 구글 폼에 응답이 제출되면 자동으로 표시됩니다.")
    st.stop()

# ── 인트로 ──
st.markdown("""
<div style="font-size:1.3rem; line-height:1.7; background:var(--bg-card); border:1px solid var(--border-main);
     border-radius:16px; padding:1.3rem 1.5rem; margin-bottom:.8rem;">
<b style="color:var(--accent-primary); font-size:1.5rem;">🌱 3일 동안 열심히 환경 교육에 참여한 우리 반!</b><br>
이제 우리 반은 환경을 어떻게 생각하고 있을까요? 설문 결과로 <b>우리 반 '생각의 지도'</b>가 그려집니다. 함께 알아봐요!
</div>
""", unsafe_allow_html=True)
# ── 목표 ──
st.markdown("""
<div style="font-size:1.25rem; line-height:1.7; background:var(--bg-metric); border-radius:14px;
     padding:1rem 1.4rem; margin-bottom:1rem;">
🎯 <b>목표</b> — 우리 반이 환경에 대해 <b>어떻게 생각하는지</b>, 그리고 <b>누구와 생각이 비슷한지</b> 알아보기
</div>
""", unsafe_allow_html=True)

# 상단 지표 + 갱신
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
# ── 네트워크 ──
draw_dynamic_network(responses)

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

# ── 우리 반 요약 (진짜 결과 반영) ──
from collections import Counter as _Counter
_pc = _Counter(r["profile"] for r in responses if r["profile"] != "나(직접 참여)")
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

# ── 주의사항 ──
st.markdown("""
<div class='eco-card' style="font-size:1.18rem; line-height:1.85; border:2px solid var(--accent-primary);">
<b style="color:var(--accent-primary); font-size:1.4rem;">🙏 주의사항</b><br>
• <b>솔직하게</b> 답해주세요 — 정답은 없어요!<br>
• 완전 <b>익명</b>이라 누가 어떤 답을 했는지 알 수 없어요.<br>
• 좋아 보이려고 하지 말고 <b>진짜 내 생각</b>을 골라야, 우리 반의 진짜 모습이 보여요.
</div>
""", unsafe_allow_html=True)

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
