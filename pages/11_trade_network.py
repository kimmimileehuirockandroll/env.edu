import json
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from shared import apply_css, get_chart_colors

apply_css()

EXAMPLE_ID  = "1x5QIn_o1eu_g_xGkCGnL85FdjYcMl-Wv8InVVlVoGks"
EXAMPLE_GID = "217255803"
REQUIRED = ["refYear", "reporterDesc", "partnerDesc", "primaryValue"]


def _csv_url(sheet_id, gid):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"


@st.cache_data(ttl=600)
def load_processed(sheet_id, gid):
    df = pd.read_csv(_csv_url(sheet_id, gid), low_memory=False)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("필수 컬럼 누락: " + ", ".join(missing))
    keep = [c for c in ["refYear", "reporterDesc", "partnerDesc", "flowDesc",
                        "qty", "netWgt", "primaryValue", "cmdDesc"] if c in df.columns]
    df = df[keep].copy()
    df = df[(df["partnerDesc"] != "World") & (df["reporterDesc"] != "World")]
    df = df.dropna(subset=["reporterDesc", "partnerDesc"])
    df["primaryValue"] = pd.to_numeric(df["primaryValue"], errors="coerce").fillna(0)
    df["refYear"] = pd.to_numeric(df["refYear"], errors="coerce")
    return df.dropna(subset=["refYear"])


def parse_sheet_url(url):
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not m:
        return None, None
    sid = m.group(1)
    g = re.search(r"[#&?]gid=([0-9]+)", url)
    return sid, (g.group(1) if g else "0")


@st.cache_data(ttl=600)
def yearly_trend(df):
    return df.groupby("refYear")["primaryValue"].sum().sort_index()


@st.cache_data(ttl=600)
def top_players(df, role, n=12):
    col = "reporterDesc" if role == "수입국" else "partnerDesc"
    return df.groupby(col)["primaryValue"].sum().sort_values(ascending=False).head(n)


@st.cache_data(ttl=600)
def edge_table(df, top_edges=70):
    return (df.groupby(["partnerDesc", "reporterDesc"])["primaryValue"].sum()
            .sort_values(ascending=False).head(top_edges).reset_index())


def get_active_df():
    src = st.session_state.get("trade_src", ("example",))
    try:
        if src[0] == "example":
            return load_processed(EXAMPLE_ID, EXAMPLE_GID), "예시 데이터 (국제 플라스틱 폐기물 무역)", None
        return load_processed(src[1], src[2]), "내 구글 스프레드시트", None
    except Exception as ex:
        return load_processed(EXAMPLE_ID, EXAMPLE_GID), "예시 데이터 (대체)", str(ex)


C = get_chart_colors()
STEPS = ["0 · 왜 무역인가", "1 🎓 데이터 구하기", "2 🛠 데이터 열기",
         "3 🛠 무역 추세", "4 🛠 주요 플레이어", "5 🛠 무역 네트워크", "6 🛠 인사이트"]

st.markdown("## 🌐 데이터로 읽는 국제무역")
st.markdown("데이터를 **어떻게 구하는지 배우고(STEP 1)**, **내 데이터(또는 예시)**로 직접 분석하는 6단계 워크숍입니다.")

if "trade_step" not in st.session_state:
    st.session_state.trade_step = STEPS[0]
st.radio("진행 단계", STEPS, key="trade_step", horizontal=True, label_visibility="collapsed")
step = STEPS.index(st.session_state.trade_step)
st.markdown("---")

df, src_label, src_err = get_active_df()

# ── STEP 0 ──
if step == 0:
    st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🌐 데이터는 국경을 넘는다</div>
  <div class='hero-sub'>
  무역은 매년 막대한 규모로 국가 사이를 오갑니다.<br>
  "누가 주고, 누가 받는가?"를 <b>데이터와 네트워크</b>로 읽어봅니다.
  </div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='eco-card'><b style='color:var(--accent-primary)'>📦 무역 데이터란</b>"
                "<p style='color:var(--text-muted);font-size:.92rem'>국가 간 사고판 기록. 무엇이 어디서 어디로 갔는지가 쌓인 의사결정 데이터.</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='eco-card'><b style='color:var(--accent-primary)'>🕸️ 네트워크란</b>"
                "<p style='color:var(--text-muted);font-size:.92rem'>점(국가)과 선(무역)으로 관계를 그린 그림. <b>선이 모이는 점=허브</b>가 핵심 주체.</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='eco-card'><b style='color:var(--accent-primary)'>🎯 오늘의 결과물</b>"
                "<p style='color:var(--text-muted);font-size:.92rem'>추세 그래프 · 주요국 순위 · 무역 네트워크 · 한 장짜리 인사이트 리포트.</p></div>", unsafe_allow_html=True)
    st.info("💡 STEP 1에서 데이터 구하는 법을 배우고, STEP 2에서 **내 시트를 연동**해 나만의 분석을 만듭니다.")

# ── STEP 1 ──
elif step == 1:
    st.markdown("### 🎓 데이터, 어디서 어떻게 구하나 — UN Comtrade")
    st.markdown("이 워크숍의 데이터는 **UN Comtrade**(유엔 국제무역 통계 DB)에서 받았습니다. "
                "같은 방법으로 원하는 품목·기간·국가를 골라 **CSV로 내려받는 법**을 익혀요. (직접 받지 않고 방법만 체득)")

    st.markdown("#### 1) 데이터 소스")
    src = pd.DataFrame({
        "출처": ["UN Comtrade", "Comtrade Plus (API)", "OEC", "관세청 무역통계"],
        "다루는 것": ["전 세계 국가 무역", "대량·자동 수집", "그래프 탐색", "한국 수출입 상세"],
        "난이도": ["보통", "다소 높음", "쉬움", "보통"],
        "무료 CSV": ["O", "O (API키)", "O", "O"],
    })
    st.dataframe(src, hide_index=True, use_container_width=True)
    st.caption("이번 데이터의 출처는 **UN Comtrade** 입니다.")

    st.markdown("#### 2) 품목을 HS 코드로 좁히기")
    st.markdown("무역 품목은 **HS 코드**로 분류돼요. 이 데이터의 품목인 **플라스틱 폐기물·스크랩 = `3915`**. "
                "친환경 분석은 이렇게 *코드로 범위를 좁히는 것*이 핵심입니다.")

    st.markdown("#### 3) 검색식(쿼리) 만들기 — 직접 해보기")
    cc1, cc2 = st.columns(2)
    hs = cc1.text_input("HS 코드", value="3915")
    reporter = cc2.text_input("보고국 (reporter, 전체=all)", value="all")
    cc3, cc4 = st.columns(2)
    y0 = cc3.number_input("시작연도", value=2017, step=1)
    y1 = cc4.number_input("끝연도", value=2023, step=1)
    flow = st.selectbox("흐름(flow)", ["Import(수입)", "Export(수출)", "둘 다"])
    flow_code = {"Import(수입)": "M", "Export(수출)": "X", "둘 다": "M,X"}[flow]
    period = ",".join(str(y) for y in range(int(y0), int(y1) + 1))
    query = (f"https://comtradeapi.un.org/data/v1/get/C/A/HS"
             f"?cmdCode={hs}&flowCode={flow_code}&reporterCode={reporter}&period={period}")
    st.code(query, language="text")
    st.caption("👆 UN Comtrade(웹 또는 API)에 이 조건을 넣고 CSV로 내려받습니다. (실제 다운로드는 강사가 시연)")
    st.success("정리: ① UN Comtrade 접속 → ② HS 코드로 품목 좁히기(3915) → ③ 보고국·기간·수출입 지정 → ④ CSV 다운로드 → ⑤ 구글시트에 업로드")

# ── STEP 2 ──  데이터 열기 + 내 시트 연동
elif step == 2:
    st.markdown("### 🛠 데이터 열어보기 — 내 시트 연동하기")
    st.markdown("**UN Comtrade에서 받은 CSV**를 구글 스프레드시트에 올린 뒤 링크를 붙여넣으면 그 데이터로 분석합니다. "
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
                load_processed(sid, gid)  # 검증
                st.session_state.trade_src = ("user", sid, gid)
                st.rerun()
            except Exception as ex:
                st.error(f"연동 실패: {ex}")
    if st.button("📋 예시 데이터 사용"):
        st.session_state.trade_src = ("example",)
        st.rerun()

    st.caption(f"필수 컬럼: {', '.join(REQUIRED)} (UN Comtrade 형식). 같은 컬럼명이면 내 데이터도 바로 분석돼요.")

    st.markdown("---")
    yrs = df["refYear"].astype(int)
    m1, m2, m3 = st.columns(3)
    m1.metric("총 거래 건수", f"{len(df):,}")
    m2.metric("기간", f"{yrs.min()}–{yrs.max()}")
    m3.metric("관련 국가 수", f"{pd.concat([df['reporterDesc'], df['partnerDesc']]).nunique()}")
    st.dataframe(df.head(200), use_container_width=True, height=320)

# ── STEP 3 ──
elif step == 3:
    st.markdown("### 🛠 무역 추세 — 언제 늘고 줄었나")
    st.caption(f"데이터: {src_label}")
    s = yearly_trend(df)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    fig.patch.set_facecolor(C["bg"]); ax.set_facecolor(C["bg"])
    ax.plot(s.index.astype(int), s.values / 1e9, marker="o", color=C["accent"], linewidth=2.5)
    ax.fill_between(s.index.astype(int), s.values / 1e9, color=C["accent"], alpha=0.15)
    for sp in ax.spines.values():
        sp.set_color(C["spine"])
    ax.tick_params(colors=C["tick"])
    ax.set_xlabel("Year", color=C["text"]); ax.set_ylabel("Value (B USD)", color=C["text"])
    ax.grid(True, color=C["spine"], alpha=0.4)
    st.pyplot(fig)
    st.markdown(
        f"<div class='eco-card'><b style='color:var(--accent-primary)'>🔎 해석해보기</b>"
        f"<p style='color:var(--text-muted)'>최고: <b>{int(s.idxmax())}년</b> · 최저: <b>{int(s.idxmin())}년</b>. "
        f"급변 지점이 있다면 어떤 사건(정책·규제)과 연결되는지 생각해보세요.</p></div>",
        unsafe_allow_html=True,
    )

# ── STEP 4 ──  증가 애니메이션 막대
elif step == 4:
    st.markdown("### 🛠 누가 주도하나 — 주요 플레이어")
    role = st.radio("기준", ["수입국", "수출국"], horizontal=True)
    s = top_players(df, role)
    mx = float(s.max()) or 1.0
    rows = ""
    for name, val in s.items():
        pct = val / mx * 100
        rows += (
            "<div class='barrow'>"
            f"<div class='barname'>{name}</div>"
            "<div class='bartrack'>"
            f"<div class='barfill' style='--w:{pct:.1f}%'></div></div>"
            f"<div class='barval'>{val/1e9:.2f}B</div>"
            "</div>"
        )
    bar_html = """
<div id="bars">
  <style>
    #bars { font-family:'Noto Sans KR',sans-serif; }
    #bars .barrow { display:flex; align-items:center; gap:10px; margin:7px 0; }
    #bars .barname { width:150px; font-size:13px; color:__TEXT__; text-align:right; flex:none; }
    #bars .bartrack { flex:1; background:__GRID__; border-radius:8px; height:22px; overflow:hidden; }
    #bars .barfill { height:100%; width:0; border-radius:8px;
        background:linear-gradient(90deg,__ACC__,__ACC2__); animation:grow 1.1s cubic-bezier(.2,.7,.2,1) forwards; }
    #bars .barval { width:62px; font-size:12px; color:__MUT__; flex:none; }
    @keyframes grow { from { width:0; } to { width:var(--w); } }
  </style>
  __ROWS__
</div>
"""
    bar_html = (bar_html.replace("__ROWS__", rows).replace("__TEXT__", C["text"])
                .replace("__GRID__", C["spine"]).replace("__ACC__", C["accent"])
                .replace("__ACC2__", C["accent2"]).replace("__MUT__", C["muted"]))
    components.html(bar_html, height=len(s) * 40 + 40)
    st.markdown(
        f"<div class='eco-card'><b style='color:var(--accent-primary)'>💬 토론</b>"
        f"<p style='color:var(--text-muted)'>{role} 1위는 <b>{s.index[0]}</b>. 왜 1위일까요? "
        f"(산업 구조 / 정책 / 인프라)</p></div>", unsafe_allow_html=True)

# ── STEP 5 ──  ForceAtlas2 네트워크 (재생/일시정지)
elif step == 5:
    st.markdown("### 🛠 무역 네트워크 — 누가 허브인가 ★")
    n_edges = st.slider("표시할 무역 흐름(엣지) 수", 30, 120, 70, step=10)
    et = edge_table(df, n_edges)

    strength = {}
    for _, r in et.iterrows():
        strength[r["partnerDesc"]] = strength.get(r["partnerDesc"], 0) + r["primaryValue"]
        strength[r["reporterDesc"]] = strength.get(r["reporterDesc"], 0) + r["primaryValue"]
    mx = max(strength.values()) or 1
    hub = max(strength, key=strength.get)
    nodes = [{"id": n, "label": n, "size": 4 + 18 * (v / mx),
              "color": C["accent"] if n == hub else C["accent2"]}
             for n, v in strength.items()]
    edges = [{"source": r["partnerDesc"], "target": r["reporterDesc"]} for _, r in et.iterrows()]

    NET = """
<div id="net-root" style="font-family:'Noto Sans KR',sans-serif;">
  <div style="display:flex; gap:8px; margin-bottom:8px;">
    <button id="net-toggle" style="font-family:inherit; padding:8px 16px; border:2px solid #1A1A1A;
      border-radius:8px; background:#FF2D6B; color:#fff; font-weight:700; cursor:pointer; box-shadow:2px 2px 0 #1A1A1A;">⏸ 일시정지</button>
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
  // drag
  let dragged=null, dragging=false;
  renderer.on("downNode", e=>{ dragging=true; dragged=e.node; });
  renderer.getMouseCaptor().on("mousemovebody", e=>{ if(!dragging||!dragged) return; const p=renderer.viewportToGraph(e); g.setNodeAttribute(dragged,"x",p.x); g.setNodeAttribute(dragged,"y",p.y); e.preventSigmaDefault(); e.original.preventDefault(); e.original.stopPropagation(); });
  renderer.getMouseCaptor().on("mouseup", ()=>{ dragging=false; dragged=null; });
</script>
"""
    NET = (NET.replace("__NODES__", json.dumps(nodes, ensure_ascii=False))
           .replace("__EDGES__", json.dumps(edges, ensure_ascii=False))
           .replace("__BG__", C["bg"]).replace("__GRID__", C["spine"]).replace("__TEXT__", C["text"]))
    components.html(NET, height=600)
    st.markdown(
        f"<div class='eco-card'><b style='color:var(--accent-primary)'>🕸️ 허브 = {hub}</b>"
        f"<p style='color:var(--text-muted)'>가장 많은 무역 흐름이 모이는 허브 국가입니다. "
        f"⏸ 버튼으로 움직임을 멈추고 구조를 천천히 살펴보세요.</p></div>", unsafe_allow_html=True)

# ── STEP 6 ──
elif step == 6:
    st.markdown("### 🛠 인사이트 정리 — 한 장 리포트 만들기")
    st.caption(f"데이터: {src_label}")
    s = yearly_trend(df)
    imp = top_players(df, "수입국", 3); exp = top_players(df, "수출국", 3)
    auto = (f"- 데이터 출처: {src_label}\n"
            f"- 분석 기간: {int(df['refYear'].min())}–{int(df['refYear'].max())}\n"
            f"- 최대 수입국: {', '.join(imp.index[:3])}\n"
            f"- 최대 수출국: {', '.join(exp.index[:3])}\n"
            f"- 무역액 최고 연도: {int(s.idxmax())}")
    st.markdown("**자동 요약 (데이터에서 추출)**")
    st.code(auto, language="text")
    a = st.text_area("📈 눈에 띄는 추세는?", height=80)
    b = st.text_area("🌍 주목할 국가/구조는?", height=80)
    cc = st.text_area("⚠️ 시사점·기회·위험은?", height=80)
    if st.button("📄 리포트 생성"):
        report = ("■ 국제무역 데이터 분석 리포트\n==============================\n\n"
                  "[데이터 요약]\n" + auto + "\n\n[추세 해석]\n" + (a or "-") +
                  "\n\n[주목 국가/구조]\n" + (b or "-") + "\n\n[시사점/기회/위험]\n" + (cc or "-") + "\n")
        st.download_button("⬇️ 리포트 다운로드 (.txt)", report,
                           file_name="trade_report.txt", mime="text/plain")
        st.success("데이터로 시작해 결론까지 — 각자 다른 데이터면 각자 다른 리포트가 나옵니다!")
