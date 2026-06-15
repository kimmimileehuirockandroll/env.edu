import streamlit as st
from shared import apply_css

st.set_page_config(
    page_title="Eco Lab. Jeju",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_css()

# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
pages = {
    "Eco Lab. Jeju": [
        st.Page("home.py", title="홈 (소개)", icon="🏠"),
        st.Page("pages/1_samdasoo_eco_race.py", title="삼다수 에코 레이스", icon="🎮"),
        st.Page("pages/2_environment_action_network.py", title="우리 반 환경행동 네트워크", icon="📊"),
    ]
}

pg = st.navigation(pages)
pg.run()
