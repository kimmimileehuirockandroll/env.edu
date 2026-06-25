import streamlit as st
from shared import apply_css, level_selector, page_visible

st.set_page_config(
    page_title="Eco Lab. Jeju",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_css()

# ─────────────────────────────────────────────
#  페이지 등록
# ─────────────────────────────────────────────
home = st.Page("home.py", title="HOME", icon="🏠")
game1 = st.Page("pages/1_samdasoo_eco_race.py", title="삼다수 에코 레이스", icon="🎮")
game2 = st.Page("pages/4_insect_murder_case.py", title="살충사건 수사본부", icon="🪲")
game3 = st.Page("pages/5_jeju_ecosystem_balance.py", title="제주 생태계 밸런스", icon="🌋")
game4 = st.Page("pages/6_pixel_eco_city.py", title="픽셀 에코시티", icon="🏙️")
game5 = st.Page("pages/7_oreumi_diary.py", title="오름이의 환경 다이어리", icon="🦌")
game6 = st.Page("pages/8_ecocity_2050.py", title="에코시티 2050", icon="🏙️")
game7 = st.Page("pages/9_eco_hero.py", title="플로깅 러쉬", icon="🏃")
game8 = st.Page("pages/10_board_quiz.py", title="아이스브레이킹", icon="🧊")
network1 = st.Page("pages/2_environment_action_network.py", title="1반 환경행동 네트워크", icon="📊")
network2 = st.Page("pages/3_survey2.py", title="2반 환경행동 네트워크", icon="📊")

# ─────────────────────────────────────────────
#  레벨 매핑 — 각 페이지가 어떤 학습자 레벨에 속하는지 (중복 가능)
#  여기 levels 리스트만 고치면 사이드바 노출 대상이 바뀝니다.
#  levels=None  → 레벨과 무관하게 항상 표시 (예: HOME)
#  (그룹, 페이지, 라벨, 아이콘, levels)
# ─────────────────────────────────────────────
SECTIONS = [
    ("Home", [
        (home, "HOME", "🏠", None),
    ]),
    ("Game", [
        (game1, "삼다수 에코 레이스", "🎮", ["중등", "고등"]),
        (game2, "살충사건 수사본부", "🪲", ["초등", "중등"]),
        (game3, "제주 생태계 밸런스", "🌋", ["고등", "대학·성인"]),
        (game4, "픽셀 에코시티", "🏙️", ["초등"]),
        (game5, "오름이의 환경 다이어리", "🦌", ["초등"]),
        (game6, "에코시티 2050", "🏙️", ["고등", "대학·성인"]),
        (game7, "플로깅 러쉬", "🏃", ["초등", "중등"]),
        (game8, "아이스브레이킹", "🧊", ["중등"]),
    ]),
    ("Survey", [
        (network1, "1반 환경행동 네트워크", "📊", ["중등", "고등", "대학·성인"]),
        (network2, "2반 환경행동 네트워크", "📊", ["중등", "고등", "대학·성인"]),
    ]),
]

# ── 사이드바 1단계: 브랜드 + 레벨 토글 (먼저 그려서 선택값을 읽는다) ──
with st.sidebar:
    st.markdown(
        """
        <a href="./" target="_self" class="brand-link">
            <div class="brand-title">🌷</br> Eco Lab. Jeju</div>
            <div class="brand-subtitle">에코랩 제주</div>
        </a>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    level_selector()
    st.markdown("---")

# ── 현재 레벨에 맞는 페이지만 필터링 ──
nav_pages = {}
for section, entries in SECTIONS:
    visible = [page for (page, _l, _i, levels) in entries if page_visible(levels)]
    if visible:
        nav_pages[section] = visible

pg = st.navigation(nav_pages, position="hidden")

# ── 사이드바 2단계: 필터링된 페이지 링크 ──
with st.sidebar:
    for section, entries in SECTIONS:
        if section == "Home":
            continue  # 홈 링크는 상단 브랜드가 대신함
        links = [(page, label, icon) for (page, label, icon, levels) in entries
                 if page_visible(levels)]
        if not links:
            continue
        st.markdown(f"#### {section}")
        for page, label, icon in links:
            st.page_link(page, label=label, icon=icon)

    st.markdown("---")
    st.markdown(
        """
<div style='font-size:.8rem; color:var(--text-muted); line-height:1.6;'>
데이터 사이언스 × 환경 교육<br>
제주 대정중학교 교육 프로그램 <br><br>
제작: 서울대학교 샤오름
</div>
""",
        unsafe_allow_html=True,
    )

pg.run()
