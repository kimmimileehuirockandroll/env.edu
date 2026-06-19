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
        --bg-metric:      #1F0D14;
        --bg-select:      #1A1A1A;
        --bg-hero:        linear-gradient(135deg, #1F0D14 0%, #0D0D0D 60%, #001A14 100%);
        --bg-node-badge:  #1F0D14;
        --bg-node-visited:#2E0A1A;
        --border-main:    #2A2A2A;
        --border-sidebar: #222222;
        --border-metric:  #4D1A2E;
        --border-select:  #4D1A2E;
        --border-badge:   #FF5C8A;
        --text-base:      #F0F0F0;
        --text-sidebar:   #CCCCCC;
        --text-muted:     #9B9B9B;
        --text-caption:   #777777;
        --text-footer:    #444444;
        --accent-primary: #FF5C8A;
        --accent-second:  #00E8C1;
        --accent-third:   #FF85A1;
        --hero-glow:      #FF2D6B22;
    }
    
    /* ══ 라이트 모드 ══ */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-base:        #FFFFFF;
            --bg-sidebar:     #F5F5F5;
            --bg-card:        #FAFAFA;
            --bg-metric:      #FFF0F5;
            --bg-select:      #FFFFFF;
            --bg-hero:        linear-gradient(135deg, #FFE4EE 0%, #F0FBF8 60%, #FFFFFF 100%);
            --bg-node-badge:  #FFF0F5;
            --bg-node-visited:#FFD6E7;
            --border-main:    #E8E8E8;
            --border-sidebar: #E0E0E0;
            --border-metric:  #FFBED5;
            --border-select:  #FFBED5;
            --border-badge:   #FF2D6B;
            --text-base:      #1A1A1A;
            --text-sidebar:   #333333;
            --text-muted:     #6B6B6B;
            --text-caption:   #9B9B9B;
            --text-footer:    #BBBBBB;
            --accent-primary: #FF2D6B;
            --accent-second:  #00C9A7;
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
    h3 { color: var(--text-muted)     !important; }

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
        background: linear-gradient(135deg, #FF2D6B, #FF85A1) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.4rem !important;
        transition: transform .15s, box-shadow .15s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px #FF2D6B44;
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
    .stProgress > div > div {    background: linear-gradient(90deg, #FF2D6B, #00C9A7) !important;}

    /* ── divider ── */
    hr { border-color: var(--border-main) !important; }

    /* ── info / warning / success boxes ── */
    .stAlert { border-radius: 10px !important; }

    /* ── hero banner ── */
    .hero-banner {
        background: var(--bg-hero);
        border: 1px solid var(--hero-glow);
        border-radius: 20px;
        padding: 2.5rem 2.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, var(--hero-glow) 0%, transparent 70%);
        border-radius: 50%;
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
        border-left: 4px solid #00897b;
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
