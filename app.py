# import streamlit as st
# from shared import apply_css

# st.set_page_config(
#     page_title="Eco Lab. Jeju",
#     page_icon="🌿",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# apply_css()

# # ─────────────────────────────────────────────
# #  SIDEBAR NAVIGATION
# # ─────────────────────────────────────────────
# pages = {
#     "Eco Lab. Jeju": [
#         st.Page("home.py", title="홈 (소개)", icon="🏠"),
#         st.Page("pages/1_samdasoo_eco_race.py", title="삼다수 에코 레이스", icon="🎮"),
#         st.Page("pages/2_environment_action_network.py", title="우리 반 환경행동 네트워크", icon="📊"),
#     ]
# }

# pg = st.navigation(pages)
# pg.run()
import streamlit as st
from shared import apply_css

st.set_page_config(
    page_title="Eco Lab. Jeju",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_css()

with st.sidebar:
    st.markdown("## 🌿 Eco Lab. Jeju")
    st.markdown("##### 에코랩 제주")
    st.markdown("---")

pages = [
    st.Page("home.py", title="홈 (소개)", icon="🏠"),
    st.Page("pages/1_samdasoo_eco_race.py", title="삼다수 에코 레이스", icon="🎮"),
    st.Page("pages/2_environment_action_network.py", title="우리 반 환경행동 네트워크", icon="📊"),
]

pg = st.navigation(pages)
pg.run()

with st.sidebar:
    st.markdown("---")
    st.markdown("""
<div style='font-size:.8rem; color:#2e7d5f; line-height:1.6;'>
데이터 사이언스 × 환경 교육<br>
제주 대정중학교 교육 프로그램 <br><br>
제작: 서울대학교 샤오름
</div>
""", unsafe_allow_html=True)
