import streamlit as st
from shared import apply_css

apply_css()

st.markdown("## 🪲 곤충 살인사건 수사본부")
st.markdown("곤충 탐정단이 되어 사건의 원인을 추리하고, 환경 문제와 곤충 생태를 연결해봅니다.")

# ─────────────────────────────────────────────
# 사건 브리핑
# ─────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🚨 곤충 살인사건 발생!</div>
  <div class='hero-sub'>
  제주 생태계에서 곤충들이 사라지고 있습니다.<br>
  범인은 누구일까요? 지구온난화, 외래종, 농지 개발, 토양오염 중 진짜 원인을 찾아보세요.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🪄 곤충화 프로그램")
st.markdown("""
<div class='eco-card'>
<b style='color:#69f0ae;'>곤충이 되어보는 이유</b>
<p style='color:#80cbc4; font-size:.95rem; line-height:1.7;'>
곤충의 시선으로 세상을 바라보면 인간 활동이 생태계에 어떤 영향을 주는지 더 잘 이해할 수 있습니다.<br>
오늘 여러분은 곤충 탐정단이 되어 단서를 찾고, 용의자의 알리바이를 분석하고, 사건의 진실을 밝혀야 합니다.
</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 사전 교육자료
# ─────────────────────────────────────────────
st.markdown("### 📚 사전 교육자료")

edu_col1, edu_col2 = st.columns(2)

with edu_col1:
    st.markdown("""
<div class='eco-card'>
<h3>🐞 곤충 이해하기</h3>
<p style='color:#80cbc4; font-size:.92rem; line-height:1.7;'>
곤충은 꽃가루받이, 먹이사슬 유지, 유기물 분해 등 생태계에서 중요한 역할을 합니다.
</p>
<p style='color:#4db6ac; font-size:.85rem;'>
※ 여기에 구글 드라이브 PDF 또는 곤충 교육자료를 넣을 예정
</p>
</div>
""", unsafe_allow_html=True)

with edu_col2:
    st.markdown("""
<div class='eco-card'>
<h3>🌍 곤충이 사라지는 이유</h3>
<p style='color:#80cbc4; font-size:.92rem; line-height:1.7;'>
지구온난화, 외래종 증가, 환경오염, 농약 사용, 산불과 홍수, 벌목, 빛 공해, 농지 개발 등이 곤충의 생존을 위협합니다.
</p>
<p style='color:#4db6ac; font-size:.85rem;'>
※ 여기에 관련 영상 또는 이미지 자료를 넣을 예정
</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 용의자 조사실
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🕵️ 용의자 조사실")

suspects = [
    {
        "cause": "지구온난화",
        "name": "미스터 카",
        "role": "관광객",
        "alibi": "어제 성산일출봉을 보고 왔다고 주장함",
        "emoji": "🚗",
        "color": "#69f0ae",
    },
    {
        "cause": "외래종·천적 증가",
        "name": "사마귀",
        "role": "곤충",
        "alibi": "AI 목소리로 Bzzzzzz 알리바이를 남김",
        "emoji": "🦗",
        "color": "#40c4ff",
    },
    {
        "cause": "농지 개발",
        "name": "모내기",
        "role": "농부",
        "alibi": "제주 사투리로 땅을 사고 왔다고 주장함",
        "emoji": "🌾",
        "color": "#ffd740",
    },
    {
        "cause": "토양오염",
        "name": "산조아",
        "role": "등산객",
        "alibi": "산을 타고 왔다고 주장함",
        "emoji": "⛰️",
        "color": "#ff8a65",
    },
]

cols = st.columns(4)

for col, s in zip(cols, suspects):
    with col:
        st.markdown(f"""
<div class='eco-card' style='min-height:250px;'>
  <div style='font-size:2.4rem; text-align:center;'>{s["emoji"]}</div>
  <h3 style='text-align:center; color:{s["color"]} !important;'>{s["name"]}</h3>
  <p style='color:#b2dfdb; font-size:.9rem; line-height:1.6;'>
  <b>정체:</b> {s["role"]}<br>
  <b>관련 원인:</b> {s["cause"]}<br><br>
  <b>알리바이</b><br>
  {s["alibi"]}
  </p>
  <p style='color:#4db6ac; font-size:.82rem;'>
  ※ 여기에 용의자 영상 삽입 예정
  </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 범행 원인 분석
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🔬 범행 원인 분석")

tab1, tab2, tab3, tab4 = st.tabs([
    "🌡️ 지구온난화",
    "🦗 외래종·천적",
    "🚜 농지 개발",
    "🧪 토양오염",
])

with tab1:
    st.markdown("""
<div class='eco-card'>
<h3>🌡️ 지구온난화</h3>
<p style='color:#80cbc4; line-height:1.7;'>
기온이 상승하면 곤충의 서식지가 이동하고, 기존 생태계의 균형이 깨질 수 있습니다.
따뜻한 지역의 곤충이 새로운 지역으로 이동하면서 기존 곤충과 경쟁하거나 먹이사슬에 영향을 줄 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

with tab2:
    st.markdown("""
<div class='eco-card'>
<h3>🦗 외래종과 천적의 증가</h3>
<p style='color:#80cbc4; line-height:1.7;'>
외래종은 원래 그 지역에 살던 생물이 아닙니다.
새로운 외래종이나 천적이 들어오면 기존 곤충의 수가 급격히 줄어들 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

with tab3:
    st.markdown("""
<div class='eco-card'>
<h3>🚜 농지 개발</h3>
<p style='color:#80cbc4; line-height:1.7;'>
숲과 초지가 농지나 건물로 바뀌면 곤충이 살 곳을 잃게 됩니다.
농약과 살충제 사용도 곤충 개체 수 감소의 중요한 원인이 될 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

with tab4:
    st.markdown("""
<div class='eco-card'>
<h3>🧪 토양오염</h3>
<p style='color:#80cbc4; line-height:1.7;'>
쓰레기, 세제, 담배꽁초, 화학물질은 토양과 물을 오염시킵니다.
토양이 오염되면 땅속에 사는 곤충과 애벌레가 직접적인 피해를 입을 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 단서 목록
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🧩 운동장 수사 단서 목록")

clues = [
    ["지구온난화", "미스터 카", "차 배경 셀카 사진 / 비행기 사진 / CO₂"],
    ["외래종·천적 증가", "사마귀", "라오스·베트남 국기 / omnivore / 삼각형 세 각의 합 180도"],
    ["농지 개발", "모내기", "땅 문서 / 쟁기 / 농약 글자 / 밭"],
    ["토양오염", "산조아", "컵라면 / 수세미·세제 / 담배꽁초 / 등산 스틱"],
]

st.table(
    {
        "원인": [c[0] for c in clues],
        "용의자": [c[1] for c in clues],
        "찾아야 할 단서": [c[2] for c in clues],
    }
)

# ─────────────────────────────────────────────
# 탐정 수첩
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📝 탐정 수첩")

st.markdown("운동장에서 찾은 단서를 체크하고, 조별 토의 전에 생각을 정리해보세요.")

check_col1, check_col2 = st.columns(2)

with check_col1:
    st.checkbox("🚗 차 배경 셀카 사진을 찾았다")
    st.checkbox("✈️ 비행기 사진을 찾았다")
    st.checkbox("CO₂ 단서를 찾았다")
    st.checkbox("🌏 라오스/베트남 국기 단서를 찾았다")
    st.checkbox("🦗 omnivore 단서를 찾았다")
    st.checkbox("🔺 180도 단서를 찾았다")

with check_col2:
    st.checkbox("📄 땅 문서를 찾았다")
    st.checkbox("🚜 쟁기 단서를 찾았다")
    st.checkbox("🧪 농약 글자를 찾았다")
    st.checkbox("🍜 컵라면 단서를 찾았다")
    st.checkbox("🧼 수세미/세제 단서를 찾았다")
    st.checkbox("🚬 담배꽁초 단서를 찾았다")

memo = st.text_area(
    "🔎 우리 조가 가장 중요하다고 생각한 단서",
    placeholder="예: CO₂와 비행기 사진은 지구온난화와 관련이 있어 보인다...",
    height=120,
)

# ─────────────────────────────────────────────
# 최종 추리
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🗳️ 현재 가장 의심되는 용의자")

suspect_vote = st.radio(
    "단서를 바탕으로 현재 가장 의심되는 용의자를 선택하세요.",
    ["아직 모르겠다", "미스터 카", "사마귀", "모내기", "산조아"],
    horizontal=True,
)

reason = st.text_area(
    "왜 그렇게 생각했나요?",
    placeholder="우리 조의 추리 근거를 적어보세요.",
    height=100,
)

if st.button("🕵️ 추리 기록 저장"):
    st.success("탐정 수첩에 추리 기록이 저장되었습니다! 조별 토의에서 이 근거를 활용해보세요.")

st.markdown("""
<div class='eco-footer'>
곤충 살인사건 · 환경 변화와 곤충 생태계 이해를 위한 방탈출 사전 교육자료
</div>
""", unsafe_allow_html=True)
