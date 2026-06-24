import streamlit as st
from shared import apply_css, level_selector

st.set_page_config(
    page_title="Eco Lab. Jeju",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_css()

# 페이지 등록
home = st.Page("home.py", title="HOME", icon="🏠")
game1 = st.Page("pages/1_samdasoo_eco_race.py", title="삼다수 에코 레이스", icon="🎮")
game2 = st.Page("pages/4_insect_murder_case.py", title="살충사건 수사본부",icon="🪲")
game3 = st.Page("pages/5_jeju_ecosystem_balance.py", title="제주 생태계 밸런스", icon="🌋")
game4 = st.Page("pages/6_pixel_eco_city.py", title="픽셀 에코시티", icon="🏙️")
game5 = st.Page("pages/7_oreumi_diary.py", title="오름이의 환경 다이어리", icon="🦌")
game6 = st.Page("pages/8_ecocity_2050.py", title="에코시티 2050", icon="🏙️")
network1 = st.Page("pages/2_environment_action_network.py", title="1반 환경행동 네트워크", icon="📊")
network2 = st.Page("pages/3_survey2.py", title="2반 환경행동 네트워크", icon="📊")

pages = {
    "Home": [home],
    "Network": [game1, game2, game3, game4, game5, game6],
    "Survey": [network1, network2],
}

pg = st.navigation(pages, position="hidden")

# 직접 만든 사이드바
with st.sidebar:
    st.markdown(
        """
        <a href="./" target="_self" class="brand-link">
            <div class="brand-title">🌷</br> Eco Lab. Jeju</div>
            <div class="brand-subtitle">에코랩 제주</div>
        </a>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # 학습자 레벨 토글 — 초등/중등/고등/대학·성인
    level_selector()
    st.markdown("---")

    st.markdown("#### Network")
    st.page_link(game1, label="삼다수 에코 레이스", icon="🎮")
    st.page_link(game2, label="살충사건 수사본부", icon="🪲")
    st.page_link(game3, label="제주 생태계 밸런스", icon="🌋")
    st.page_link(game4, label="픽셀 에코시티", icon="🏙️")
    st.page_link(game5, label="오름이의 환경 다이어리", icon="🦌")
    st.page_link(game6, label="에코시티 2050", icon="🏙️")
    # st.page_link(game2, label="게임2", icon="🎮")
    # st.page_link(game3, label="게임3", icon="🎮")

    st.markdown("#### Survey")
    st.page_link(network1, label="1반 환경행동 네트워크", icon="📊")
    st.page_link(network2, label="2반 환경행동 네트워크", icon="📊")
    # st.page_link(game6, label="게임6", icon="📊")

    st.markdown("---")
    st.markdown("""
<div style='font-size:.8rem; color:#2e7d5f; line-height:1.6;'>
데이터 사이언스 × 환경 교육<br>
제주 대정중학교 교육 프로그램 <br><br>
제작: 서울대학교 샤오름
</div>
""", unsafe_allow_html=True)

pg.run()
