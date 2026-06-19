import streamlit as st
from shared import apply_css

apply_css()

st.markdown("## 🪲 살충사건 수사본부")
st.markdown("곤충 탐정단이 되어 사건의 원인을 추리하고, 환경 문제와 곤충 생태를 연결해봅니다.")

# ─────────────────────────────────────────────
# 사건 브리핑
# ─────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🚨 살충사건 발생!</div>
  <div class='hero-sub'>
  제주 생태계에서 곤충들이 사라지고 있습니다.<br>
  범인은 누구일까요? 지구온난화, 외래종, 농지 개발, 토양오염 중 진짜 원인을 찾아보세요.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🪄 우리는 이제부터 곤충")
st.markdown("""
<div class='eco-card'>
<b style='color:var(--accent-primary);'>곤충이 되어보는 이유</b>
<p style='color:var(--text-muted); font-size:.95rem; line-height:1.7;'>
곤충의 시선으로 세상을 바라보면 인간 활동이 생태계에 어떤 영향을 주는지 더 잘 이해할 수 있습니다.<br>
오늘 여러분은 곤충 탐정단이 되어 단서를 찾고, 용의자의 알리바이를 분석하고, 사건의 진실을 밝혀야 합니다.
</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 사전 교육자료
# ─────────────────────────────────────────────
st.markdown("### 📚 사전 교육자료")

st.markdown("""
<div class='eco-card'>
<h3>🐞 곤충 이해하기</h3>
<p style='color:var(--text-muted); font-size:.95rem; line-height:1.7;'>
곤충은 꽃가루받이, 먹이사슬 유지, 유기물 분해 등 생태계에서 중요한 역할을 합니다.
</p>
<p style='color:var(--text-caption); font-size:.85rem;'>
※ 여기에 구글 드라이브 PDF 또는 곤충 교육자료를 넣을 예정
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='eco-card'>
<h3>🌍 곤충이 사라지는 이유</h3>
<p style='color:var(--text-muted); font-size:.95rem; line-height:1.7;'>
지구온난화, 외래종 증가, 환경오염, 농약 사용, 산불과 홍수, 벌목, 빛 공해, 농지 개발 등이 곤충의 생존을 위협합니다.
</p>
<p style='color:var(--text-caption); font-size:.85rem;'>
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
        "name": "Mr.Car",
        "role": "관광객",
        "alibi": "어제 성산일출봉을 보고 왔다고 주장함",
        "emoji": "🚗",
        "color": "#1A1A1A",
    },
    {
        "name": "사마귀",
        "role": "곤충",
        "alibi": "AI 목소리로 Bzzzzzz 알리바이를 남김",
        "emoji": "🦗",
        "color": "#1A1A1A",
    },
    {
        "name": "모내기",
        "role": "농부",
        "alibi": "제주 사투리로 땅을 사고 왔다고 주장함",
        "emoji": "🌾",
        "color": "#1A1A1A",
    },
    {
        "name": "산조아",
        "role": "등산객",
        "alibi": "산을 타고 왔다고 주장함",
        "emoji": "⛰️",
        "color": "#1A1A1A",
    },
]

if "selected_suspect" not in st.session_state:
    st.session_state.selected_suspect = 0

left_col, right_col = st.columns([1, 3])

with left_col:
    st.markdown("#### 용의자")

    for i, s in enumerate(suspects):
        if st.button(
            f"{s['emoji']} {s['name']}",
            key=f"suspect_btn_{i}",
            use_container_width=True,
        ):
            st.session_state.selected_suspect = i

selected = suspects[st.session_state.selected_suspect]

with right_col:
    st.markdown(f"""
<div class='eco-card' style='min-height:320px;'>
  <div style='font-size:3rem;'>{selected["emoji"]}</div>
  <h2 style='color:{selected["color"]} !important;'>{selected["name"]}</h2>

  <p style='color:var(--text-base); font-size:1rem; line-height:1.8;'>
  <b>직업:</b> {selected["role"]}<br>
  <b>알리바이:</b><br>
  {selected["alibi"]}
  </p>

  <div style='
      margin-top:1rem;
      padding:1rem;
      border:1px dashed var(--border-main);
      border-radius:12px;
      color:var(--text-caption);
      font-size:.9rem;
  '>
  🎥 여기에 선택한 용의자의 영상을 삽입할 예정
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 범행 원인 분석 -> 제거?
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
<p style='color:var(--text-muted); line-height:1.7;'>
기온이 상승하면 곤충의 서식지가 이동하고, 기존 생태계의 균형이 깨질 수 있습니다.
따뜻한 지역의 곤충이 새로운 지역으로 이동하면서 기존 곤충과 경쟁하거나 먹이사슬에 영향을 줄 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

with tab2:
    st.markdown("""
<div class='eco-card'>
<h3>🦗 외래종과 천적의 증가</h3>
<p style='color:var(--text-muted); line-height:1.7;'>
외래종은 원래 그 지역에 살던 생물이 아닙니다.
새로운 외래종이나 천적이 들어오면 기존 곤충의 수가 급격히 줄어들 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

with tab3:
    st.markdown("""
<div class='eco-card'>
<h3>🚜 농지 개발</h3>
<p style='color:var(--text-muted); line-height:1.7;'>
숲과 초지가 농지나 건물로 바뀌면 곤충이 살 곳을 잃게 됩니다.
농약과 살충제 사용도 곤충 개체 수 감소의 중요한 원인이 될 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

with tab4:
    st.markdown("""
<div class='eco-card'>
<h3>🧪 토양오염</h3>
<p style='color:var(--text-muted); line-height:1.7;'>
쓰레기, 세제, 담배꽁초, 화학물질은 토양과 물을 오염시킵니다.
토양이 오염되면 땅속에 사는 곤충과 애벌레가 직접적인 피해를 입을 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 단서 목록
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🗺️ 운동장 단서 지도")

st.markdown("""
<div class='eco-card'>
<h3>🔎 운동장 수사 구역</h3>
<p style='color:var(--text-muted); font-size:.95rem; line-height:1.7;'>
운동장 곳곳에 숨겨진 단서를 찾아보세요.
각 단서는 특정 용의자와 환경 문제에 연결되어 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

st.image(
    "jeju_insect.png",
    use_container_width=True,
)

st.info("""
🕵️ 탐정 미션

운동장에 숨겨진 단서를 모두 찾아 기록하세요.

🚗 Mr.Car
🦗 사마귀
🌾 모내기
⛰️ 산조아

각 단서가 어떤 환경 문제를 의미하는지 조별로 토의해보세요.
""")

hint_col1, hint_col2 = st.columns(2)

with hint_col1:
    st.markdown("""
<div class='eco-card'>
<h3>📍 힌트 구역 A</h3>
<p style='color:var(--text-muted);'>
교통, 이동, 탄소 배출과 관련된 단서가 숨어 있을 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='eco-card'>
<h3>📍 힌트 구역 B</h3>
<p style='color:var(--text-muted);'>
외래종, 천적, 먹이사슬과 관련된 단서를 찾아보세요.
</p>
</div>
""", unsafe_allow_html=True)

with hint_col2:
    st.markdown("""
<div class='eco-card'>
<h3>📍 힌트 구역 C</h3>
<p style='color:var(--text-muted);'>
농지 개발, 농약, 땅의 변화와 관련된 단서가 있을 수 있습니다.
</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='eco-card'>
<h3>📍 힌트 구역 D</h3>
<p style='color:var(--text-muted);'>
토양오염, 쓰레기, 생활 오염과 관련된 단서를 확인해보세요.
</p>
</div>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────
# 탐정 수첩
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📝 탐정 수첩")

st.markdown("""
운동장에서 발견한 단서를 기록해보세요.

어떤 단서가 어떤 원인과 연결되는지는 아직 알 수 없습니다.
조별 토의를 통해 의미를 추리해보세요.
""")

st.markdown("#### 🔍 단서 수집 현황")

headers = st.columns([2,1,1,1,1])

headers[0].markdown("**단서 종류**")
headers[1].markdown("**단서 1**")
headers[2].markdown("**단서 2**")
headers[3].markdown("**단서 3**")
headers[4].markdown("**단서 4**")

clue_types = [
    ("🚗 Mr.Car", "A"),
    ("🦗 사마귀", "B"),
    ("🌾 모내기", "C"),
    ("⛰️ 산조아", "D"),
]

for label, prefix in clue_types:

    cols = st.columns([2,1,1,1,1])

    cols[0].markdown(f"**{label}**")

    for i in range(1,5):
        cols[i].checkbox(
            "",
            key=f"{prefix}_{i}",
            label_visibility="collapsed"
        )

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
    ["아직 모르겠다", "Mr.Car", "사마귀", "모내기", "산조아"],
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
