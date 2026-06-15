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
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

    /* ══ CSS 변수 — 다크 모드 (기본) ══ */
    :root {
        --bg-base:        #0a0f0d;
        --bg-sidebar:     #0d1a14;
        --bg-card:        #0d1f17;
        --bg-metric:      #0d2418;
        --bg-select:      #0d2418;
        --bg-hero:        linear-gradient(135deg,#003d1f 0%,#00251a 50%,#001a12 100%);
        --bg-node-badge:  #003d1f;
        --bg-node-visited:#1b5e20;
        --border-main:    #1b3a2a;
        --border-sidebar: #1e3a2a;
        --border-metric:  #1b5e3b;
        --border-select:  #1b5e3b;
        --border-badge:   #00897b;
        --text-base:      #e8f5e9;
        --text-sidebar:   #b2dfdb;
        --text-muted:     #80cbc4;
        --text-caption:   #4db6ac;
        --text-footer:    #2e5945;
        --accent-primary: #69f0ae;
        --accent-second:  #40c4aa;
        --accent-third:   #1de9b6;
        --hero-glow:      #1de9b622;
    }

    /* ══ CSS 변수 — 라이트 모드 ══ */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-base:        #f0faf4;
            --bg-sidebar:     #e6f4ec;
            --bg-card:        #ffffff;
            --bg-metric:      #e8f5e9;
            --bg-select:      #ffffff;
            --bg-hero:        linear-gradient(135deg,#c8f0d8 0%,#e0f7ec 50%,#f0fdf6 100%);
            --bg-node-badge:  #e8f5e9;
            --bg-node-visited:#c8e6c9;
            --border-main:    #a5d6b0;
            --border-sidebar: #b2dfbd;
            --border-metric:  #66bb8a;
            --border-select:  #66bb8a;
            --border-badge:   #00897b;
            --text-base:      #1b3a2a;
            --text-sidebar:   #2e6b4f;
            --text-muted:     #2e7d52;
            --text-caption:   #00796b;
            --text-footer:    #4caf7d;
            --accent-primary: #00897b;
            --accent-second:  #00796b;
            --accent-third:   #00bfa5;
            --hero-glow:      #00bfa522;
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
        background: linear-gradient(135deg, #00897b, var(--accent-third)) !important;
        color: #001a12 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.4rem !important;
        transition: transform .15s, box-shadow .15s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px #00bfa544;
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
    .stProgress > div > div { background: linear-gradient(90deg,#00897b,var(--accent-primary)) !important; }

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
