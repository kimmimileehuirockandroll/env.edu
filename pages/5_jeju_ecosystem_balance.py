import random

import streamlit as st

from shared import apply_css, get_chart_colors, lesson_flow

apply_css()

TOTAL_TURNS = 6
START_BUDGET_BASE = 60

POLICY_POOL = [
    {"name": "곶자왈 보호구역 지정", "cost": 40, "tourism": -5, "satisfaction": 5, "ecology": 15,
     "desc": "관광 개발은 줄지만 제주 고유 생태계를 지킵니다."},
    {"name": "대형 리조트 유치", "cost": 30, "tourism": 15, "satisfaction": -3, "ecology": -12,
     "desc": "관광 수입은 늘지만 해안 환경에 부담을 줍니다."},
    {"name": "전기버스 도입", "cost": 25, "tourism": 2, "satisfaction": 5, "ecology": 8,
     "desc": "대기질 개선과 주민 만족도 상승."},
    {"name": "관광객 수 제한", "cost": 10, "tourism": -15, "satisfaction": 8, "ecology": 10,
     "desc": "혼잡도가 줄고 생태계가 회복할 시간을 얻습니다."},
    {"name": "해양 정화 캠페인", "cost": 20, "tourism": 0, "satisfaction": 5, "ecology": 10,
     "desc": "해양 쓰레기를 줄이고 주민 자긍심을 높입니다."},
    {"name": "쓰레기 매립장 확장", "cost": 15, "tourism": 0, "satisfaction": 10, "ecology": -15,
     "desc": "당장의 처리난은 해결되지만 토양·수질이 나빠집니다."},
    {"name": "해녀문화 체험 관광", "cost": 20, "tourism": 8, "satisfaction": 6, "ecology": 2,
     "desc": "전통문화 기반 관광으로 환경 부담이 적습니다."},
    {"name": "송악산 개발 허가", "cost": 35, "tourism": 20, "satisfaction": -8, "ecology": -20,
     "desc": "큰 수익이 예상되지만 반대 여론과 생태 훼손이 큽니다."},
    {"name": "친환경 숙박 인증제", "cost": 18, "tourism": 4, "satisfaction": 2, "ecology": 6,
     "desc": "숙박업계의 친환경 전환을 유도합니다."},
    {"name": "주민 환경교육 프로그램", "cost": 15, "tourism": 0, "satisfaction": 8, "ecology": 5,
     "desc": "주민들의 환경 의식이 높아집니다."},
    {"name": "양식장 확대", "cost": 25, "tourism": 10, "satisfaction": -5, "ecology": -10,
     "desc": "수산업 소득은 늘지만 해양 오염 위험이 커집니다."},
    {"name": "생태 모니터링 조사단", "cost": 10, "tourism": 0, "satisfaction": 2, "ecology": 5,
     "desc": "데이터 기반 의사결정의 토대를 마련합니다."},
]

EVENTS = [
    {"name": "적조 발생", "condition": lambda s: s["ecology"] < 35, "tourism": -10, "satisfaction": -8, "ecology": -5,
     "msg": "🦠 낮은 생태지표 때문에 적조가 발생해 어업과 관광이 큰 피해를 입었습니다."},
    {"name": "관광 과잉 민원", "condition": lambda s: s["tourism"] > 80, "tourism": -5, "satisfaction": -10, "ecology": -5,
     "msg": "🏖️ 관광객이 너무 많아 주민들의 불만이 커지고 있습니다."},
    {"name": "태풍 피해", "condition": lambda s: True, "tourism": -5, "satisfaction": -3, "ecology": -3,
     "msg": "🌀 태풍이 지나가며 해안가에 쓰레기가 쌓였습니다."},
    {"name": "생태 관광 입소문", "condition": lambda s: s["ecology"] > 65, "tourism": 8, "satisfaction": 5, "ecology": 0,
     "msg": "🐬 깨끗한 생태계가 입소문이 나며 관광객이 늘었습니다."},
]


def init_state():
    if "jeju_turn" not in st.session_state:
        st.session_state.jeju_turn = 1
        st.session_state.jeju_stats = {"tourism": 50, "satisfaction": 50, "ecology": 50}
        st.session_state.jeju_log = []
        st.session_state.jeju_game_over = False
        pool = POLICY_POOL.copy()
        random.shuffle(pool)
        st.session_state.jeju_options = pool[:4]
        st.session_state.jeju_pool = pool[4:]


def clamp(v):
    return max(0, min(100, v))


def apply_choices(selected):
    stats = st.session_state.jeju_stats
    for card in selected:
        stats["tourism"] = clamp(stats["tourism"] + card["tourism"])
        stats["satisfaction"] = clamp(stats["satisfaction"] + card["satisfaction"])
        stats["ecology"] = clamp(stats["ecology"] + card["ecology"])
        st.session_state.jeju_log.append(f"턴 {st.session_state.jeju_turn}: '{card['name']}' 시행")

    triggered = [e for e in EVENTS if e["condition"](stats) and random.random() < 0.5]
    if triggered:
        event = random.choice(triggered)
        stats["tourism"] = clamp(stats["tourism"] + event["tourism"])
        stats["satisfaction"] = clamp(stats["satisfaction"] + event["satisfaction"])
        stats["ecology"] = clamp(stats["ecology"] + event["ecology"])
        st.session_state.jeju_log.append(event["msg"])

    if stats["ecology"] <= 0 or stats["satisfaction"] <= 0:
        st.session_state.jeju_game_over = True
        return

    st.session_state.jeju_turn += 1
    if st.session_state.jeju_turn > TOTAL_TURNS:
        st.session_state.jeju_game_over = True
        return

    if len(st.session_state.jeju_pool) < 4:
        refill = POLICY_POOL.copy()
        random.shuffle(refill)
        st.session_state.jeju_pool = refill
    st.session_state.jeju_options = st.session_state.jeju_pool[:4]
    st.session_state.jeju_pool = st.session_state.jeju_pool[4:]


def ending(stats):
    eco, sat, tour = stats["ecology"], stats["satisfaction"], stats["tourism"]
    if eco <= 0:
        return "💀 생태 붕괴", "곶자왈과 해안 생태계가 회복 불능 상태가 되어 제주의 자연이 무너졌습니다."
    if sat <= 0:
        return "😡 주민 이탈", "주민들의 불만이 극에 달해 마을을 떠나는 사람들이 늘었습니다."
    if eco >= 70 and sat >= 60 and tour >= 50:
        return "🌿 지속가능한 제주", "관광, 주민 삶, 생태계가 균형을 이루며 모범적인 섬으로 거듭났습니다."
    if tour >= 80 and eco < 40:
        return "🏗️ 관광으로 무너진 섬", "수익은 늘었지만 생태계는 회복하기 힘든 상태가 되었습니다."
    if eco >= 60 and tour < 30:
        return "🍃 조용한 보존의 섬", "관광 수익은 적지만 생태계가 잘 보존되었습니다."
    return "⚖️ 균형 잡힌 제주", "완벽하진 않지만 여러 가치 사이에서 무난한 균형을 찾았습니다."


def restart():
    for key in ["jeju_turn", "jeju_stats", "jeju_log", "jeju_game_over", "jeju_pool", "jeju_options"]:
        st.session_state.pop(key, None)


st.markdown("## 🌋 제주 생태계 밸런스 시뮬레이터")

lesson_flow(
    "jeju_balance",
    concept=[
        {"title": "📘 Chapter 1 · 지속가능발전이란?", "body": """
<p style='line-height:1.8'>
<b>지속가능발전(Sustainable Development)</b>은 "<b>미래 세대의 필요를 해치지 않으면서
현재 세대의 필요를 충족하는</b> 발전"을 뜻합니다. 지금 다 써버리는 게 아니라, 다음 세대도
누릴 수 있게 남겨두자는 생각이에요.<br><br>
이를 위해서는 세 가지를 <b>함께</b> 봐야 합니다 — 흔히 <b>지속가능성의 세 기둥</b>이라 불러요.
</p>
<ul style='line-height:1.9; color:var(--text-muted)'>
<li><b>경제 (관광수입):</b> 지역이 먹고살 수 있는가</li>
<li><b>사회 (주민만족도):</b> 사는 사람들이 행복한가</li>
<li><b>환경 (생태지표):</b> 자연이 건강하게 유지되는가</li>
</ul>
"""},
        {"title": "📗 Chapter 2 · 트레이드오프와 제주의 딜레마", "body": """
<p style='line-height:1.8'>
세 기둥은 서로 부딪힐 때가 많습니다. 관광을 늘리면 <b>수입(경제)</b>은 오르지만 쓰레기·혼잡으로
<b>생태·주민 삶</b>이 나빠질 수 있어요. 이렇게 하나를 얻으면 다른 걸 잃는 관계가
<b>트레이드오프</b>입니다.<br><br>
실제 제주도 이 딜레마를 겪고 있어요:
</p>
<ul style='line-height:1.9; color:var(--text-muted)'>
<li><b>과잉관광:</b> 관광객 급증 → 쓰레기·교통난·물 부족 → 주민 불만</li>
<li><b>개발 압력:</b> 리조트·도로 건설 → 곶자왈·해안 훼손</li>
<li><b>인구·물가:</b> 관광 경제가 커지며 주민 삶의 비용 상승</li>
</ul>
"""},
        {"title": "📙 Chapter 3 · 자원은 한정, 정답은 없다", "body": """
<p style='line-height:1.8'>
정책을 펼치려면 <b>예산(자원)이 필요</b>하고, 자원은 늘 부족합니다. 그래서
"무엇을 <b>먼저</b> 할지" 우선순위를 정해야 해요. 모든 지표를 동시에 100점 만드는 마법은 없습니다.<br><br>
그래서 이 게임엔 <b>정답이 없습니다</b>. 관광 중심의 섬, 보존 중심의 섬, 균형 잡힌 섬 —
어떤 결말이든 당신의 <b>가치 선택</b>이 만든 결과예요. 중요한 건 "왜 그렇게 선택했는지"
설명할 수 있는 것입니다.
</p>
<p style='color:var(--text-caption); font-size:.85rem'>🎯 문제: 촌장이 되어 6턴 동안 어떤 정책으로 세 축의 균형을 잡을 것인가?</p>
"""},
    ],
    discuss=[
        "당신은 무엇을 위해 무엇을 포기했나요? 그 선택이 옳았나요?",
        "관광수입만 극대화하면 어떤 일이 벌어질까요? (실제 과잉관광 사례)",
        "현실의 제주가 겪는 개발 vs 보전 딜레마는 무엇이 있을까요?",
        "'지속가능한 균형'이란 모두를 100점 만드는 것일까요, 아니면 다른 무엇일까요?",
    ],
    present="""
<div class='eco-card'>
<b style='color:var(--accent-primary)'>🎤 발표: 우리 촌장의 정책 철학</b>
<ul style='color:var(--text-muted); line-height:1.8'>
<li>우리가 <b>우선한 가치</b>와 그 이유</li>
<li>가장 어려웠던 <b>트레이드오프</b> 결정</li>
<li>최종 결말(엔딩)과, 다시 한다면 바꿀 정책</li>
</ul>
</div>
""",
)

st.markdown("""
<div class='hero-banner'>
  <div class='hero-title'>🏝️ 촌장이 되어보세요</div>
  <div class='hero-sub'>
  정답은 없습니다. 한쪽을 챙기면 다른 쪽이 흔들리는 트레이드오프 속에서 당신만의 균형을 찾아보세요.
  </div>
</div>
""", unsafe_allow_html=True)

init_state()
stats = st.session_state.jeju_stats

if not st.session_state.jeju_game_over:
    st.markdown(f"### 턴 {st.session_state.jeju_turn} / {TOTAL_TURNS}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🏖️ **관광수입**")
        st.progress(stats["tourism"] / 100)
        st.caption(f"{stats['tourism']} / 100")
    with col2:
        st.markdown("😊 **주민만족도**")
        st.progress(stats["satisfaction"] / 100)
        st.caption(f"{stats['satisfaction']} / 100")
    with col3:
        st.markdown("🌱 **생태지표**")
        st.progress(stats["ecology"] / 100)
        st.caption(f"{stats['ecology']} / 100")

    budget = START_BUDGET_BASE + stats["tourism"] // 2
    st.markdown(f"""
    <div class='res-bar'>
      <div class='res-chip'>💰 이번 턴 예산 <span class='val'>{budget}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 정책 카드를 선택하세요 (예산 내에서 자유롭게)")
    selected_idx = []
    total_cost = 0
    for i, card in enumerate(st.session_state.jeju_options):
        st.markdown(
            f"""
            <div class="eco-card">
            <b style='color:var(--accent-primary);'>{card['name']}</b> (비용 {card['cost']})<br>
            <span style="color:var(--text-muted); font-size:.9rem;">{card['desc']}</span><br>
            <span style="color:var(--text-caption); font-size:.82rem;">관광 {card['tourism']:+d} · 만족도 {card['satisfaction']:+d} · 생태 {card['ecology']:+d}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.checkbox(f"'{card['name']}' 선택", key=f"jeju_chk_{st.session_state.jeju_turn}_{i}"):
            selected_idx.append(i)
            total_cost += card["cost"]

    if total_cost > budget:
        st.error(f"예산 초과! 선택한 비용 {total_cost} > 예산 {budget}. 일부를 해제하세요.")
    else:
        st.markdown(f"선택한 비용: {total_cost} / {budget}")

    if st.button("이번 턴 확정", disabled=(total_cost > budget)):
        chosen = [st.session_state.jeju_options[i] for i in selected_idx]
        apply_choices(chosen)
        st.rerun()

    if st.session_state.jeju_log:
        with st.expander("지난 턴 기록 보기"):
            for entry in reversed(st.session_state.jeju_log):
                st.write("- " + entry)

else:
    title, desc = ending(stats)
    st.markdown(
        f"""
        <div class="eco-card" style="text-align:center; border-color:var(--accent-primary);">
        <h2 style="color:var(--accent-primary);">{title}</h2>
        <p style="color:var(--text-muted);">{desc}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🏖️ **관광수입**")
        st.progress(stats["tourism"] / 100)
        st.caption(f"{stats['tourism']} / 100")
    with col2:
        st.markdown("😊 **주민만족도**")
        st.progress(stats["satisfaction"] / 100)
        st.caption(f"{stats['satisfaction']} / 100")
    with col3:
        st.markdown("🌱 **생태지표**")
        st.progress(stats["ecology"] / 100)
        st.caption(f"{stats['ecology']} / 100")

    with st.expander("전체 정책 기록"):
        for entry in st.session_state.jeju_log:
            st.write("- " + entry)

    if st.button("다시 시작하기"):
        restart()
        st.rerun()
