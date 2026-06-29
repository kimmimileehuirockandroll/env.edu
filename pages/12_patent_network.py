import json
import re
from collections import Counter
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from shared import apply_css, get_chart_colors

apply_css()

EXAMPLE_ID  = "1avskack5dD-45gqcVknChlgX1fMuioam8qjlc1Bwv8A"
EXAMPLE_GID = "1001181212"
REQUIRED = ["Publication Year", "Applicants"]


def _csv_url(sheet_id, gid):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"


def _cpc_subs(cell):
    if not isinstance(cell, str) or not cell.strip():
        return []
    out = []
    for code in cell.split(";;"):
        m = re.match(r"[A-Z]\d{2}[A-Z]", code.strip())
        if m:
            out.append(m.group(0))
    return sorted(set(out))


@st.cache_data(ttl=600)
def load_processed(sheet_id, gid):
    df = pd.read_csv(_csv_url(sheet_id, gid), low_memory=False)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("필수 컬럼 누락: " + ", ".join(missing))
    out = pd.DataFrame()
    out["year"] = pd.to_numeric(df["Publication Year"], errors="coerce")
    out["applicant"] = df["Applicants"].fillna("").astype(str).str.split(";;").str[0].str.strip()
    out["jurisdiction"] = df["Jurisdiction"].astype(str) if "Jurisdiction" in df.columns else ""
    out["cited"] = pd.to_numeric(df.get("Cited by Patent Count", 0), errors="coerce").fillna(0).astype(int)
    out["title"] = df["Title"].astype(str) if "Title" in df.columns else ""
    out["url"] = df["URL"].astype(str) if "URL" in df.columns else ""
    out["_cpc"] = df["CPC Classifications"].apply(_cpc_subs) if "CPC Classifications" in df.columns else [[] for _ in range(len(df))]
    out = out.dropna(subset=["year"])
    out = out[out["applicant"] != ""]
    return out.reset_index(drop=True)


def parse_sheet_url(url):
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not m:
        return None, None
    g = re.search(r"[#&?]gid=([0-9]+)", url)
    return m.group(1), (g.group(1) if g else "0")


@st.cache_data(ttl=600)
def yearly_trend(df, ymax=2024):
    s = df[df["year"] <= ymax].groupby("year").size().sort_index()
    return s


@st.cache_data(ttl=600)
def top_players(df, role, n=12):
    col = "applicant" if role == "출원인" else "jurisdiction"
    return df[col].value_counts().head(n)


@st.cache_data(ttl=600)
def cpc_network(df, top_edges=70, top_nodes=45):
    freq = Counter()
    pair = Counter()
    for subs in df["_cpc"]:
        for s in subs:
            freq[s] += 1
        for a, b in combinations(subs, 2):
            pair[(a, b)] += 1
    top_set = {n for n, _ in freq.most_common(top_nodes)}
    edges = [(a, b, w) for (a, b), w in pair.items() if a in top_set and b in top_set]
    edges.sort(key=lambda x: -x[2])
    return freq, edges[:top_edges], top_set


@st.cache_data(ttl=600)
def core_patents(df, n=10):
    cols = [c for c in ["title", "applicant", "year", "cited", "jurisdiction"] if c in df.columns]
    return df.sort_values("cited", ascending=False).head(n)[cols]


def get_active_df():
    src = st.session_state.get("pat_src", ("example",))
    try:
        if src[0] == "example":
            return load_processed(EXAMPLE_ID, EXAMPLE_GID), "예시 데이터 (친환경 특허, lens.org)", None
        return load_processed(src[1], src[2]), "내 구글 스프레드시트", None
    except Exception as ex:
        return load_processed(EXAMPLE_ID, EXAMPLE_GID), "예시 데이터 (대체)", str(ex)


C = get_chart_colors()
STEPS = ["0 · 왜 특허인가", "1 🎓 데이터 구하기", "2 🛠 데이터 열기",
         "3 🛠 출원 추세", "4 🛠 주요 플레이어", "5 🛠 기술 네트워크", "6 🛠 인사이트"]

st.markdown("## 📜 데이터로 읽는 특허")
st.markdown("특허 데이터를 **어떻게 구하는지 배우고(STEP 1)**, **내 데이터(또는 예시)**로 직접 기술 지형을 분석하는 6단계 워크숍입니다.")

if "pat_step" not in st.session_state:
    st.session_state.pat_step = STEPS[0]
st.radio("진행 단계", STEPS, key="pat_step", horizontal=True, label_visibility="collapsed")
step = STEPS.index(st.session_state.pat_step)
st.markdown("---")

df, src_label, src_err = get_active_df()

# ── STEP 0 ──
if step == 0:
    st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>📜 특허 = 기술 결정의 기록</div>
  <div class='hero-sub'>
  특허는 "누가 · 언제 · 어떤 기술을 선점했는가"가 쌓인 데이터입니다.<br>
  <b>데이터와 네트워크</b>로 기술의 흐름과 핵심을 읽어봅니다.
  </div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='eco-card'><b style='color:var(--accent-primary)'>📈 S-커브</b>"
                "<p style='color:var(--text-muted);font-size:.92rem'>기술은 도입→성장→성숙을 거칩니다. 출원 추세로 지금 어느 국면인지 읽어요.</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='eco-card'><b style='color:var(--accent-primary)'>🕸️ 네트워크</b>"
                "<p style='color:var(--text-muted);font-size:.92rem'>점(기술분류)과 선(함께 등장)으로 그린 지도. <b>모이는 점=핵심 기술</b>.</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='eco-card'><b style='color:var(--accent-primary)'>🎯 결과물</b>"
                "<p style='color:var(--text-muted);font-size:.92rem'>출원 추세 · 주요 출원인 · 기술 융합 네트워크 · 핵심특허 · 한 장 리포트.</p></div>", unsafe_allow_html=True)
    st.info("💡 STEP 1에서 데이터 구하는 법을 배우고, STEP 2에서 **내 시트를 연동**해 나만의 분석을 만듭니다.")

# ── STEP 1 ──
elif step == 1:
    st.markdown("### 🎓 데이터, 어디서 어떻게 구하나 — lens.org")
    st.markdown("이 워크숍의 데이터는 **lens.org**(무료 특허·학술 검색)에서 받았습니다. "
                "원하는 기술·기간을 골라 **CSV로 내려받는 법**을 익혀요. (직접 받지 않고 방법만 체득)")

    st.markdown("#### 1) 데이터 소스")
    src = pd.DataFrame({
        "출처": ["lens.org", "Google Patents", "KIPRIS(특허정보넷)", "USPTO PatentsView"],
        "특징": ["무료·CSV 다운로드 강력", "검색 편리", "한국어·국내 특허", "미국 특허 API"],
        "난이도": ["보통", "쉬움", "보통", "다소 높음"],
        "무료 CSV": ["O", "△", "O", "O(API)"],
    })
    st.dataframe(src, hide_index=True, use_container_width=True)
    st.caption("이번 데이터의 출처는 **lens.org** 입니다.")

    st.markdown("#### 2) 친환경 기술만 좁히기 — CPC 코드")
    st.markdown("특허 기술은 **CPC 코드**로 분류돼요. 기후·친환경 기술은 **`Y02`**(예: `Y02E` 에너지, `Y02W` 폐기물). "
                "검색에 CPC를 넣으면 *친환경 특허만* 골라낼 수 있어요.")

    st.markdown("#### 3) 검색식(쿼리) 만들기 — 직접 해보기")
    cc1, cc2 = st.columns(2)
    kw = cc1.text_input("키워드", value="recycling")
    cpc = cc2.text_input("CPC 코드", value="Y02")
    cc3, cc4 = st.columns(2)
    y0 = cc3.number_input("시작연도", value=2015, step=1)
    y1 = cc4.number_input("끝연도", value=2024, step=1)
    query = (f'("{kw}") AND cpc_class:{cpc}* '
             f"AND publication_date:[{int(y0)} TO {int(y1)}]")
    st.code(query, language="text")
    st.caption("👆 lens.org 검색창에 이런 식으로 넣고, 결과를 CSV로 내보냅니다. (실제 다운로드는 강사가 시연)")
    st.success("정리: ① lens.org 접속 → ② CPC(Y02)로 친환경 좁히기 → ③ 키워드·기간 지정 → ④ CSV 다운로드 → ⑤ 구글시트에 업로드")

# ── STEP 2 ──
elif step == 2:
    st.markdown("### 🛠 데이터 열어보기 — 내 시트 연동하기")
    st.markdown("**lens.org에서 받은 CSV**를 구글 스프레드시트에 올린 뒤 링크를 붙여넣으면 그 데이터로 분석합니다. "
                "처음엔 예시 데이터로 연결돼 있어요.")
    st.markdown(f"**현재 연결:** `{src_label}`")
    if src_err:
        st.warning(f"내 시트 연동 실패 → 예시로 대체했습니다: {src_err}")

    colA, colB = st.columns([3, 1])
    url = colA.text_input("내 구글 스프레드시트 링크 (공유: '링크가 있는 모든 사용자 보기')",
                          placeholder="https://docs.google.com/spreadsheets/d/.../edit#gid=0")
    colB.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    if colB.button("🔗 내 시트 연동", use_container_width=True):
        sid, gid = parse_sheet_url(url)
        if not sid:
            st.error("링크에서 시트 ID를 찾지 못했어요. 전체 URL을 붙여넣어 주세요.")
        else:
            try:
                load_processed(sid, gid)
                st.session_state.pat_src = ("user", sid, gid)
                st.rerun()
            except Exception as ex:
                st.error(f"연동 실패: {ex}")
    if st.button("📋 예시 데이터 사용"):
        st.session_state.pat_src = ("example",)
        st.rerun()
    st.caption(f"필수 컬럼: {', '.join(REQUIRED)} (lens.org 내보내기 형식). CPC·피인용수 컬럼이 있으면 네트워크·핵심특허도 분석돼요.")

    st.markdown("---")
    yrs = df["year"].astype(int)
    m1, m2, m3 = st.columns(3)
    m1.metric("총 특허 건수", f"{len(df):,}")
    m2.metric("기간", f"{yrs.min()}–{yrs.max()}")
    m3.metric("출원인 수", f"{df['applicant'].nunique():,}")
    show_cols = [c for c in ["year", "applicant", "jurisdiction", "cited", "title"] if c in df.columns]
    st.dataframe(df[show_cols].head(200), use_container_width=True, height=320)

# ── STEP 3 ──
elif step == 3:
    st.markdown("### 🛠 출원 추세 — S-커브 읽기")
    st.caption(f"데이터: {src_label} · 2024년까지 (최신연도는 집계 미완)")
    s = yearly_trend(df)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    fig.patch.set_facecolor(C["bg"]); ax.set_facecolor(C["bg"])
    ax.plot(s.index.astype(int), s.values, marker="o", color=C["accent"], linewidth=2.5)
    ax.fill_between(s.index.astype(int), s.values, color=C["accent"], alpha=0.15)
    for sp in ax.spines.values():
        sp.set_color(C["spine"])
    ax.tick_params(colors=C["tick"])
    ax.set_xlabel("Publication Year", color=C["text"]); ax.set_ylabel("Patents", color=C["text"])
    ax.grid(True, color=C["spine"], alpha=0.4)
    st.pyplot(fig)
    st.markdown(
        f"<div class='eco-card'><b style='color:var(--accent-primary)'>🔎 해석해보기</b>"
        f"<p style='color:var(--text-muted)'>출원 정점: <b>{int(s.idxmax())}년</b>. "
        f"기울기가 가파르면 <b>성장기</b>, 평평/하락이면 <b>성숙기</b>예요. 지금은 어느 국면일까요?</p></div>",
        unsafe_allow_html=True,
    )

# ── STEP 4 ──
elif step == 4:
    st.markdown("### 🛠 누가 선점했나 — 주요 플레이어")
    role = st.radio("기준", ["출원인", "관할국"], horizontal=True)
    s = top_players(df, role)
    mx = float(s.max()) or 1.0
    rows = ""
    for name, val in s.items():
        pct = val / mx * 100
        disp = (name[:26] + "…") if isinstance(name, str) and len(name) > 27 else name
        rows += ("<div class='barrow'>"
                 f"<div class='barname' title='{name}'>{disp}</div>"
                 f"<div class='bartrack'><div class='barfill' style='--w:{pct:.1f}%'></div></div>"
                 f"<div class='barval'>{int(val)}</div></div>")
    bar_html = """
<div id="bars"><style>
  #bars { font-family:'Noto Sans KR',sans-serif; }
  #bars .barrow { display:flex; align-items:center; gap:10px; margin:7px 0; }
  #bars .barname { width:200px; font-size:13px; color:__TEXT__; text-align:right; flex:none; overflow:hidden; white-space:nowrap; }
  #bars .bartrack { flex:1; background:__GRID__; border-radius:8px; height:22px; overflow:hidden; }
  #bars .barfill { height:100%; width:0; border-radius:8px; background:linear-gradient(90deg,__ACC__,__ACC2__); animation:grow 1.1s cubic-bezier(.2,.7,.2,1) forwards; }
  #bars .barval { width:52px; font-size:12px; color:__MUT__; flex:none; }
  @keyframes grow { from { width:0; } to { width:var(--w); } }
</style>__ROWS__</div>
"""
    bar_html = (bar_html.replace("__ROWS__", rows).replace("__TEXT__", C["text"])
                .replace("__GRID__", C["spine"]).replace("__ACC__", C["accent"])
                .replace("__ACC2__", C["accent2"]).replace("__MUT__", C["muted"]))
    components.html(bar_html, height=len(s) * 40 + 40)
    st.markdown(
        f"<div class='eco-card'><b style='color:var(--accent-primary)'>💬 토론</b>"
        f"<p style='color:var(--text-muted)'>{role} 1위는 <b>{s.index[0]}</b>. "
        f"이 주체의 전략은 무엇일까요? (집중 분야 / 시장 / 협력)</p></div>", unsafe_allow_html=True)

# ── STEP 5 ──
elif step == 5:
    st.markdown("### 🛠 기술 네트워크 — 어떤 기술이 핵심인가 ★")
    st.caption("노드=CPC 기술분류(소분류), 선=같은 특허에 함께 등장(기술 융합). 크기=빈도.")
    n_edges = st.slider("표시할 연결(엣지) 수", 30, 120, 70, step=10)
    freq, edges, top_set = cpc_network(df, n_edges)
    if not edges:
        st.warning("CPC 분류 데이터가 없어 네트워크를 그릴 수 없어요. (CPC Classifications 컬럼 필요)")
    else:
        mx = max(freq[n] for n in top_set) or 1
        hub = max(top_set, key=lambda n: freq[n])
        used = set()
        for a, b, w in edges:
            used.add(a); used.add(b)
        nodes = [{"id": n, "label": n, "size": 4 + 18 * (freq[n] / mx),
                  "color": C["accent"] if n == hub else C["accent2"]} for n in used]
        ej = [{"source": a, "target": b} for a, b, w in edges]
        NET = """
<div id="net-root" style="font-family:'Noto Sans KR',sans-serif;">
  <div style="display:flex; gap:8px; margin-bottom:8px;">
    <button id="net-toggle" style="font-family:inherit; padding:8px 16px; border:2px solid #1A1A1A; border-radius:8px; background:#FF2D6B; color:#fff; font-weight:700; cursor:pointer; box-shadow:2px 2px 0 #1A1A1A;">⏸ 일시정지</button>
    <span style="font-size:12px; color:#888; align-self:center;">노드를 끌어 옮길 수 있어요</span>
  </div>
  <div id="net" style="width:100%; height:520px; background:__BG__; border:2px solid __GRID__; border-radius:12px; overflow:hidden;"></div>
</div>
<script type="module">
  import Graph from "https://cdn.jsdelivr.net/npm/graphology@0.26.0/+esm";
  import { Sigma } from "https://cdn.jsdelivr.net/npm/sigma@2.4.0/+esm";
  import forceAtlas2 from "https://cdn.jsdelivr.net/npm/graphology-layout-forceatlas2@0.10.1/+esm";
  const nodes = __NODES__, edges = __EDGES__;
  const g = new Graph();
  nodes.forEach(n => g.addNode(n.id, { label:n.label, x:Math.random()*2-1, y:Math.random()*2-1, size:n.size, color:n.color }));
  edges.forEach((e,i) => { if(g.hasNode(e.source)&&g.hasNode(e.target)&&!g.hasEdge(e.source,e.target)) g.addEdgeWithKey("e"+i, e.source, e.target, { size:1, color:"__GRID__" }); });
  const renderer = new Sigma(g, document.getElementById("net"), { labelColor:{color:"__TEXT__"}, labelSize:11, labelWeight:"bold" });
  const settings = forceAtlas2.inferSettings(g);
  let running = true;
  function animate(){ if(running){ forceAtlas2.assign(g,{iterations:1, settings:{...settings, gravity:0.1, scalingRatio:18, slowDown:6}}); } renderer.refresh(); requestAnimationFrame(animate); }
  animate();
  const btn = document.getElementById("net-toggle");
  btn.onclick = function(){ running=!running; btn.textContent = running ? "⏸ 일시정지" : "▶ 재생"; btn.style.background = running ? "#FF2D6B" : "#2e8b57"; };
  let dragged=null, dragging=false;
  renderer.on("downNode", e=>{ dragging=true; dragged=e.node; });
  renderer.getMouseCaptor().on("mousemovebody", e=>{ if(!dragging||!dragged) return; const p=renderer.viewportToGraph(e); g.setNodeAttribute(dragged,"x",p.x); g.setNodeAttribute(dragged,"y",p.y); e.preventSigmaDefault(); e.original.preventDefault(); e.original.stopPropagation(); });
  renderer.getMouseCaptor().on("mouseup", ()=>{ dragging=false; dragged=null; });
</script>
"""
        NET = (NET.replace("__NODES__", json.dumps(nodes, ensure_ascii=False))
               .replace("__EDGES__", json.dumps(ej, ensure_ascii=False))
               .replace("__BG__", C["bg"]).replace("__GRID__", C["spine"]).replace("__TEXT__", C["text"]))
        components.html(NET, height=600)
        st.markdown(
            f"<div class='eco-card'><b style='color:var(--accent-primary)'>🕸️ 핵심 기술 = {hub}</b>"
            f"<p style='color:var(--text-muted)'>가장 많이 등장·연결되는 기술분류입니다. ⏸로 멈춰 군집(기술 묶음)을 살펴보세요. "
            f"(예: <b>Y02</b>로 시작하면 친환경 기술)</p></div>", unsafe_allow_html=True)

    cp = core_patents(df)
    if cp["cited"].max() > 0:
        st.markdown("#### 🌟 핵심 특허 (피인용 Top 10)")
        st.dataframe(cp, hide_index=True, use_container_width=True)

# ── STEP 6 ──
elif step == 6:
    st.markdown("### 🛠 인사이트 정리 — 한 장 리포트 만들기")
    st.caption(f"데이터: {src_label}")
    s = yearly_trend(df)
    apps = top_players(df, "출원인", 3)
    freq, edges, top_set = cpc_network(df, 50)
    top_cpc = ", ".join([n for n, _ in Counter(freq).most_common(5)]) if freq else "-"
    cp = core_patents(df, 1)
    core_title = cp["title"].iloc[0] if len(cp) and "title" in cp else "-"
    auto = (f"- 데이터 출처: {src_label}\n"
            f"- 분석 기간: {int(df['year'].min())}–{int(df['year'].max())}\n"
            f"- 총 특허: {len(df):,}건\n"
            f"- 주요 출원인: {', '.join(apps.index[:3])}\n"
            f"- 핵심 기술분류(CPC): {top_cpc}\n"
            f"- 출원 정점: {int(s.idxmax())}년\n"
            f"- 최다 피인용 특허: {core_title[:60]}")
    st.markdown("**자동 요약 (데이터에서 추출)**")
    st.code(auto, language="text")
    a = st.text_area("📈 기술 수명주기(S-커브) 상 지금은?", height=80)
    b = st.text_area("🏢 주목할 출원인/기술 융합은?", height=80)
    cc = st.text_area("⚠️ 우리 조직의 기회·위협은?", height=80)
    if st.button("📄 리포트 생성"):
        report = ("■ 특허 데이터 분석 리포트\n==============================\n\n"
                  "[데이터 요약]\n" + auto + "\n\n[기술 수명주기]\n" + (a or "-") +
                  "\n\n[주목 출원인/기술]\n" + (b or "-") + "\n\n[기회/위협]\n" + (cc or "-") + "\n")
        st.download_button("⬇️ 리포트 다운로드 (.txt)", report,
                           file_name="patent_report.txt", mime="text/plain")
        st.success("데이터로 시작해 결론까지 — 각자 다른 특허셋이면 각자 다른 리포트가 나옵니다!")
