import streamlit as st
from shared import apply_css

st.set_page_config(
    page_title="Eco Lab. Jeju",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_css()

# 페이지 등록
home = st.Page("home.py", title="HOME", icon="🏠")
game1 = st.Page("pages/1_samdasoo_eco_race.py", title="삼다수 에코 레이스", icon="🎮")
network1 = st.Page("pages/2_environment_action_network.py", title="우리 반 환경행동 네트워크", icon="📊")

pages = {
    "Home": [home],
    "Network": [game1],
    "Survey": [network1],
}

pg = st.navigation(pages, position="hidden")

# 직접 만든 사이드바
with st.sidebar:
    st.markdown("""
<a href="/" target="_self" style="text-decoration:none;">
    <div style="
        color:#69f0ae;
        font-size:1.5rem;
        font-weight:800;
        margin-bottom:0.1rem;
    ">
        🌿 Eco Lab. Jeju
    </div>

    <div style="
        color:#80cbc4;
        font-size:0.95rem;
        font-weight:600;
        margin-bottom:0.8rem;
    ">
        에코랩 제주
    </div>
</a>
""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("#### Network")
    st.page_link(game1, label="삼다수 에코 레이스", icon="🎮")
    # st.page_link(game2, label="게임2", icon="🎮")
    # st.page_link(game3, label="게임3", icon="🎮")

    st.markdown("#### Survey")
    st.page_link(network1, label="우리 반 환경행동 네트워크", icon="📊")
    # st.page_link(game5, label="게임5", icon="📊")
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
