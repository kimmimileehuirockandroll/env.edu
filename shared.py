import streamlit as st
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
import numpy as np
import random
import math
import json
from datetime import datetime


# ─────────────────────────────────────────────
#  GLOBAL CSS  (system-adaptive light/dark + green/mint theme)
# ─────────────────────────────────────────────
def apply_css():
    """전역 CSS 적용 — 각 페이지 맨 위에서 호출"""
    
    st.markdown("""
    <style>
    [data-testid="stToolbarActions"],
    [data-testid="stMainMenu"],
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stDecoration"] {display: none !important;}
    footer {display: none !important;}
    [data-testid="stHeader"],
    .stAppHeader {
        background: transparent !important;
        box-shadow: none !important;}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

    /* ══ CSS 변수 — 다크 모드 (기본) ══ */
    /* ══ 다크 모드 (기본) ══ */
    :root {
        --bg-base:        #0D0D0D;
        --bg-sidebar:     #111111;
        --bg-card:        #1A1A1A;
        --bg-metric:      #1A1A1A;
        --bg-select:      #1A1A1A;
        --bg-hero:        linear-gradient(135deg, #1F0D14 0%, #0D0D0D 60%, #1F0D14 100%);
        --bg-node-badge:  #1F0D14;
        --bg-node-visited:#2E0A1A;
        --border-main:    #2A2A2A;
        --border-sidebar: #222222;
        --border-metric:  #2A2A2A;
        --border-select:  #4D1A2E;
        --border-badge:   #FF5C8A;
        --text-base:      #F0F0F0;
        --text-sidebar:   #CCCCCC;
        --text-muted:     #9B9B9B;
        --text-caption:   #777777;
        --text-footer:    #444444;
        --accent-primary: #FF5C8A;
        --accent-second:  #F0F0F0;
        --accent-third:   #FF85A1;
        --hero-glow:      #FF2D6B22;
    }
    
    /* ══ 라이트 모드 ══ */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-base:        #FFFFFF;
            --bg-sidebar:     #F5F5F5;
            --bg-card:        #FAFAFA;
            --bg-metric:      #F5F5F5;
            --bg-select:      #FFFFFF;
            --bg-hero:        linear-gradient(135deg, #FFE4EE 0%, #FFF0F5 60%, #FFFFFF 100%);
            --bg-node-badge:  #FFF0F5;
            --bg-node-visited:#FFD6E7;
            --border-main:    #E8E8E8;
            --border-sidebar: #E0E0E0;
            --border-metric:  #E0E0E0;
            --border-select:  #FFBED5;
            --border-badge:   #FF2D6B;
            --text-base:      #1A1A1A;
            --text-sidebar:   #333333;
            --text-muted:     #6B6B6B;
            --text-caption:   #9B9B9B;
            --text-footer:    #BBBBBB;
            --accent-primary: #FF2D6B;
            --accent-second:  #1A1A1A;
            --accent-third:   #FF6B9D;
            --hero-glow:      #FF2D6B18;
        }
    }
    /* ── reset & base ── */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', 'Space Grotesk', sans-serif;
    }
    .stApp {
        background: var(--bg-base) !important;
        color: var(--text-base) !important;
    }

    /* ── sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-sidebar);
    }
    [data-testid="stSidebar"] * { color: var(--text-sidebar) !important; }
    [data-testid="stSidebar"] .stRadio label { font-size: 1rem; }

    /* ── headings ── */
    h1 { color: var(--accent-primary) !important; letter-spacing: -1px; }
    h2 { color: var(--accent-second)  !important; }
    h3 { color: var(--text-base)     !important; }

    /* ── metric cards ── */
    [data-testid="stMetric"] {
        background: var(--bg-metric);
        border: 1px solid var(--border-metric);
        border-radius: 12px;
        padding: 12px 18px;
    }
    [data-testid="stMetricValue"] { color: var(--accent-primary) !important; font-size: 1.6rem !important; }
    [data-testid="stMetricLabel"] { color: var(--text-muted) !important; }
    [data-testid="stMetricDelta"]  { font-size: .85rem !important; }

    /* ── buttons ── */
    .stButton > button {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F0F0 100%) !important;
        color: var(--text-base) !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow:
            0 1px 0 rgba(255,255,255,0.9) inset,
            0 4px 12px rgba(0,0,0,0.10),
            0 1px 3px rgba(0,0,0,0.08) !important;
        transition: all .2s;
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #FFFFFF 0%, #E8E8E8 100%) !important;
        color: var(--accent-primary) !important;
        box-shadow:
            0 1px 0 rgba(255,255,255,0.9) inset,
            0 6px 20px rgba(255,45,107,0.12),
            0 2px 6px rgba(0,0,0,0.08) !important;
        transform: translateY(-2px);
    }
        /* ── selectbox / radio ── */
        .stSelectbox label, .stRadio label { color: var(--text-sidebar) !important; font-size: .93rem; }
        div[data-baseweb="select"] > div {
            background: var(--bg-select) !important;
            border: 1px solid var(--border-select) !important;
            color: var(--text-base) !important;
            border-radius: 8px !important;
        }
            
    /* ── progress bar ── */
    div[role="progressbar"] {
        background: rgba(255, 45, 107, 0.12) !important;
        border-radius: 99px !important;
        height: 6px !important;
        border: none !important;
        overflow: hidden !important;
    }
    div[role="progressbar"] > div {
        background: #FF2D6B !important;
        border-radius: 99px !important;
        height: 6px !important;
        transition: width 0.4s ease !important;
    }
    [data-testid="stProgressBar"] > div {
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #FF2D6B, #FF85A1) !important;
    }
    /* ── divider ── */
    hr { border-color: var(--border-main) !important; }

    /* ── info / warning / success boxes ── */
    .stAlert { border-radius: 10px !important; }

    /* ── hero banner ── */
    .hero-banner {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0 0 1.5rem 0;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        display: none;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 900;
        color: var(--accent-primary);
        margin: 0 0 .4rem;
        line-height: 1.15;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: var(--text-muted);
        margin: 0;
    }

    /* ── game resource bar ── */
    .res-bar { display: flex; gap: 12px; flex-wrap: wrap; margin: 1rem 0; }
    .res-chip {
        background: var(--bg-metric);
        border: 1px solid var(--border-metric);
        border-radius: 50px;
        padding: 6px 18px;
        font-size: .9rem;
        color: var(--text-sidebar);
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .res-chip .val { color: var(--accent-primary); font-weight: 700; }

    /* ── card ── */
    .eco-card {
        background: var(--bg-card);
        border: 1px solid var(--border-main);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    /* ── node badge ── */
    .node-badge {
        display: inline-block;
        background: var(--bg-node-badge);
        border: 1px solid var(--border-badge);
        color: var(--accent-primary);
        border-radius: 8px;
        padding: 3px 10px;
        font-size: .82rem;
        margin: 2px;
    }
    .node-badge.visited {
        background: var(--bg-node-visited);
        border-color: var(--accent-primary);
    }

    /* ── survey question card ── */
    .q-card {
        background: var(--bg-card);
        border-left: 4px solid var(--accent-primary);
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .q-theory { font-size: .75rem; color: var(--text-caption); margin-bottom: 4px; }
    .q-text   { font-size: 1rem;   color: var(--text-base); }

    /* ── footer ── */
    .eco-footer {
        text-align: center;
        color: var(--text-footer);
        font-size: .8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border-main);
    }
    /* ── Sidebar Brand Link ── */
    .brand-link {
        text-decoration: none !important;
        display: block;
        margin-bottom: 0.4rem;
    }
    
    .brand-title {
        color: var(--accent-primary) !important;
        font-size: 1.45rem !important;
        font-weight: 850 !important;
        line-height: 1.25;
    }
    
    .brand-subtitle {
        color: var(--text-muted) !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin-top: 0.15rem;
    }
    /* ── metric delta 색상 ── */
    [data-testid="stMetricDelta"] svg { display: none !important; }
    [data-testid="stMetricDelta"] > div {
        color: #6B6B6B !important;
        font-size: .85rem !important;
    }

    /* ─────────────────────────────────────────────
       학습자 레벨 선택 (pills / radio 공통)
       ───────────────────────────────────────────── */
    /* 라벨 */
    [data-testid="stPills"] label,
    div[role="radiogroup"] > label:first-child {
        font-size: .82rem !important;
        font-weight: 700 !important;
        color: var(--text-sidebar) !important;
        margin-bottom: .4rem !important;
    }

    /* ── pills(알약 버튼) — 간격 + 비선택 스타일 ── */
    [data-testid="stPills"] [data-testid="stPillsContainer"],
    [data-testid="stPills"] div:has(> button) {
        gap: 6px !important;
        flex-wrap: wrap !important;
    }
    [data-testid="stPills"] button {
        border: 1.5px solid var(--border-select) !important;
        background: var(--bg-select) !important;
        color: var(--text-sidebar) !important;
        font-size: .85rem !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,.06) !important;
        transition: all .15s ease !important;
    }
    [data-testid="stPills"] button:hover {
        border-color: var(--accent-primary) !important;
        color: var(--accent-primary) !important;
        transform: translateY(-1px);
    }
    /* 선택된 알약 */
    [data-testid="stPills"] button[aria-checked="true"],
    [data-testid="stPills"] button[kind="pillsActive"],
    button[data-testid="stBaseButton-pillsActive"] {
        background: linear-gradient(180deg, var(--accent-primary), var(--accent-third)) !important;
        border-color: var(--accent-primary) !important;
        color: #FFFFFF !important;
        box-shadow: 0 3px 10px rgba(255,45,107,.30) !important;
    }
    [data-testid="stPills"] button[aria-checked="true"] *,
    button[data-testid="stBaseButton-pillsActive"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stPills"] button[aria-checked="true"]:hover,
    button[data-testid="stBaseButton-pillsActive"]:hover {
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }

    /* ── radio 폴백도 동일한 알약 스타일로 ── */
    div[role="radiogroup"] {
        gap: 6px !important;
        flex-wrap: wrap !important;
    }
    div[role="radiogroup"] > label {
        border-radius: 999px !important;
        border: 1.5px solid var(--border-select) !important;
        background: var(--bg-select) !important;
        padding: .35rem .9rem !important;
        margin: 0 !important;
        font-size: .85rem !important;
        cursor: pointer;
        transition: all .15s ease !important;
    }
    div[role="radiogroup"] > label:hover {
        border-color: var(--accent-primary) !important;
    }
    div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(180deg, var(--accent-primary), var(--accent-third)) !important;
        border-color: var(--accent-primary) !important;
        box-shadow: 0 3px 10px rgba(255,45,107,.30) !important;
    }
    div[role="radiogroup"] > label:has(input:checked) * {
        color: #FFFFFF !important;
    }
    /* 라디오 동그라미 숨기기(알약만 보이게) */
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  KOREAN FONT LOADER (공용)
# ─────────────────────────────────────────────
import os
import matplotlib.font_manager as fm

def load_korean_font(size=8.5):
    """나눔고딕 폰트를 찾아 FontProperties로 반환. 없으면 None."""
    candidates = [
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "C:/Windows/Fonts/malgun.ttf",
    ]
    # fm 캐시에서도 검색
    for f in fm.fontManager.ttflist:
        if any(k in f.name for k in ["Nanum", "Gothic", "Malgun", "Noto Sans CJK"]):
            candidates.insert(0, f.fname)
    for p in candidates:
        if p and os.path.exists(p):
            try:
                return fm.FontProperties(fname=p, size=size)
            except Exception:
                continue
    return None

_korean_font = load_korean_font(8.5)

# ─────────────────────────────────────────────
#  LEARNER LEVEL (학습자 레벨 / 대상 토글) — 단일 선택
#  선택한 레벨에 맞는 게임/페이지만 사이드바에 노출한다.
#  (게임 한 개가 여러 레벨에 속할 수 있음 → 각 페이지에 levels 태그를 단다)
#  '전체' 선택 시 모든 페이지 표시.
#
#  사용법:
#    - 페이지 표시 분기: page_visible(["고등", "대학·성인"])
#    - 학술 이론 라벨 분기: show_theory()  (전체·고등·대학/성인에서만 True)
# ─────────────────────────────────────────────
LEVELS = ["전체", "대학·성인", "고등", "중등", "초등"]
LEVEL_LABELS = {
    "전체":     "전체",
    "대학·성인": "대학생·성인",
    "고등":     "고등학생",
    "중등":     "중학생",
    "초등":     "초등학생",
}
# 페이지 태그용(전체 제외) — 각 페이지 levels에 쓰는 실제 대상 키
CONTENT_LEVELS = ["대학·성인", "고등", "중등", "초등"]
DEFAULT_LEVEL = "전체"
THEORY_LEVELS = {"전체", "고등", "대학·성인"}  # 학술 이론 라벨을 노출할 레벨


def level_selector():
    """사이드바 등에서 호출 — 단일 선택 알약형 학습자 레벨 선택기."""
    # 세션값을 먼저 시드(이후 위젯은 key로만 연결 → default/key 충돌 방지)
    if "learner_level" not in st.session_state:
        st.session_state["learner_level"] = DEFAULT_LEVEL
    # pills: 각 항목이 독립된 알약으로 렌더링됨(가장 깔끔)
    if hasattr(st, "pills"):
        sel = st.pills(
            "🎚️ 학습자 레벨",
            options=LEVELS,
            selection_mode="single",
            format_func=lambda k: LEVEL_LABELS.get(k, k),
            key="learner_level",
        )
        # 선택 해제(None) 방지 — 비면 직전/기본값 유지
        return sel or DEFAULT_LEVEL
    # 폴백: 가로 라디오
    return st.radio(
        "🎚️ 학습자 레벨",
        options=LEVELS,
        format_func=lambda k: LEVEL_LABELS.get(k, k),
        horizontal=True,
        key="learner_level",
    )


def current_level():
    """현재 선택된 레벨 키. 비어 있으면 '전체'."""
    return st.session_state.get("learner_level") or DEFAULT_LEVEL


def is_all_selected():
    """'전체'가 선택된 상태인지."""
    return current_level() == "전체"


def page_visible(page_levels=None):
    """현재 선택 레벨에서 이 페이지를 보여줄지 여부.

    page_levels: 이 페이지가 해당하는 레벨 리스트(중복 가능). None/빈 값이면 항상 표시.
    """
    if is_all_selected():
        return True
    if not page_levels:            # 레벨 태그 없는 공통 페이지는 항상 표시
        return True
    if "전체" in page_levels:
        return True
    return current_level() in page_levels


# 콘텐츠 항목 분기에도 같은 규칙을 쓰고 싶을 때를 위한 별칭
def item_visible(item_levels=None):
    """콘텐츠 항목 표시 여부 — page_visible과 동일 규칙."""
    return page_visible(item_levels)


def filter_items(items, level_key="levels"):
    """딕셔너리 리스트를 현재 선택 레벨에 맞게 필터링해서 반환."""
    return [it for it in items if page_visible(it.get(level_key))]


def show_theory():
    """학술 이론 라벨/개념을 노출할지 여부 (전체·고등·대학/성인 선택 시 True)."""
    return current_level() in THEORY_LEVELS


# ─────────────────────────────────────────────
#  LESSON FLOW (개념 설명 → 실습 → 토론 → 발표)
#  각 게임 페이지 상단에서 lesson_flow(...)를 호출하면
#  단계 버튼이 그려지고, '실습'이 아닌 단계에서는 해당 콘텐츠를 렌더 후 st.stop().
#  '실습' 단계에서는 함수가 그냥 반환되어 아래의 게임 코드가 실행됨.
# ─────────────────────────────────────────────
LESSON_STEPS = ["📖 개념 설명", "🎮 실습", "💬 토론", "🎤 발표"]


def lesson_flow(key, concept, discuss, present, default_step=0):
    """수업 4단계 네비게이션.

    concept: 챕터 리스트 [{"title": "Chapter 1 · ...", "body": "<html>"}, ...]
             (호환용으로 문자열 하나를 줘도 단일 카드로 표시)
    discuss: 질문 리스트, present: HTML 문자열.
    """
    sk = f"lesson_{key}"
    if sk not in st.session_state:
        st.session_state[sk] = LESSON_STEPS[default_step]
    st.radio("수업 단계", LESSON_STEPS, key=sk, horizontal=True, label_visibility="collapsed")
    st.markdown("---")
    i = LESSON_STEPS.index(st.session_state[sk])
    if i == 0:
        st.markdown("### 📖 개념 설명 · 문제 제시")
        st.caption("아래 챕터를 펼쳐 개념을 충분히 익힌 뒤 실습으로 넘어가세요.")
        if isinstance(concept, str):
            st.markdown(concept, unsafe_allow_html=True)
        else:
            for idx, ch in enumerate(concept):
                with st.expander(ch["title"], expanded=(idx == 0)):
                    st.markdown(ch["body"], unsafe_allow_html=True)
        st.info("개념을 이해했다면 위의 **🎮 실습** 버튼을 눌러 직접 해보세요.")
        st.stop()
    elif i == 2:
        st.markdown("### 💬 토론하기")
        st.caption("정답을 맞히는 게 아니라, 생각을 꺼내고 서로 부딪혀보세요.")
        for q in discuss:
            st.markdown(f"<div class='eco-card'>❓ {q}</div>", unsafe_allow_html=True)
        st.stop()
    elif i == 3:
        st.markdown("### 🎤 발표 · 산출물")
        st.markdown(present, unsafe_allow_html=True)
        st.stop()
    # i == 1 (실습) → 반환하여 아래 게임 코드 실행

# ─────────────────────────────────────────────
#  CHART COLOR PALETTE (matplotlib용)
#  색상 변경 시 여기만 수정하면 모든 페이지 차트에 반영됨
# ─────────────────────────────────────────────
def get_chart_colors():
    """현재 Streamlit 테마에 맞는 matplotlib 색상 딕셔너리 반환."""
    is_dark = st.get_option("theme.base") == "dark"

    if is_dark:
        return {
            "bg":       "#0D0D0D",
            "card":     "#1A1A1A",
            "text":     "#F0F0F0",
            "muted":    "#9B9B9B",
            "caption":  "#777777",
            "tick":     "#9B9B9B",
            "axis":     "#9B9B9B",
            "spine":    "#2A2A2A",
            "accent":   "#FF5C8A",
            "accent2":  "#FF85A1",
            "label":    "#F0F0F0",
        }
    else:
        return {
            "bg":       "#FFFFFF",
            "card":     "#FAFAFA",
            "text":     "#1A1A1A",
            "muted":    "#6B6B6B",
            "caption":  "#9B9B9B",
            "tick":     "#6B6B6B",
            "axis":     "#6B6B6B",
            "spine":    "#E8E8E8",
            "accent":   "#FF2D6B",
            "accent2":  "#FF6B9D",
            "label":    "#1A1A1A",
        }
