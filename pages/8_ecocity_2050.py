from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from shared import apply_css, lesson_flow

apply_css()

# 자산 경로 (이 파일 기준 ../assets)
ASSETS = Path(__file__).resolve().parent.parent / "assets"
GAME_HTML = ASSETS / "ecocity.html"
GUIDE_MD = ASSETS / "ecocity_teacher_guide.md"

st.markdown("## 🏙️ 에코시티 2050")

lesson_flow(
    "ecocity2050",
    concept=[
        {"title": "📘 Chapter 1 · 탄소중립과 넷제로", "body": """
<p style='line-height:1.8'>
<b>탄소중립(넷제로, Net-Zero)</b>은 배출하는 온실가스와 흡수·제거하는 양을 같게 만들어
<b>순배출을 0으로</b> 만드는 것입니다. 완전히 안 쓰는 게 아니라, 쓴 만큼 상쇄한다는 개념이에요.<br><br>
전 세계는 지구 평균 기온 상승을 억제하기 위해 <b>2050년 탄소중립</b>을 목표로 합니다.
그 중간 목표로 흔히 "2030년까지 <b>−45~55%</b>" 같은 감축이 제시돼요. 이 게임의 목표
<b>−55%</b>도 여기서 왔습니다.
</p>
<p style='color:var(--text-caption); font-size:.85rem'>💡 도시는 전 세계 탄소의 큰 부분을 배출하기에, 도시 전환이 특히 중요합니다.</p>
"""},
        {"title": "📗 Chapter 2 · 은탄환은 없다 — 포트폴리오 전략", "body": """
<p style='line-height:1.8'>
"태양광만 잔뜩 깔면 되지 않나?" — 안 됩니다. 어떤 <b>단 하나의 해법(은탄환, silver bullet)</b>으로
기후 목표를 달성할 수는 없어요.<br><br>
현실에서는 <b>여러 정책을 동시에 조합</b>해야 합니다 — 재생에너지 확대 + 건물 단열 + 전기차·대중교통
+ 산업 효율화 등. 이렇게 여러 수단을 섞는 것을 <b>포트폴리오 전략</b>이라고 해요. 한 분야만
밀면 어딘가에서 반드시 막힙니다(전력망 한계, 비용 폭증 등).
</p>
"""},
        {"title": "📙 Chapter 3 · 전환의 순서와 사회적 수용성", "body": """
<p style='line-height:1.8'>
정책엔 <b>순서와 시간(리드타임)</b>이 있습니다. 청정 발전소를 <b>먼저 짓고</b> 나서 석탄을 닫아야
정전이 안 나요. 순서를 어기면 좋은 의도도 재앙이 됩니다.<br><br>
또한 좋은 정책도 <b>사람들의 반발</b>에 부딪힙니다 — 석탄 노동자의 일자리, 혼잡통행료의 형평성 등.
그래서 <b>사회적 수용성</b>과 <b>정의로운 전환(공정하게 부담 나누기)</b>이 중요해요.
게임 속 '정치자본'이 바로 이 현실을 표현한 자원입니다.
</p>
<p style='color:var(--text-caption); font-size:.85rem'>🎯 문제: 예산·정치자본 안에서 6임기 동안 탄소 −55%를 어떻게 달성할까?</p>
"""},
    ],
    discuss=[
        "왜 석탄을 한 번에 못 닫았나요? (전환의 순서·정전 리스크)",
        "태양광 한 가지만 밀었다면 어떻게 됐을까요? 왜 여러 정책이 필요했나요?",
        "가장 어려웠던 트레이드오프는? 무엇을 위해 무엇을 포기했나요?",
        "시민·노조가 화난 순간이 있었나요? 그때 어떤 책임이 있었을까요?",
    ],
    present="""
<div class='eco-card'>
<b style='color:var(--accent-primary)'>🎤 발표: 시장의 정책 브리프</b>
<ul style='color:var(--text-muted); line-height:1.8'>
<li>최종 <b>탄소 감축률</b>과 목표 달성 여부</li>
<li>가장 자랑스러운 결정과 가장 후회되는 결정</li>
<li>다시 시장이 된다면 <b>가장 먼저 바꿀 한 수</b></li>
</ul>
</div>
""",
)

st.markdown("2025→2050년, 6임기 동안 신임 시장이 되어 도시의 **탄소배출 −55%**에 도전하는 픽셀아트 도시경영 시뮬레이션입니다.")

st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🗳️ 당신은 신임 시장</div>
  <div class='hero-sub'>
  정책 카드로 에너지·교통·건물을 바꾸고, 예산과 정치자본 속에서 트레이드오프를 협상하세요.<br>
  은탄환은 없습니다 — 여러 정책을 조합해 기후 목표를 달성해야 합니다.
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 게임 임베드 (자체완결형 HTML)
# ─────────────────────────────────────────────
if GAME_HTML.exists():
    html = GAME_HTML.read_text(encoding="utf-8")
    components.html(html, height=900, scrolling=True)
else:
    st.error("게임 파일(assets/ecocity.html)을 찾을 수 없습니다.")

st.caption("💡 화면이 작게 보이면 위 게임 영역 안에서 스크롤하거나, 브라우저 창을 넓혀보세요.")

# ─────────────────────────────────────────────
# 교사용 수업 가이드
# ─────────────────────────────────────────────
st.divider()
with st.expander("📚 교사용 수업 가이드 (차시 설계 · 디브리핑 질문 · 워크시트)"):
    if GUIDE_MD.exists():
        st.markdown(GUIDE_MD.read_text(encoding="utf-8"))
    else:
        st.info("교사용 가이드 파일(assets/ecocity_teacher_guide.md)을 찾을 수 없습니다.")
