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
#  LEARNER LEVEL (학습자 레벨 / 대상 토글) — 복수 선택(중복 가능)
#  설문 척도(15문항)는 데이터 일관성을 위해 건드리지 않고,
#  교육용 콘텐츠·용어·이론 노출만 레벨로 분기한다.
#
#  사용법:
#    - 콘텐츠 항목에 levels 태그를 달고 item_visible(levels)로 표시 여부 판단.
#      예) item_visible(["초등", "중등"])  →  초등/중등 선택 시(또는 전체) True
#    - 학술 이론 라벨은 show_theory()로 분기(고등·대학/성인 또는 전체에서만).
# ─────────────────────────────────────────────
LEVELS = ["전체", "대학·성인", "고등", "중등", "초등"]
LEVEL_LABELS = {
    "전체":     "전체",
    "대학·성인": "대학생·성인",
    "고등":     "고등학생",
    "중등":     "중학생",
    "초등":     "초등학생",
}
# 콘텐츠 태그용(전체 제외) — 항목 levels에 쓰는 실제 대상 키
CONTENT_LEVELS = ["대학·성인", "고등", "중등", "초등"]
DEFAULT_LEVELS = ["전체"]
THEORY_LEVELS = {"전체", "고등", "대학·성인"}  # 학술 이론 라벨을 노출할 레벨


def level_selector():
    """사이드바 등에서 호출 — 복수 선택 가능한 학습자 레벨 선택기."""
    return st.multiselect(
        "🎚️ 학습자 레벨 (복수 선택 가능)",
        options=LEVELS,
        default=st.session_state.get("learner_levels", DEFAULT_LEVELS),
        format_func=lambda k: LEVEL_LABELS.get(k, k),
        key="learner_levels",
    )


def selected_levels():
    """현재 선택된 레벨 리스트. 비어 있으면 '전체'로 간주."""
    sel = st.session_state.get("learner_levels", DEFAULT_LEVELS)
    return sel if sel else DEFAULT_LEVELS


def is_all_selected():
    """'전체'가 선택되어 모든 레벨 콘텐츠를 보여줘야 하는 상태인지."""
    return "전체" in selected_levels()


def item_visible(item_levels=None):
    """콘텐츠 항목을 현재 선택 레벨에서 보여줄지 여부.

    item_levels: 이 항목이 해당하는 레벨 리스트(중복 가능). None/빈 값이면 항상 표시.
    """
    if is_all_selected():
        return True
    if not item_levels:            # 레벨 태그 없는 공통 항목은 항상 표시
        return True
    if "전체" in item_levels:
        return True
    return bool(set(selected_levels()) & set(item_levels))


def filter_items(items, level_key="levels"):
    """딕셔너리 리스트를 현재 선택 레벨에 맞게 필터링해서 반환."""
    return [it for it in items if item_visible(it.get(level_key))]


def show_theory():
    """학술 이론 라벨/개념을 노출할지 여부 (전체·고등·대학/성인 선택 시 True)."""
    return bool(set(selected_levels()) & THEORY_LEVELS)

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
