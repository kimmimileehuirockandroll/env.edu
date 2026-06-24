from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from shared import apply_css

apply_css()

# 자산 경로 (이 파일 기준 ../assets)
ASSETS = Path(__file__).resolve().parent.parent / "assets"
GAME_HTML = ASSETS / "ecocity.html"
GUIDE_MD = ASSETS / "ecocity_teacher_guide.md"

st.markdown("## 🏙️ 에코시티 2050")
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
