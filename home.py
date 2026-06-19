import streamlit as st
from shared import apply_css

apply_css()

# 히어로 배너를 최상단에 붙이기
st.markdown("""
<style>
.block-container {
    padding-top: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🌷<br>에코랩 제주</div>
  <div class='hero-sub'>데이터 사이언스 × 환경 교육</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
<div class='eco-card'>
  <h3>🎮 삼다수 에코 레이스</h3>
  <p style='color:#80cbc4; font-size:.95rem;'>
  제주도의 6개 랜드마크를 탐험하는 네트워크 게임!<br>
  대중교통 vs. 전기 렌터카 중 최적의 이동 수단을 선택하며<br>
  <b style='color:#69f0ae;'>시간 · 탄소 · 비용</b> 세 가지 자원을 관리해보세요.<br><br>
  지름길이 항상 정답이 아닙니다. 트레이드오프를 분석해 가장 많은 랜드마크를 방문하세요!
  </p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class='eco-card'>
  <h3>🪲 살충사건 수사본부</h3>
  <p style='color:#80cbc4; font-size:.95rem;'>
  사라지는 곤충들, 그리고 수상한 용의자들!<br>
  지구온난화 · 외래종 증가 · 농지 개발 · 토양오염 중<br>
  곤충 생태계를 위협한 진짜 원인을 추리해보세요.<br><br>
  <b style='color:#69f0ae;'>용의자 영상 · 단서 수집 · 조별 추리</b>를 통해<br>
  곤충 탐정단이 되어 사건의 진실을 밝혀봅니다!
  </p>
</div>
""", unsafe_allow_html=True)
  
with col3:
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
