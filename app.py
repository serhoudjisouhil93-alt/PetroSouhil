import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
from scipy.interpolate import griddata, RBFInterpolator
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io

# ═══════════════════════════════════════════════════════════════
#  APP CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PetroStream Ultra 2.0",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
#  MASTER CSS — Petroleum Dark Luxury Theme
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&family=Barlow+Condensed:wght@200;300;400;500;600;700;800&display=swap');

:root {
    --bg-void:       #04080f;
    --bg-deep:       #080e1a;
    --bg-panel:      #0c1424;
    --bg-card:       #101828;
    --bg-raised:     #151e2e;
    --gold-bright:   #f0c040;
    --gold-mid:      #c8982a;
    --gold-dim:      #8a6510;
    --amber:         #ff8c00;
    --amber-dim:     #8a4a00;
    --teal:          #00d4aa;
    --teal-dim:      #005a46;
    --red-warn:      #ff4444;
    --blue-data:     #4499ff;
    --text-primary:  #e8eaf0;
    --text-secondary:#8a9ab5;
    --text-muted:    #3d4f6a;
    --border-subtle: #1a2540;
    --border-active: #2a3f60;
    --glow-gold:     0 0 20px rgba(240,192,64,0.3);
    --glow-teal:     0 0 20px rgba(0,212,170,0.3);
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: var(--bg-void) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    color: var(--text-primary) !important;
}

/* ── Animated grain overlay ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    opacity: 0.4;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060b14 0%, #04080f 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.8) !important;
}

section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ── Sidebar logo block ── */
.sidebar-logo {
    background: linear-gradient(135deg, #0a1520 0%, #0d1a2a 100%);
    border-bottom: 1px solid var(--gold-dim);
    padding: 24px 20px 20px;
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
}
.sidebar-logo::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -20px;
    width: 120px;
    height: 200%;
    background: linear-gradient(90deg, transparent, rgba(240,192,64,0.04), transparent);
    transform: skewX(-15deg);
    animation: shimmer 4s infinite;
}
@keyframes shimmer {
    0%   { right: -20px; opacity: 0; }
    50%  { opacity: 1; }
    100% { right: 110%; opacity: 0; }
}
.logo-title {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    letter-spacing: 0.15em;
    color: var(--gold-bright);
    text-transform: uppercase;
    line-height: 1.2;
    text-shadow: var(--glow-gold);
}
.logo-version {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--teal);
    letter-spacing: 0.25em;
    margin-top: 4px;
}
.logo-author {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 8px;
    letter-spacing: 0.08em;
    font-weight: 300;
}

/* ── Nav radio ── */
div[data-testid="stRadio"] > label {
    display: none !important;
}
div[data-testid="stRadio"] > div {
    gap: 2px !important;
}
div[data-testid="stRadio"] > div > label {
    background: transparent !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 10px 16px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    color: var(--text-secondary) !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    border-left: 2px solid transparent !important;
}
div[data-testid="stRadio"] > div > label:hover {
    background: rgba(240,192,64,0.06) !important;
    color: var(--text-primary) !important;
    border-left-color: var(--gold-dim) !important;
}
div[data-testid="stRadio"] > div > label[data-checked="true"],
div[data-testid="stRadio"] > div > label[aria-checked="true"] {
    background: linear-gradient(90deg, rgba(240,192,64,0.12), transparent) !important;
    color: var(--gold-bright) !important;
    border-left-color: var(--gold-bright) !important;
    font-weight: 600 !important;
}

/* ── Main content ── */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1600px !important;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: flex-end;
    gap: 20px;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-subtle);
    position: relative;
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 80px;
    height: 2px;
    background: var(--gold-bright);
    box-shadow: var(--glow-gold);
}
.page-title {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 2.2rem;
    letter-spacing: 0.12em;
    color: var(--text-primary);
    text-transform: uppercase;
    line-height: 1;
}
.page-subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 4px;
    font-weight: 300;
}

/* ── KPI Cards ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-raised)) !important;
    border: 1px solid var(--border-subtle) !important;
    border-top: 2px solid var(--gold-mid) !important;
    border-radius: 6px !important;
    padding: 18px 20px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6), var(--glow-gold) !important;
}
div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 60px; height: 60px;
    background: radial-gradient(circle at top right, rgba(240,192,64,0.08), transparent 70%);
}
[data-testid="stMetricValue"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--gold-bright) !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
}

/* ── Section header ── */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.section-header::before {
    content: '';
    width: 4px;
    height: 16px;
    background: var(--gold-bright);
    border-radius: 2px;
    box-shadow: var(--glow-gold);
}

/* ── Data table ── */
.stDataFrame {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}
.stDataFrame thead th {
    background: var(--bg-deep) !important;
    color: var(--gold-mid) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-active) !important;
    padding: 10px 14px !important;
}
.stDataFrame tbody tr { border-bottom: 1px solid var(--border-subtle) !important; }
.stDataFrame tbody tr:hover { background: rgba(240,192,64,0.04) !important; }
.stDataFrame tbody td {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
    color: var(--text-primary) !important;
    padding: 8px 14px !important;
}

/* ── Info/warning boxes ── */
div[data-testid="stInfo"], .stAlert {
    background: rgba(0,212,170,0.06) !important;
    border: 1px solid var(--teal-dim) !important;
    border-left: 3px solid var(--teal) !important;
    border-radius: 4px !important;
    color: var(--text-primary) !important;
}

/* ── Plotly charts container ── */
.js-plotly-plot { border-radius: 6px; }

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--gold-dim), var(--gold-mid)) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
    padding: 8px 18px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, var(--gold-mid), var(--gold-bright)) !important;
    box-shadow: var(--glow-gold) !important;
    transform: translateY(-1px) !important;
}

/* ── Select boxes, sliders ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-active) !important;
    border-radius: 4px !important;
    color: var(--text-primary) !important;
}
.stSlider > div > div > div { background: var(--gold-mid) !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 4px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.08em !important;
}

/* ── Status badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-family: 'Share Tech Mono', monospace;
}
.badge-active  { background: rgba(0,212,170,0.12); color: var(--teal); border: 1px solid var(--teal-dim); }
.badge-warn    { background: rgba(255,140,0,0.12);  color: var(--amber); border: 1px solid var(--amber-dim); }
.badge-danger  { background: rgba(255,68,68,0.12);  color: var(--red-warn); border: 1px solid #5a1a1a; }

/* ── Maturity indicator ── */
.maturity-bar-wrap { margin: 6px 0; }
.maturity-bar {
    height: 6px;
    border-radius: 3px;
    background: var(--bg-raised);
    overflow: hidden;
    position: relative;
}
.maturity-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 1s ease;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 0 !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold-bright) !important;
    border-bottom-color: var(--gold-bright) !important;
}

/* ── Well card ── */
.well-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 16px;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
}
.well-card:hover {
    border-color: var(--border-active);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4), var(--glow-gold);
    transform: translateY(-2px);
}
.well-card .well-name {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--gold-bright);
    letter-spacing: 0.1em;
}
.well-card .well-stat {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 4px;
}
.well-card .well-highlight {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--teal);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border-active); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold-dim); }

/* ── Divider ── */
hr { border-color: var(--border-subtle) !important; margin: 1.5rem 0 !important; }

/* ── h1/h2/h3 ── */
h1 { font-family: 'Rajdhani', sans-serif !important; font-weight: 700 !important; }
h2 { font-family: 'Barlow Condensed', sans-serif !important; font-weight: 600 !important; color: var(--text-secondary) !important; }
h3 { font-family: 'Barlow Condensed', sans-serif !important; color: var(--text-secondary) !important; }

p, li { font-family: 'Barlow Condensed', sans-serif !important; font-size: 1rem !important; line-height: 1.6 !important; }

/* ── Sidebar section labels ── */
.sidebar-section {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: var(--text-muted);
    text-transform: uppercase;
    padding: 16px 16px 6px;
    border-top: 1px solid var(--border-subtle);
    margin-top: 8px;
}

/* ── Plotly config (dark bg) ── */
.plotly-graph-div { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PLOTLY THEME CONFIG
# ═══════════════════════════════════════════════════════════════
def apply_theme(fig, title="", height=420, margin=None, extra=None):
    """Apply the PetroStream dark theme to any Plotly figure."""
    axis_style = dict(
        gridcolor='#1a2540', gridwidth=0.5,
        linecolor='#1a2540', zerolinecolor='#2a3f60',
        tickfont=dict(family='Share Tech Mono', size=10, color='#8a9ab5'),
    )
    if margin is None:
        margin = dict(l=50, r=30, t=50, b=50)
    updates = dict(
        paper_bgcolor='#0c1424',
        plot_bgcolor='#080e1a',
        font=dict(family='Barlow Condensed, Share Tech Mono', color='#8a9ab5', size=12),
        title=dict(text=title, font=dict(family='Rajdhani', size=16, color='#e8eaf0'), x=0.02),
        xaxis=axis_style,
        yaxis=axis_style,
        legend=dict(
            bgcolor='rgba(8,14,26,0.85)',
            bordercolor='#1a2540', borderwidth=1,
            font=dict(family='Barlow Condensed', size=11, color='#8a9ab5'),
        ),
        margin=margin,
        colorway=['#f0c040','#00d4aa','#4499ff','#ff8c00','#ff4444','#aa66ff','#44ffcc','#ffcc44'],
        height=height,
    )
    if extra:
        updates.update(extra)
    fig.update_layout(**updates)
    return fig

# Keep axis style dict accessible for reuse
_AXIS = dict(
    gridcolor='#1a2540', gridwidth=0.5,
    linecolor='#1a2540', zerolinecolor='#2a3f60',
    tickfont=dict(family='Share Tech Mono', size=10, color='#8a9ab5'),
)

GOLD_SEQ   = ['#04080f','#1a2a00','#3a5000','#6a7800','#a09000','#c8a020','#f0c040','#ffd870']
TEAL_SEQ   = ['#04080f','#001a14','#003a2a','#006a50','#009a76','#00c49a','#00d4aa','#66ffe0']


# ═══════════════════════════════════════════════════════════════
#  DATA ENGINE
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    data = {
        'Well':      ['SBAA-1','DECH-1','OTLA-1','BDW-1','ODZ-1','OTRT-1','LT-1bis','MGR-1'],
        'X':         [7.5, 6.5, 1.8, 6.2, 5.8, 4.2, 2.0, 5.9],
        'Y':         [5.5, 7.5, 1.2, 6.1, 5.0, 4.3, 2.1, 4.8],
        'Thickness': [70,  68,  54,  48,  185, 188, 173, 253],
        'TOC':       [1.44,2.65,1.49,0.57,5.74,0.97,0.61,0.71],
        'S2':        [4.39,16.04,6.91,2.04,4.06,0.79,0.43,1.88],
        'Tmax':      [446, 440, 437, 460, 445, 452, 443, 454],
        'HI':        [315, 484, 467, 404, 292, 93,  53,  128],
        'OI':        [19,  26,  33,  24,  46,  13,  48,  22],
    }
    df = pd.DataFrame(data)
    df['Ro_calc']    = ((0.018 * df['Tmax']) - 7.16).round(2)
    df['PI']         = (df['S2'] / (df['S2'] + df['TOC'] + 0.001)).round(3)
    df['HC_Potential'] = pd.cut(df['TOC'], bins=[0,0.5,1,2,4,100],
                                labels=['Poor','Fair','Good','Very Good','Excellent'])
    df['Maturity']   = pd.cut(df['Ro_calc'], bins=[0,0.6,0.9,1.35,2.0,100],
                               labels=['Immature','Early Oil','Peak Oil','Wet Gas','Dry Gas'])
    return df

df = load_data()

# colour maps per classification
HC_COLORS = {
    'Poor':'#ff4444','Fair':'#ff8c00','Good':'#f0c040',
    'Very Good':'#00d4aa','Excellent':'#4499ff'
}
MAT_COLORS = {
    'Immature':'#3d4f6a','Early Oil':'#f0c040','Peak Oil':'#00d4aa',
    'Wet Gas':'#ff8c00','Dry Gas':'#ff4444'
}


# ═══════════════════════════════════════════════════════════════
#  PDF REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════
def generate_csv_report(dataframe):
    """Fallback: export as styled CSV since fpdf may not be installed."""
    return dataframe.to_csv(index=False).encode('utf-8')


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div class="sidebar-logo">
    <div class="logo-title"> PetroStream</div>
    <div class="logo-version">ULTRA 2.0 · SBAA BASIN</div>
    <div class="logo-author">Serhoudji Souhil · MSc Petroleum Geology</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

NAV_ICONS = {
    "  Overview":            "Overview",
    "  Basin Registry":      "Basin Registry",
    "  Geochemical Lab":     "Geochemical Lab",
    "  3D Mapping":          "3D Mapping",
    "  Cross-Plots":         "Cross-Plots",
    "  Log Viewer":          "Log Viewer",
    "  Resource Estimation": "Resource Estimation",
    "  Burial History":      "Burial History",
    "  PDF Report":          "PDF Report",
}
menu_label = st.sidebar.radio("", list(NAV_ICONS.keys()), label_visibility="collapsed")
menu = NAV_ICONS[menu_label]

# ── Sidebar stats ──
st.sidebar.markdown('<div class="sidebar-section">Live Basin Stats</div>', unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div style="padding:8px 16px;font-family:'Share Tech Mono',monospace;font-size:0.72rem;color:#8a9ab5;line-height:2;">
  <span style="color:#3d4f6a;">WELLS LOGGED</span><br>
  <span style="color:#f0c040;font-size:1.1rem;">{len(df)}</span><br>
  <span style="color:#3d4f6a;">AVG TOC</span><br>
  <span style="color:#00d4aa;font-size:1.1rem;">{df['TOC'].mean():.2f}%</span><br>
  <span style="color:#3d4f6a;">AVG Ro</span><br>
  <span style="color:#4499ff;font-size:1.1rem;">{df['Ro_calc'].mean():.2f}%</span><br>
  <span style="color:#3d4f6a;">MAX THICKNESS</span><br>
  <span style="color:#ff8c00;font-size:1.1rem;">{df['Thickness'].max()}m</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">Export</div>', unsafe_allow_html=True)
csv_data = generate_csv_report(df)
st.sidebar.download_button(
    label="⬇  Export Basin Data (CSV)",
    data=csv_data,
    file_name="SBAA_Basin_Data.csv",
    mime="text/csv",
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:0.65rem;color:#3d4f6a;text-align:center;padding:8px;font-family:'Share Tech Mono',monospace;">
PETROSTREAM ULTRA 2.0<br>© 2024 SERHOUDJI SOUHIL<br>ALL RIGHTS RESERVED
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════
if menu == "Overview":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">SBAA Basin · Upper Devonian</div>
            <div class="page-title">Project Overview</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_map = st.columns([1, 1.4])

    with col_info:
        st.markdown("""
        <div class="section-header">Executive Summary</div>
        <p>
        Integrated characterization of the <strong style="color:#f0c040;">Upper Devonian source rock</strong>
        within the <strong style="color:#00d4aa;">SBAA Basin</strong> using Rock-Eval pyrolysis data,
        stratigraphic analysis, and advanced geochemical cross-plot techniques.
        </p>
        <p>
        Maturity assessment follows the <em>Jarvie (2007)</em> vitrinite reflectance proxy model:
        <code style="background:#101828;color:#00d4aa;padding:2px 6px;border-radius:3px;">Ro = 0.018 × Tmax − 7.16</code>
        </p>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Data Inventory</div>', unsafe_allow_html=True)

        inv_data = {
            "Parameter":   ["Wells Analysed","Stratigraphic Interval","Main Method","Interpolation","Coordinate System"],
            "Value":       ["8 exploration wells","Upper Devonian (Frasnian)","Rock-Eval Pyrolysis","Cubic Spline / RBF","UTM Zone 31N"],
        }
        st.dataframe(pd.DataFrame(inv_data), use_container_width=True, hide_index=True)

        st.markdown('<div class="section-header">Maturity Window</div>', unsafe_allow_html=True)
        for _, row in df.iterrows():
            pct = min(row['Ro_calc'] / 3.0 * 100, 100)
            col = MAT_COLORS.get(str(row['Maturity']), '#3d4f6a')
            st.markdown(f"""
            <div class="maturity-bar-wrap">
                <div style="display:flex;justify-content:space-between;font-size:0.72rem;margin-bottom:3px;">
                    <span style="font-family:'Rajdhani',sans-serif;color:#e8eaf0;font-weight:600;">{row['Well']}</span>
                    <span style="font-family:'Share Tech Mono',monospace;color:{col};">Ro {row['Ro_calc']:.2f}% · {row['Maturity']}</span>
                </div>
                <div class="maturity-bar">
                    <div class="maturity-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{col}88,{col});"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_map:
        st.markdown('<div class="section-header">Well Location Map</div>', unsafe_allow_html=True)
        fig_map = go.Figure()
        for _, row in df.iterrows():
            hc = str(row['HC_Potential'])
            fig_map.add_trace(go.Scatter(
                x=[row['X']], y=[row['Y']],
                mode='markers+text',
                marker=dict(size=14, color=HC_COLORS.get(hc,'#f0c040'),
                            line=dict(color='#e8eaf0', width=1),
                            symbol='diamond'),
                text=[row['Well']],
                textposition='top center',
                textfont=dict(family='Rajdhani', size=11, color='#e8eaf0'),
                name=hc,
                hovertemplate=(
                    f"<b>{row['Well']}</b><br>"
                    f"TOC: {row['TOC']:.2f}%<br>"
                    f"Tmax: {row['Tmax']}°C<br>"
                    f"Ro: {row['Ro_calc']:.2f}%<br>"
                    f"HC Potential: {hc}<extra></extra>"
                ),
                showlegend=False,
            ))
        apply_theme(fig_map, title="Well Locations — HC Potential", height=480, extra=dict(
            xaxis_title="Easting (km)", yaxis_title="Northing (km)",
        ))
        st.plotly_chart(fig_map, use_container_width=True)

        # Legend
        st.markdown("""
        <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:-8px;">
        """ + "".join([
            f'<span class="status-badge badge-active" style="background:rgba(0,0,0,0);border-color:{HC_COLORS[k]}20;color:{HC_COLORS[k]};">◆ {k}</span>'
            for k in HC_COLORS
        ]) + "</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 2 — BASIN REGISTRY
# ═══════════════════════════════════════════════════════════════
elif menu == "Basin Registry":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">Integrated Data · 8 Wells</div>
            <div class="page-title">Basin Registry</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Avg TOC",        f"{df['TOC'].mean():.2f} %")
    c2.metric("Max Thickness",  f"{df['Thickness'].max()} m")
    c3.metric("Avg Ro",         f"{df['Ro_calc'].mean():.2f} %")
    c4.metric("Avg HI",         f"{df['HI'].mean():.0f}")
    c5.metric("Wells",          f"{len(df)}")

    st.markdown('<div class="section-header">Well Cards</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (_, row) in enumerate(df.iterrows()):
        hc   = str(row['HC_Potential'])
        mat  = str(row['Maturity'])
        col  = HC_COLORS.get(hc,'#f0c040')
        mcol = MAT_COLORS.get(mat,'#3d4f6a')
        with cols[i % 4]:
            st.markdown(f"""
            <div class="well-card">
                <div style="position:absolute;top:0;right:0;width:4px;height:100%;background:{col};border-radius:0 6px 6px 0;"></div>
                <div class="well-name">{row['Well']}</div>
                <div class="well-highlight">{row['Thickness']} m</div>
                <div class="well-stat">THICKNESS</div>
                <hr style="margin:8px 0;border-color:#1a2540;">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">
                    <div>
                        <div style="font-family:'Share Tech Mono',monospace;font-size:0.85rem;color:#f0c040;">{row['TOC']:.2f}%</div>
                        <div class="well-stat">TOC</div>
                    </div>
                    <div>
                        <div style="font-family:'Share Tech Mono',monospace;font-size:0.85rem;color:#4499ff;">{row['Ro_calc']:.2f}%</div>
                        <div class="well-stat">Ro</div>
                    </div>
                    <div>
                        <div style="font-family:'Share Tech Mono',monospace;font-size:0.85rem;color:#ff8c00;">{row['Tmax']}°C</div>
                        <div class="well-stat">Tmax</div>
                    </div>
                    <div>
                        <div style="font-family:'Share Tech Mono',monospace;font-size:0.85rem;color:#00d4aa;">{row['HI']}</div>
                        <div class="well-stat">HI</div>
                    </div>
                </div>
                <hr style="margin:8px 0;border-color:#1a2540;">
                <span class="status-badge" style="background:rgba(0,0,0,0);border-color:{col}33;color:{col};font-size:0.62rem;">{hc}</span>
                <span class="status-badge" style="background:rgba(0,0,0,0);border-color:{mcol}33;color:{mcol};font-size:0.62rem;margin-left:4px;">{mat}</span>
            </div>
            <br>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Complete Dataset</div>', unsafe_allow_html=True)
    display_df = df[['Well','Thickness','TOC','S2','Tmax','HI','OI','Ro_calc','HC_Potential','Maturity']].copy()
    st.dataframe(
        display_df.style
            .format({'TOC':'{:.2f}','S2':'{:.2f}','Ro_calc':'{:.2f}'})
            .background_gradient(subset=['TOC','S2','Thickness'], cmap='YlOrBr')
            .background_gradient(subset=['Ro_calc','Tmax'], cmap='Blues'),
        use_container_width=True,
        hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════
#  PAGE 3 — GEOCHEMICAL LAB
# ═══════════════════════════════════════════════════════════════
elif menu == "Geochemical Lab":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">Rock-Eval Pyrolysis · Source Rock Evaluation</div>
            <div class="page-title">Geochemical Lab</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["  Distribution Analysis", "  Thermal Maturity", "  Ranking"])

    with tab1:
        cols_params = st.columns([1,2])
        with cols_params[0]:
            param = st.selectbox("Parameter", ['TOC','S2','HI','OI','Tmax','Ro_calc','Thickness'], index=0)
        with cols_params[1]:
            chart_type = st.radio("Chart type", ["Bar","Violin","Box"], horizontal=True)

        param_colors = {
            'TOC':'#f0c040','S2':'#00d4aa','HI':'#4499ff',
            'OI':'#ff8c00','Tmax':'#ff4444','Ro_calc':'#aa66ff','Thickness':'#44ccff'
        }
        pc = param_colors.get(param, '#f0c040')

        if chart_type == "Bar":
            hover_text = [f"<b>{well}</b><br>{param}: {val:.2f}" for well, val in zip(df['Well'], df[param])]
            fig = go.Figure(go.Bar(
                x=df['Well'], y=df[param],
                marker=dict(
                    color=df[param],
                    colorscale=[[0, '#101828'], [0.5, pc], [1, pc]],
                    line=dict(color=pc, width=0.5),
                ),
                text=hover_text,
                textposition='outside',
                textfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'),
                hovertemplate='%{text}<extra></extra>',
            ))
        elif chart_type == "Violin":
            hover_text = [f"{param}: {val:.2f}" for val in df[param]]
            # Convert hex to rgba for fillcolor transparency
            pc_rgba = f'rgba({int(pc[1:3],16)},{int(pc[3:5],16)},{int(pc[5:7],16)},0.13)'
            fig = go.Figure(go.Violin(
                y=df[param], points='all',
                pointpos=0, jitter=0.3,
                line_color=pc, fillcolor=pc_rgba,
                marker=dict(color=pc, size=8),
                hovertemplate='%{text}<extra></extra>',
                text=hover_text,
            ))
        else:
            hover_text = [f"{param}: {val:.2f}" for val in df[param]]
            # Convert hex to rgba for fillcolor transparency
            pc_rgba = f'rgba({int(pc[1:3],16)},{int(pc[3:5],16)},{int(pc[5:7],16)},0.13)'
            fig = go.Figure(go.Box(
                y=df[param], points='all',
                marker=dict(color=pc, size=8),
                line=dict(color=pc),
                fillcolor=pc_rgba,
                hovertemplate='%{text}<extra></extra>',
                text=hover_text,
            ))

        apply_theme(fig, title=f"{param} — All Wells", height=420, extra=dict(yaxis_title=param))
        st.plotly_chart(fig, use_container_width=True)

        # Quick stats
        s = df[param]
        sc1,sc2,sc3,sc4 = st.columns(4)
        sc1.metric("Mean",  f"{s.mean():.2f}")
        sc2.metric("Std",   f"{s.std():.2f}")
        sc3.metric("Min",   f"{s.min():.2f}")
        sc4.metric("Max",   f"{s.max():.2f}")

    with tab2:
        fig_mat = go.Figure()
        # Pseudo-Tmax profile
        tmax_sorted = df.sort_values('Tmax')
        fig_mat.add_trace(go.Scatter(
            x=tmax_sorted['Well'], y=tmax_sorted['Tmax'],
            mode='lines+markers',
            line=dict(color='#ff4444', width=2),
            marker=dict(color=tmax_sorted['Ro_calc'], colorscale='YlOrRd', size=12,
                        line=dict(color='#e8eaf0',width=1),
                        colorbar=dict(title='Ro%', x=1.02)),
            name='Tmax (°C)',
            hovertemplate='<b>%{x}</b><br>Tmax: %{y}°C<extra></extra>',
        ))
        # Reference lines
        for level, label, color in [(435,'Early Oil','#f0c040'),(455,'Wet Gas','#ff8c00'),(470,'Dry Gas','#ff4444')]:
            fig_mat.add_hline(y=level, line_dash='dash', line_color=color, opacity=0.5,
                              annotation_text=label, annotation_position='right',
                              annotation_font=dict(color=color, size=10))
        apply_theme(fig_mat, title="Thermal Maturity Profile (Tmax / Ro)", height=380, extra=dict(yaxis_title="Tmax (°C)"))
        st.plotly_chart(fig_mat, use_container_width=True)

        # Ro vs Depth proxy
        fig_ro = make_subplots(rows=1, cols=2,
                               subplot_titles=['Ro Calculated', 'HI vs OI (Kerogen Type)'],
                               specs=[[{"type":"scatter"},{"type":"scatter"}]])
        for _, row in df.iterrows():
            col = MAT_COLORS.get(str(row['Maturity']),'#3d4f6a')
            fig_ro.add_trace(go.Bar(
                x=[row['Well']], y=[row['Ro_calc']],
                marker_color=col, name=row['Well'], showlegend=False,
            ), row=1, col=1)
            fig_ro.add_trace(go.Scatter(
                x=[row['OI']], y=[row['HI']],
                mode='markers+text', text=[row['Well']],
                textposition='top center',
                textfont=dict(size=9, color='#8a9ab5'),
                marker=dict(size=10, color=col, line=dict(color='#e8eaf0',width=0.5)),
                showlegend=False,
                hovertemplate=f"<b>{row['Well']}</b><br>OI: {row['OI']}<br>HI: {row['HI']}<extra></extra>",
            ), row=1, col=2)
        apply_theme(fig_ro, title="", height=380)
        fig_ro.update_yaxes(title_text="Ro (%)",  row=1, col=1)
        fig_ro.update_yaxes(title_text="HI (mg HC/g TOC)", row=1, col=2)
        fig_ro.update_xaxes(title_text="OI (mg CO₂/g TOC)", row=1, col=2)
        st.plotly_chart(fig_ro, use_container_width=True)

    with tab3:
        rank_by = st.selectbox("Rank wells by", ['TOC','S2','Thickness','HI','Ro_calc'])
        df_ranked = df[['Well',rank_by,'HC_Potential','Maturity']].sort_values(rank_by, ascending=False).reset_index(drop=True)
        df_ranked.index += 1
        df_ranked.insert(0,'Rank',df_ranked.index)

        hover_text = [f"<b>{well}</b><br>{rank_by}: {val:.2f}" for well, val in zip(df_ranked['Well'], df_ranked[rank_by])]
        fig_rank = go.Figure(go.Bar(
            x=df_ranked[rank_by], y=df_ranked['Well'],
            orientation='h',
            marker=dict(
                color=df_ranked[rank_by],
                colorscale=[[0,'#1a2540'],[0.5,'#c8982a'],[1,'#f0c040']],
                line=dict(color='#f0c040', width=0.3),
            ),
            text=hover_text,
            textposition='outside',
            textfont=dict(family='Share Tech Mono', size=10),
            hovertemplate='%{text}<extra></extra>',
        ))
        apply_theme(fig_rank, title=f"Well Ranking by {rank_by}", height=380, extra=dict(
            xaxis_title=rank_by, yaxis_autorange='reversed',
        ))
        st.plotly_chart(fig_rank, use_container_width=True)
        st.dataframe(df_ranked, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 4 — 3D MAPPING
# ═══════════════════════════════════════════════════════════════
elif menu == "3D Mapping":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">Spatial Interpolation · Basin Maps</div>
            <div class="page-title">3D Mapping Suite</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_map = st.columns([1, 3])
    with col_ctrl:
        param_3d = st.selectbox("Map Parameter", ['Thickness','TOC','S2','Ro_calc','HI'])
        interp   = st.selectbox("Interpolation", ['Cubic','Linear','Nearest'])
        view_3d  = st.radio("View Mode", ["Surface 3D","Contour 2D","Both"])
        resolution = st.slider("Grid Resolution", 30, 120, 60)
        colormap = st.selectbox("Color Scale", ['YlOrBr','Plasma','Viridis','Hot','Cividis'])

    with col_map:
        xi = np.linspace(df['X'].min()-0.5, df['X'].max()+0.5, resolution)
        yi = np.linspace(df['Y'].min()-0.5, df['Y'].max()+0.5, resolution)
        XI, YI = np.meshgrid(xi, yi)
        method_map = {'Cubic':'cubic','Linear':'linear','Nearest':'nearest'}
        ZI = griddata((df['X'], df['Y']), df[param_3d],
                      (XI, YI), method=method_map[interp])

        if view_3d in ["Surface 3D","Both"]:
            fig_surf = go.Figure(go.Surface(
                x=xi, y=yi, z=ZI,
                colorscale=colormap,
                contours=dict(
                    z=dict(show=True, usecolormap=True, highlightcolor='#f0c040', project_z=True)
                ),
                lighting=dict(ambient=0.6, diffuse=0.8, specular=0.3),
                colorbar=dict(title=param_3d, tickfont=dict(color='#8a9ab5', size=10),
                              bgcolor='rgba(8,14,26,0.8)', bordercolor='#1a2540'),
                hovertemplate='E: %{x:.1f}<br>N: %{y:.1f}<br>%{z:.2f}<extra></extra>',
            ))
            # Add well scatter
            fig_surf.add_trace(go.Scatter3d(
                x=df['X'], y=df['Y'], z=df[param_3d]+df[param_3d].max()*0.05,
                mode='markers+text',
                marker=dict(size=5, color='#f0c040', symbol='diamond',
                            line=dict(color='white', width=1)),
                text=df['Well'],
                textfont=dict(size=9, color='#f0c040'),
                name='Wells',
                hovertemplate='<b>%{text}</b><br>%{z:.2f}<extra></extra>',
            ))
            fig_surf.update_layout(
                paper_bgcolor='#0c1424',
                plot_bgcolor='#080e1a',
                font=dict(family='Barlow Condensed, Share Tech Mono', color='#8a9ab5', size=12),
                title=dict(text=f"{param_3d} — 3D Surface Map",
                           font=dict(family='Rajdhani', size=16, color='#e8eaf0'), x=0.02),
                legend=dict(bgcolor='rgba(8,14,26,0.85)', bordercolor='#1a2540', borderwidth=1,
                            font=dict(family='Barlow Condensed', size=11, color='#8a9ab5')),
                scene=dict(
                    bgcolor='#080e1a',
                    xaxis=dict(backgroundcolor='#0c1424', gridcolor='#1a2540',
                               title='Easting (km)', tickfont=dict(size=9,color='#8a9ab5')),
                    yaxis=dict(backgroundcolor='#0c1424', gridcolor='#1a2540',
                               title='Northing (km)', tickfont=dict(size=9,color='#8a9ab5')),
                    zaxis=dict(backgroundcolor='#0c1424', gridcolor='#1a2540',
                               title=param_3d, tickfont=dict(size=9,color='#8a9ab5')),
                    camera=dict(eye=dict(x=1.6, y=-1.6, z=1.2)),
                ),
                height=520,
                margin=dict(l=0,r=0,t=50,b=0),
            )
            st.plotly_chart(fig_surf, use_container_width=True)

        if view_3d in ["Contour 2D","Both"]:
            fig_cont = go.Figure()
            fig_cont.add_trace(go.Contour(
                x=xi, y=yi, z=ZI,
                colorscale=colormap,
                ncontours=20,
                contours_coloring='heatmap',
                line_smoothing=0.85,
                colorbar=dict(title=param_3d, tickfont=dict(color='#8a9ab5',size=10),
                              bgcolor='rgba(8,14,26,0.8)', bordercolor='#1a2540'),
                hovertemplate='E: %{x:.1f}<br>N: %{y:.1f}<br>%{z:.2f}<extra></extra>',
            ))
            fig_cont.add_trace(go.Scatter(
                x=df['X'], y=df['Y'],
                mode='markers+text',
                marker=dict(size=10, color='#f0c040', symbol='diamond',
                            line=dict(color='white',width=1)),
                text=df['Well'],
                textposition='top center',
                textfont=dict(family='Rajdhani', size=11, color='#f0c040'),
                name='Wells',
                hovertemplate='<b>%{text}</b><extra></extra>',
            ))
            apply_theme(fig_cont, title=f"{param_3d} — Contour Map", height=480, extra=dict(
                xaxis_title='Easting (km)', yaxis_title='Northing (km)',
            ))
            st.plotly_chart(fig_cont, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 5 — CROSS-PLOTS
# ═══════════════════════════════════════════════════════════════
elif menu == "Cross-Plots":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">Geochemical Diagnostics · Kerogen Typing</div>
            <div class="page-title">Cross-Plot Diagnostics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    params = ['TOC','S2','HI','OI','Tmax','Ro_calc','Thickness','PI']
    cp1, cp2, cp3 = st.columns([1,1,1])
    with cp1: x_param = st.selectbox("X Axis", params, index=0)
    with cp2: y_param = st.selectbox("Y Axis", params, index=1)
    with cp3: size_p  = st.selectbox("Bubble Size", params, index=2)

    tab_a, tab_b, tab_c = st.tabs(["  Bubble Cross-Plot", "  Van Krevelen Diagram", "  Correlation Matrix"])

    with tab_a:
        fig_cp = go.Figure()
        for _, row in df.iterrows():
            hc  = str(row['HC_Potential'])
            col = HC_COLORS.get(hc,'#f0c040')
            sz  = max(10, min(40, row[size_p] / df[size_p].max() * 40))
            fig_cp.add_trace(go.Scatter(
                x=[row[x_param]], y=[row[y_param]],
                mode='markers+text',
                marker=dict(size=sz, color=col, opacity=0.85,
                            line=dict(color='white',width=1.2),
                            symbol='circle'),
                text=[row['Well']],
                textposition='top center',
                textfont=dict(family='Rajdhani', size=10, color='#e8eaf0'),
                name=hc,
                showlegend=False,
                hovertemplate=(
                    f"<b>{row['Well']}</b><br>"
                    f"{x_param}: {row[x_param]:.2f}<br>"
                    f"{y_param}: {row[y_param]:.2f}<br>"
                    f"{size_p}: {row[size_p]:.2f}<br>"
                    f"HC Potential: {hc}<extra></extra>"
                ),
            ))
        # Trendline
        z = np.polyfit(df[x_param], df[y_param], 1)
        xfit = np.linspace(df[x_param].min(), df[x_param].max(), 100)
        fig_cp.add_trace(go.Scatter(
            x=xfit, y=np.polyval(z, xfit),
            mode='lines', line=dict(color='#f0c040', dash='dot', width=1.5),
            name='Trend', showlegend=False,
        ))
        r = np.corrcoef(df[x_param], df[y_param])[0,1]
        apply_theme(fig_cp, title=f"{y_param} vs {x_param}  |  r = {r:.3f}", height=480, extra=dict(
            xaxis_title=x_param, yaxis_title=y_param,
        ))
        st.plotly_chart(fig_cp, use_container_width=True)

    with tab_b:
        fig_vk = go.Figure()
        # Type regions (background)
        regions = [
            dict(x=[0,50,50,0], y=[600,600,150,150],  name='Type II', fillcolor='rgba(68,153,255,0.06)'),
            dict(x=[0,150,150,0], y=[700,700,400,400], name='Type I',  fillcolor='rgba(0,212,170,0.06)'),
            dict(x=[50,150,150,50], y=[200,200,100,100], name='Type III', fillcolor='rgba(255,140,0,0.06)'),
        ]
        for r in regions:
            fig_vk.add_trace(go.Scatter(
                x=r['x'], y=r['y'], fill='toself',
                fillcolor=r['fillcolor'], line=dict(color='rgba(255,255,255,0.05)'),
                name=r['name'], mode='lines', hoverinfo='skip',
            ))
        for _, row in df.iterrows():
            col = MAT_COLORS.get(str(row['Maturity']),'#3d4f6a')
            fig_vk.add_trace(go.Scatter(
                x=[row['OI']], y=[row['HI']],
                mode='markers+text',
                marker=dict(size=14, color=col, symbol='diamond',
                            line=dict(color='white',width=1)),
                text=[row['Well']],
                textposition='top center',
                textfont=dict(family='Rajdhani', size=10, color='#e8eaf0'),
                name=row['Well'], showlegend=False,
                hovertemplate=(
                    f"<b>{row['Well']}</b><br>"
                    f"OI: {row['OI']}<br>HI: {row['HI']}<br>"
                    f"Maturity: {row['Maturity']}<extra></extra>"
                ),
            ))
        for label, ox, hy in [('TYPE I', 25, 660), ('TYPE II', 100, 580), ('TYPE III', 100, 180)]:
            fig_vk.add_annotation(x=ox, y=hy, text=label, showarrow=False,
                                  font=dict(size=10, color='#3d4f6a',
                                            family='Share Tech Mono'), opacity=0.7)
        apply_theme(fig_vk, title="Van Krevelen Diagram — Kerogen Typing", height=480, extra=dict(
            xaxis=dict(gridcolor='#1a2540', gridwidth=0.5, linecolor='#1a2540',
                       zerolinecolor='#2a3f60', range=[0, 60],
                       tickfont=dict(family='Share Tech Mono', size=10, color='#8a9ab5'),
                       title_text="OI (mg CO₂/g TOC)"),
            yaxis=dict(gridcolor='#1a2540', gridwidth=0.5, linecolor='#1a2540',
                       zerolinecolor='#2a3f60', range=[0, 700],
                       tickfont=dict(family='Share Tech Mono', size=10, color='#8a9ab5'),
                       title_text="HI (mg HC/g TOC)"),
        ))
        st.plotly_chart(fig_vk, use_container_width=True)

    with tab_c:
        numeric_cols = ['Thickness','TOC','S2','Tmax','HI','OI','Ro_calc','PI']
        corr = df[numeric_cols].corr()
        fig_hm = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.index,
            colorscale=[
                [0.0,'#ff4444'],[0.2,'#8a1a1a'],[0.4,'#1a2540'],
                [0.6,'#0d5a3a'],[0.8,'#00a07a'],[1.0,'#00d4aa']
            ],
            zmid=0, text=corr.round(2).values.astype(str),
            texttemplate="%{text}", textfont=dict(size=10, family='Share Tech Mono'),
            hoverongaps=False, showscale=True,
            colorbar=dict(tickfont=dict(color='#8a9ab5',size=9),
                          bgcolor='rgba(8,14,26,0.8)', bordercolor='#1a2540'),
        ))
        apply_theme(fig_hm, title="Parameter Correlation Matrix", height=480, extra=dict(
            xaxis=dict(gridcolor='#1a2540', tickfont=dict(family='Share Tech Mono', size=10, color='#8a9ab5')),
            yaxis=dict(gridcolor='#1a2540', tickfont=dict(family='Share Tech Mono', size=10, color='#8a9ab5')),
        ))
        st.plotly_chart(fig_hm, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 6 — LOG VIEWER
# ═══════════════════════════════════════════════════════════════
elif menu == "Log Viewer":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">Synthetic Petrophysical Logs</div>
            <div class="page-title">Log Viewer</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    lv1, lv2 = st.columns([1, 3])
    with lv1:
        well_sel = st.selectbox("Select Well", df['Well'].tolist())
        log_set  = st.multiselect("Log Tracks", ['GR','RHOB','NPHI','RT','DT','PE'], default=['GR','RHOB','NPHI','RT'])
        depth_rng = st.slider("Depth Range (m)", 2000, 4500, (2800, 3800), step=50)
        seed = df[df['Well']==well_sel].index[0]

    well_row = df[df['Well']==well_sel].iloc[0]

    depth = np.arange(depth_rng[0], depth_rng[1], 0.5)
    np.random.seed(seed * 7 + 42)
    logs = {
        'GR':   np.clip(np.cumsum(np.random.randn(len(depth))*0.5)+70, 10, 150),
        'RHOB': np.clip(np.cumsum(np.random.randn(len(depth))*0.001)+2.5, 2.0, 2.9),
        'NPHI': np.clip(np.cumsum(np.random.randn(len(depth))*0.001)+0.22, 0.05, 0.45),
        'RT':   np.abs(np.cumsum(np.random.randn(len(depth))*0.2)+10),
        'DT':   np.clip(np.cumsum(np.random.randn(len(depth))*0.3)+80, 50, 140),
        'PE':   np.clip(np.cumsum(np.random.randn(len(depth))*0.05)+2.8, 1.5, 6.0),
    }
    log_meta = {
        'GR':   dict(color='#00d4aa', unit='API',       xmin=0,    xmax=150,  fill=True),
        'RHOB': dict(color='#ff4444', unit='g/cc',      xmin=1.8,  xmax=3.0,  fill=False),
        'NPHI': dict(color='#4499ff', unit='v/v',       xmin=0.0,  xmax=0.5,  fill=True),
        'RT':   dict(color='#f0c040', unit='ohm·m',     xmin=0.1,  xmax=1000, fill=False),
        'DT':   dict(color='#aa66ff', unit='µs/ft',     xmin=40,   xmax=160,  fill=False),
        'PE':   dict(color='#ff8c00', unit='b/e',       xmin=0,    xmax=8,    fill=False),
    }

    visible_logs = [l for l in log_set if l in logs]
    if not visible_logs:
        st.info("Select at least one log track.")
    else:
        n_tracks = len(visible_logs)
        fig_log = make_subplots(
            rows=1, cols=n_tracks,
            shared_yaxes=True,
            subplot_titles=visible_logs,
            horizontal_spacing=0.02,
        )
        for i, log_name in enumerate(visible_logs):
            meta = log_meta[log_name]
            vals = logs[log_name]
            col_num = i + 1

            if meta['fill']:
                # Convert hex to rgba for transparency
                hex_color = meta['color'].lstrip('#')
                r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                rgba_color = f'rgba({r},{g},{b},0.13)'
                fig_log.add_trace(go.Scatter(
                    x=vals, y=depth, mode='lines',
                    line=dict(color=meta['color'], width=1),
                    fill='tozerox', fillcolor=rgba_color,
                    name=log_name,
                    hovertemplate=f"{log_name}: %{{x:.2f}} {meta['unit']}<br>Depth: %{{y:.0f}}m<extra></extra>",
                ), row=1, col=col_num)
            else:
                fig_log.add_trace(go.Scatter(
                    x=vals, y=depth, mode='lines',
                    line=dict(color=meta['color'], width=1.2),
                    name=log_name,
                    hovertemplate=f"{log_name}: %{{x:.2f}} {meta['unit']}<br>Depth: %{{y:.0f}}m<extra></extra>",
                ), row=1, col=col_num)

            axis_key = 'xaxis' if col_num == 1 else f'xaxis{col_num}'
            fig_log.update_layout(**{axis_key: dict(
                range=[meta['xmin'], meta['xmax']],
                gridcolor='#1a2540', gridwidth=0.5,
                tickfont=dict(family='Share Tech Mono', size=8, color='#8a9ab5'),
                title_text=f"{log_name} ({meta['unit']})",
                title_font=dict(family='Barlow Condensed', size=10, color=meta['color']),
                side='top',
            )})

        fig_log.update_yaxes(
            autorange='reversed',
            title_text="MD (m)", title_font=dict(family='Barlow Condensed', size=11, color='#8a9ab5'),
            gridcolor='#1a2540', gridwidth=0.5,
            tickfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'),
        )
        fig_log.update_layout(
            paper_bgcolor='#0c1424',
            plot_bgcolor='#080e1a',
            font=dict(family='Barlow Condensed, Share Tech Mono', color='#8a9ab5', size=12),
            title=dict(text=f"Well Log — {well_sel}",
                       font=dict(family='Rajdhani', size=16, color='#e8eaf0'), x=0.02),
            legend=dict(bgcolor='rgba(8,14,26,0.85)', bordercolor='#1a2540', borderwidth=1,
                        font=dict(family='Barlow Condensed', size=11, color='#8a9ab5')),
            margin=dict(l=50, r=30, t=80, b=50),
            height=650,
            showlegend=False,
        )
        st.plotly_chart(fig_log, use_container_width=True)

    with lv2:
        st.markdown(f"""
        <div class="section-header">Well Header — {well_sel}</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px;">
            <div class="well-card">
                <div class="well-stat">TOC</div>
                <div class="well-highlight">{well_row['TOC']:.2f}%</div>
            </div>
            <div class="well-card">
                <div class="well-stat">Tmax</div>
                <div class="well-highlight">{well_row['Tmax']}°C</div>
            </div>
            <div class="well-card">
                <div class="well-stat">Ro calc</div>
                <div class="well-highlight">{well_row['Ro_calc']:.2f}%</div>
            </div>
            <div class="well-card">
                <div class="well-stat">HI</div>
                <div class="well-highlight">{well_row['HI']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 7 — RESOURCE ESTIMATION
# ═══════════════════════════════════════════════════════════════
elif menu == "Resource Estimation":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">Volumetric Analysis · Shale Oil / Gas Potential</div>
            <div class="page-title">Resource Estimation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(240,192,64,0.06);border:1px solid #8a6510;border-left:3px solid #f0c040;
                border-radius:4px;padding:12px 16px;margin-bottom:1.5rem;
                font-family:'Barlow Condensed',sans-serif;font-size:0.95rem;color:#8a9ab5;">
     <strong style="color:#f0c040;">Methodology:</strong>
    Shale Oil-in-Place (OOIP) via modified Jarvie (2012) formula. 
    Gas-in-Place (OGIP) via Langmuir adsorption model.
    Adjust parameters below and results update live.
    </div>
    """, unsafe_allow_html=True)

    re_left, re_right = st.columns([1, 2])

    with re_left:
        st.markdown('<div class="section-header">Basin Parameters</div>', unsafe_allow_html=True)
        area_km2      = st.slider("Drainage Area (km²)",       10, 500, 150, step=10)
        net_pay_m     = st.slider("Net Pay Thickness (m)",      5,  80,  30, step=1)
        porosity_pct  = st.slider("Porosity (%)",               2,  20,   8, step=1)
        sw_pct        = st.slider("Water Saturation (%)",       20,  70,  35, step=5)
        bo_factor     = st.slider("Formation Vol. Factor (Bo)", 1.0, 2.0, 1.3, step=0.05)
        rf_pct        = st.slider("Recovery Factor (%)",         2,  30,  8,  step=1)

        st.markdown('<div class="section-header">Geochemical Inputs</div>', unsafe_allow_html=True)
        well_sel_re = st.selectbox("Reference Well", df['Well'].tolist(), key='re_well')
        ref         = df[df['Well'] == well_sel_re].iloc[0]
        toc_use     = st.slider("TOC (%)",  0.1, 8.0, float(ref['TOC']),  step=0.05)
        hi_use      = st.slider("HI",        50, 600, int(ref['HI']),      step=5)
        ro_use      = st.slider("Ro (%)",   0.3, 3.0, float(ref['Ro_calc']), step=0.05)

    with re_right:
        # ── Volumetric calculations ──
        area_acres   = area_km2 * 247.105
        net_pay_ft   = net_pay_m * 3.28084
        phi          = porosity_pct / 100
        sw           = sw_pct / 100
        rf           = rf_pct / 100

        # OOIP (MMbbl) — simplified Jarvie shale oil
        ooip_mmbbl   = (area_acres * net_pay_ft * phi * (1 - sw)) / (5.615 * bo_factor * 1e6)
        ooip_mmbbl  *= 1e6  # re-scale to meaningful number
        eur_oil      = ooip_mmbbl * rf

        # OGIP (Bcf) — Langmuir-based
        # Vl = Langmuir volume (scf/ton), Pl = Langmuir pressure (psi)
        density_g_cc = 2.55
        vl           = 100 * toc_use          # proxy: ~100 scf/ton per % TOC
        pl           = 500.0
        p_res        = 3000.0
        v_ads        = vl * p_res / (pl + p_res)   # scf/ton
        bulk_vol_m3  = area_km2 * 1e6 * net_pay_m
        mass_tons    = bulk_vol_m3 * density_g_cc * (1 - phi) * 1000
        ogip_bcf     = (mass_tons * v_ads) / 1e9
        eur_gas      = ogip_bcf * rf * 2

        # Transformation ratio proxy
        tr = min(1.0, max(0.0, (ro_use - 0.6) / (1.35 - 0.6)))
        expelled_hc = toc_use * hi_use * tr * 0.001  # kg HC / ton rock

        # ── KPI row ──
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("OOIP (MMbbl)",    f"{ooip_mmbbl:.1f}")
        k2.metric("EUR Oil (MMbbl)", f"{eur_oil:.1f}")
        k3.metric("OGIP (Bcf)",      f"{ogip_bcf:.1f}")
        k4.metric("EUR Gas (Bcf)",   f"{eur_gas:.1f}")

        st.markdown('<div class="section-header">Sensitivity — Recovery Factor vs Area</div>', unsafe_allow_html=True)
        rf_range   = np.arange(2, 31, 2)
        area_range = [50, 100, 150, 200, 300]
        fig_sens = go.Figure()
        colors_sens = ['#3d4f6a','#f0c040','#00d4aa','#4499ff','#ff8c00']
        for ai, a in enumerate(area_range):
            a_acres = a * 247.105
            ooip_v  = (a_acres * net_pay_ft * phi * (1 - sw)) / (5.615 * bo_factor * 1e6) * 1e6
            eur_v   = ooip_v * (rf_range / 100)
            fig_sens.add_trace(go.Scatter(
                x=rf_range, y=eur_v,
                mode='lines+markers',
                line=dict(color=colors_sens[ai], width=2),
                marker=dict(size=5),
                name=f"{a} km²",
                hovertemplate=f"Area {a} km²<br>RF: %{{x}}%<br>EUR: %{{y:.1f}} MMbbl<extra></extra>",
            ))
        # Mark current scenario
        fig_sens.add_trace(go.Scatter(
            x=[rf_pct], y=[eur_oil],
            mode='markers', marker=dict(size=14, color='#ff4444', symbol='star',
                                         line=dict(color='white', width=1.5)),
            name='Current', showlegend=True,
            hovertemplate=f"Current: EUR {eur_oil:.1f} MMbbl<extra></extra>",
        ))
        apply_theme(fig_sens, title="EUR Oil Sensitivity (MMbbl)", height=340, extra=dict(
            xaxis_title="Recovery Factor (%)", yaxis_title="EUR (MMbbl)",
        ))
        st.plotly_chart(fig_sens, use_container_width=True)

        st.markdown('<div class="section-header">HC Generation Model — All Wells</div>', unsafe_allow_html=True)
        gen_data = []
        for _, row in df.iterrows():
            tr_w  = min(1.0, max(0.0, (row['Ro_calc'] - 0.6) / (1.35 - 0.6)))
            exp_w = row['TOC'] * row['HI'] * tr_w * 0.001
            gen_data.append({'Well': row['Well'], 'TR': tr_w, 'Expelled_HC': exp_w,
                             'HC_Potential': str(row['HC_Potential'])})
        gen_df = pd.DataFrame(gen_data)

        fig_gen = make_subplots(rows=1, cols=2,
                                subplot_titles=['Transformation Ratio', 'Expelled HC (kg/ton)'],
                                specs=[[{"type":"bar"},{"type":"bar"}]])
        for _, row in gen_df.iterrows():
            c = HC_COLORS.get(row['HC_Potential'], '#f0c040')
            fig_gen.add_trace(go.Bar(x=[row['Well']], y=[row['TR']],
                                     marker_color=c, showlegend=False,
                                     hovertemplate=f"<b>{row['Well']}</b><br>TR: {row['TR']:.2f}<extra></extra>"),
                              row=1, col=1)
            fig_gen.add_trace(go.Bar(x=[row['Well']], y=[row['Expelled_HC']],
                                     marker_color=c, showlegend=False,
                                     hovertemplate=f"<b>{row['Well']}</b><br>Expelled: {row['Expelled_HC']:.3f} kg/ton<extra></extra>"),
                              row=1, col=2)
        apply_theme(fig_gen, title="", height=300)
        fig_gen.update_yaxes(title_text="TR (0–1)", gridcolor='#1a2540', row=1, col=1)
        fig_gen.update_yaxes(title_text="kg HC/ton rock", gridcolor='#1a2540', row=1, col=2)
        st.plotly_chart(fig_gen, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 8 — BURIAL HISTORY SIMULATOR
# ═══════════════════════════════════════════════════════════════
elif menu == "Burial History":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">1D Basin Modelling · Thermal Evolution</div>
            <div class="page-title">Burial History Simulator</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    bh_left, bh_right = st.columns([1, 2])

    with bh_left:
        st.markdown('<div class="section-header">Well Selection</div>', unsafe_allow_html=True)
        bh_well  = st.selectbox("Select Well", df['Well'].tolist(), key='bh_well')
        bh_ref   = df[df['Well'] == bh_well].iloc[0]

        st.markdown('<div class="section-header">Thermal Parameters</div>', unsafe_allow_html=True)
        paleo_ht    = st.slider("Paleo Heat Flow (mW/m²)",  40, 120, 75, step=5)
        present_ht  = st.slider("Present Heat Flow (mW/m²)", 40, 100, 60, step=5)
        erosion_m   = st.slider("Eroded Section (m)",         0, 2000, 500, step=50)
        depo_age    = st.slider("Deposition Age (Ma)",         300, 420, 375, step=5)
        surface_T   = st.slider("Surface Temp (°C)",           10,  30,  20, step=1)

        st.markdown('<div class="section-header">Compaction</div>', unsafe_allow_html=True)
        phi0   = st.slider("Initial Porosity (%)",  30, 60, 45, step=1)
        c_coef = st.slider("Compaction Coeff (km⁻¹)", 0.2, 1.0, 0.5, step=0.05)

    with bh_right:
        # ── Time axis ──
        time_ma    = np.linspace(depo_age, 0, 500)          # Ma (old→present)
        age_fwd    = depo_age - time_ma                      # time elapsed since deposition

        # ── Burial curve: linear subsidence + erosion pulse ──
        subsid_rate = (bh_ref['Thickness'] + erosion_m) / depo_age   # m/Ma
        depth_burial = subsid_rate * age_fwd
        # Add erosion pulse at ~100 Ma
        erosion_pulse = erosion_m * np.exp(-((time_ma - 100)**2) / (2 * 50**2))
        depth_m       = np.clip(depth_burial - erosion_pulse, 0, None)

        # ── Heat flow linear interpolation ──
        hf = paleo_ht + (present_ht - paleo_ht) * (age_fwd / depo_age)

        # ── BHT (simple conductive gradient) ──
        grad = hf / 1000 / 2.5 * 1000   # °C/km  (hf mW/m², TC=2.5 W/mK)
        bht  = surface_T + grad * depth_m / 1000

        # ── Easy%Ro (simplified Sweeney & Burnham) ──
        # Use cumulative temperature proxy
        easy_ro = 0.2 * np.exp(0.0078 * bht)
        easy_ro = np.clip(easy_ro, 0.2, 5.0)

        # ── Porosity with depth ──
        phi_z = (phi0/100) * np.exp(-c_coef * depth_m / 1000)

        # ── Oil generation window flag ──
        oil_gen_mask = (easy_ro >= 0.6) & (easy_ro <= 1.35)

        # ── PLOT 1: Burial + Temperature ──
        fig_bh = make_subplots(rows=1, cols=3,
                               subplot_titles=['Burial Curve', 'Thermal History', 'Vitrinite Reflectance'],
                               specs=[[{"type":"scatter"},{"type":"scatter"},{"type":"scatter"}]],
                               horizontal_spacing=0.06)

        # Burial curve
        fig_bh.add_trace(go.Scatter(
            x=time_ma, y=depth_m,
            mode='lines', line=dict(color='#4499ff', width=2),
            fill='tozeroy', fillcolor='rgba(68,153,255,0.08)',
            name='Depth', hovertemplate='Age: %{x:.0f} Ma<br>Depth: %{y:.0f} m<extra></extra>',
        ), row=1, col=1)
        # Oil window depth band
        for t_idx in np.where(np.diff(oil_gen_mask.astype(int)))[0]:
            fig_bh.add_vline(x=time_ma[t_idx], line_dash='dot',
                             line_color='#f0c040', opacity=0.4, row=1, col=1)

        # Thermal history
        fig_bh.add_trace(go.Scatter(
            x=time_ma, y=bht,
            mode='lines', line=dict(color='#ff4444', width=2),
            fill='tozeroy', fillcolor='rgba(255,68,68,0.07)',
            name='BHT', hovertemplate='Age: %{x:.0f} Ma<br>BHT: %{y:.1f}°C<extra></extra>',
        ), row=1, col=2)
        for thresh, lbl, clr in [(60,'Early Gen','#f0c04088'),(120,'Peak Oil','#00d4aa88'),(150,'Gas Zone','#ff440088')]:
            fig_bh.add_hline(y=thresh, line_dash='dash', line_color=clr, opacity=0.6,
                             annotation_text=lbl, annotation_position='right',
                             annotation_font=dict(size=9, color=clr), row=1, col=2)

        # Ro curve
        fig_bh.add_trace(go.Scatter(
            x=time_ma, y=easy_ro,
            mode='lines', line=dict(color='#f0c040', width=2.5),
            name='Ro', hovertemplate='Age: %{x:.0f} Ma<br>Ro: %{y:.2f}%<extra></extra>',
        ), row=1, col=3)
        # Oil window band
        fig_bh.add_hrect(y0=0.6, y1=1.35, fillcolor='rgba(0,212,170,0.08)',
                         line_width=0, row=1, col=3)
        fig_bh.add_hrect(y0=1.35, y1=2.0, fillcolor='rgba(255,140,0,0.08)',
                         line_width=0, row=1, col=3)
        for ro_v, lbl, c in [(0.6,'Oil Window','#00d4aa'),(1.35,'Wet Gas','#ff8c00'),(2.0,'Dry Gas','#ff4444')]:
            fig_bh.add_hline(y=ro_v, line_dash='dot', line_color=c, opacity=0.5,
                             annotation_text=lbl, annotation_font=dict(size=8, color=c),
                             annotation_position='right', row=1, col=3)
        # Mark present-day Ro from data
        fig_bh.add_trace(go.Scatter(
            x=[0], y=[bh_ref['Ro_calc']],
            mode='markers', marker=dict(size=12, color='#ff4444', symbol='star',
                                         line=dict(color='white', width=1.5)),
            name=f"Measured Ro ({bh_ref['Ro_calc']:.2f}%)", showlegend=True,
            hovertemplate=f"Measured Ro: {bh_ref['Ro_calc']:.2f}%<extra></extra>",
        ), row=1, col=3)

        apply_theme(fig_bh, title=f"Burial & Thermal History — {bh_well}", height=420)
        fig_bh.update_xaxes(title_text="Age (Ma)", autorange='reversed',
                            gridcolor='#1a2540', tickfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'))
        fig_bh.update_yaxes(title_text="Depth (m)", autorange='reversed',
                            gridcolor='#1a2540', tickfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'),
                            row=1, col=1)
        fig_bh.update_yaxes(title_text="BHT (°C)", gridcolor='#1a2540',
                            tickfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'),
                            row=1, col=2)
        fig_bh.update_yaxes(title_text="Ro (%)", gridcolor='#1a2540',
                            tickfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'),
                            row=1, col=3)
        st.plotly_chart(fig_bh, use_container_width=True)

        # ── PLOT 2: Porosity evolution + heat flow ──
        fig_bh2 = make_subplots(rows=1, cols=2,
                                subplot_titles=['Porosity Evolution', 'Heat Flow History'],
                                specs=[[{"type":"scatter"},{"type":"scatter"}]])
        fig_bh2.add_trace(go.Scatter(
            x=time_ma, y=phi_z * 100,
            mode='lines', line=dict(color='#aa66ff', width=2),
            fill='tozeroy', fillcolor='rgba(170,102,255,0.08)',
            name='Porosity', hovertemplate='Age: %{x:.0f} Ma<br>φ: %{y:.1f}%<extra></extra>',
        ), row=1, col=1)
        fig_bh2.add_trace(go.Scatter(
            x=time_ma, y=hf,
            mode='lines', line=dict(color='#ff8c00', width=2),
            fill='tozeroy', fillcolor='rgba(255,140,0,0.07)',
            name='HF', hovertemplate='Age: %{x:.0f} Ma<br>HF: %{y:.0f} mW/m²<extra></extra>',
        ), row=1, col=2)
        apply_theme(fig_bh2, title="", height=300)
        fig_bh2.update_xaxes(title_text="Age (Ma)", autorange='reversed',
                             gridcolor='#1a2540', tickfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'))
        fig_bh2.update_yaxes(title_text="Porosity (%)", gridcolor='#1a2540',
                             tickfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'), row=1, col=1)
        fig_bh2.update_yaxes(title_text="Heat Flow (mW/m²)", gridcolor='#1a2540',
                             tickfont=dict(family='Share Tech Mono', size=9, color='#8a9ab5'), row=1, col=2)
        st.plotly_chart(fig_bh2, use_container_width=True)

        # ── Present-day summary strip ──
        present_depth = depth_m[-1]
        present_bht   = bht[-1]
        present_ro    = easy_ro[-1]
        present_phi   = phi_z[-1] * 100
        sb1, sb2, sb3, sb4 = st.columns(4)
        sb1.metric("Present Depth",  f"{present_depth:.0f} m")
        sb2.metric("Present BHT",    f"{present_bht:.1f} °C")
        sb3.metric("Modelled Ro",    f"{present_ro:.2f} %")
        sb4.metric("Present φ",      f"{present_phi:.1f} %")


# ═══════════════════════════════════════════════════════════════
#  PAGE 9 — PDF REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════
elif menu == "PDF Report":
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-subtitle">Automated Technical Documentation</div>
            <div class="page-title">PDF Report Generator</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pr_left, pr_right = st.columns([1, 1.6])

    with pr_left:
        st.markdown('<div class="section-header">Report Configuration</div>', unsafe_allow_html=True)
        report_title    = st.text_input("Report Title",    "SBAA Basin — Source Rock Characterisation")
        report_author   = st.text_input("Author",          "Serhoudji Souhil")
        report_company  = st.text_input("Company / Inst.", "University · MSc Petroleum Geology")
        report_date     = st.text_input("Date",            "2024")
        report_abstract = st.text_area("Abstract",
            "Integrated characterization of the Upper Devonian source rock "
            "in the SBAA Basin using Rock-Eval pyrolysis, stratigraphic "
            "analysis and geochemical cross-plot techniques. Maturity "
            "assessed using the Jarvie (2007) Ro proxy model.",
            height=110)

        st.markdown('<div class="section-header">Sections to Include</div>', unsafe_allow_html=True)
        inc_summary  = st.checkbox("Executive Summary",          True)
        inc_table    = st.checkbox("Well Data Table",            True)
        inc_stats    = st.checkbox("Statistical Summary",        True)
        inc_maturity = st.checkbox("Maturity Classification",    True)
        inc_hc       = st.checkbox("HC Potential Classification",True)
        inc_methods  = st.checkbox("Methodology Notes",          True)

        generate_btn = st.button("⚙  Generate HTML Report", use_container_width=True)

    with pr_right:
        st.markdown('<div class="section-header">Report Preview</div>', unsafe_allow_html=True)

        # ── Always show live preview ──
        stat_rows = ""
        if inc_stats:
            for col_n, label in [('TOC','TOC (%)'),('S2','S2 (mg/g)'),
                                  ('Tmax','Tmax (°C)'),('HI','HI'),('Ro_calc','Ro (%)')]:
                stat_rows += f"""
                <tr>
                  <td>{label}</td>
                  <td>{df[col_n].mean():.2f}</td>
                  <td>{df[col_n].std():.2f}</td>
                  <td>{df[col_n].min():.2f}</td>
                  <td>{df[col_n].max():.2f}</td>
                </tr>"""

        well_rows = ""
        if inc_table:
            for _, row in df.iterrows():
                well_rows += f"""
                <tr>
                  <td><strong>{row['Well']}</strong></td>
                  <td>{row['Thickness']}</td>
                  <td>{row['TOC']:.2f}</td>
                  <td>{row['S2']:.2f}</td>
                  <td>{row['Tmax']}</td>
                  <td>{row['HI']}</td>
                  <td>{row['OI']}</td>
                  <td>{row['Ro_calc']:.2f}</td>
                  <td>{row['HC_Potential']}</td>
                  <td>{row['Maturity']}</td>
                </tr>"""

        mat_rows = ""
        if inc_maturity:
            for cat, cnt in df['Maturity'].value_counts().items():
                wells = ', '.join(df[df['Maturity']==cat]['Well'].tolist())
                mat_rows += f"<tr><td>{cat}</td><td>{cnt}</td><td>{wells}</td></tr>"

        hc_rows = ""
        if inc_hc:
            for cat, cnt in df['HC_Potential'].value_counts().items():
                wells = ', '.join(df[df['HC_Potential']==cat]['Well'].tolist())
                hc_rows += f"<tr><td>{cat}</td><td>{cnt}</td><td>{wells}</td></tr>"

        html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{report_title}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');
  :root {{
    --gold: #c8982a; --teal: #00a07a; --bg: #04080f; --card: #0c1424;
    --text: #e8eaf0; --muted: #8a9ab5; --border: #1a2540;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Barlow Condensed',sans-serif;
          font-size:14px; line-height:1.6; padding:40px; }}
  .cover {{ text-align:center; padding:60px 20px; border-bottom:2px solid var(--gold);
            margin-bottom:40px; position:relative; }}
  .cover::before {{ content:''; position:absolute; inset:0;
    background:radial-gradient(ellipse at center, rgba(200,152,42,0.08) 0%, transparent 70%); }}
  .cover-logo {{ font-size:3rem; margin-bottom:8px; }}
  .cover-title {{ font-size:2.2rem; font-weight:700; color:var(--gold); letter-spacing:0.1em;
                  text-transform:uppercase; line-height:1.2; margin-bottom:12px; }}
  .cover-sub {{ font-size:1rem; color:var(--muted); letter-spacing:0.15em;
                text-transform:uppercase; margin-bottom:24px; }}
  .cover-meta {{ display:inline-block; background:var(--card); border:1px solid var(--border);
                 border-radius:6px; padding:16px 32px; }}
  .cover-meta p {{ margin:4px 0; color:var(--muted); font-size:0.85rem; }}
  .cover-meta strong {{ color:var(--text); }}
  h2 {{ font-size:1.3rem; font-weight:700; color:var(--gold); letter-spacing:0.12em;
        text-transform:uppercase; margin:36px 0 12px;
        padding-bottom:6px; border-bottom:1px solid var(--border);
        display:flex; align-items:center; gap:10px; }}
  h2::before {{ content:''; width:4px; height:16px; background:var(--gold); border-radius:2px; }}
  p {{ color:var(--muted); margin-bottom:12px; font-size:0.95rem; }}
  table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:0.8rem; }}
  th {{ background:var(--card); color:var(--gold); font-family:'Share Tech Mono',monospace;
        font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase;
        padding:8px 10px; border:1px solid var(--border); text-align:left; }}
  td {{ padding:7px 10px; border:1px solid var(--border); color:var(--text); }}
  tr:hover td {{ background:rgba(200,152,42,0.04); }}
  .badge {{ display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.7rem;
            font-weight:600; letter-spacing:0.1em; text-transform:uppercase;
            font-family:'Share Tech Mono',monospace; }}
  .footer {{ margin-top:60px; padding-top:20px; border-top:1px solid var(--border);
             text-align:center; color:var(--muted); font-size:0.75rem;
             font-family:'Share Tech Mono',monospace; letter-spacing:0.15em; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin:16px 0; }}
  .kpi-card {{ background:var(--card); border:1px solid var(--border);
               border-top:2px solid var(--gold); border-radius:4px; padding:12px; }}
  .kpi-val {{ font-size:1.4rem; font-weight:700; color:var(--gold);
              font-family:'Share Tech Mono',monospace; }}
  .kpi-lbl {{ font-size:0.65rem; color:var(--muted); text-transform:uppercase;
              letter-spacing:0.12em; margin-top:2px; }}
  code {{ background:var(--card); color:var(--teal); padding:2px 6px; border-radius:3px;
          font-family:'Share Tech Mono',monospace; }}
</style>
</head>
<body>

<div class="cover">
  <div class="cover-logo">⛽</div>
  <div class="cover-title">{report_title}</div>
  <div class="cover-sub">PetroStream Ultra 2.0 · Automated Technical Report</div>
  <div class="cover-meta">
    <p><strong>{report_author}</strong></p>
    <p>{report_company}</p>
    <p>Generated: {report_date}</p>
    <p>Basin: SBAA · Formation: Upper Devonian (Frasnian)</p>
  </div>
</div>

{'<h2>Abstract</h2><p>' + report_abstract + '</p>' if inc_summary else ''}

<div class="kpi-grid">
  <div class="kpi-card"><div class="kpi-val">{len(df)}</div><div class="kpi-lbl">Wells Logged</div></div>
  <div class="kpi-card"><div class="kpi-val">{df['TOC'].mean():.2f}%</div><div class="kpi-lbl">Avg TOC</div></div>
  <div class="kpi-card"><div class="kpi-val">{df['Tmax'].mean():.0f}°C</div><div class="kpi-lbl">Avg Tmax</div></div>
  <div class="kpi-card"><div class="kpi-val">{df['Ro_calc'].mean():.2f}%</div><div class="kpi-lbl">Avg Ro</div></div>
  <div class="kpi-card"><div class="kpi-val">{df['Thickness'].max()}m</div><div class="kpi-lbl">Max Thickness</div></div>
</div>

{'<h2>Well Data Table</h2><table><thead><tr><th>Well</th><th>Thick (m)</th><th>TOC (%)</th><th>S2</th><th>Tmax (°C)</th><th>HI</th><th>OI</th><th>Ro (%)</th><th>HC Potential</th><th>Maturity</th></tr></thead><tbody>' + well_rows + '</tbody></table>' if inc_table else ''}

{'<h2>Statistical Summary</h2><table><thead><tr><th>Parameter</th><th>Mean</th><th>Std Dev</th><th>Min</th><th>Max</th></tr></thead><tbody>' + stat_rows + '</tbody></table>' if inc_stats else ''}

{'<h2>Maturity Classification</h2><table><thead><tr><th>Maturity Stage</th><th>Well Count</th><th>Wells</th></tr></thead><tbody>' + mat_rows + '</tbody></table>' if inc_maturity else ''}

{'<h2>HC Potential Classification</h2><table><thead><tr><th>HC Potential</th><th>Well Count</th><th>Wells</th></tr></thead><tbody>' + hc_rows + '</tbody></table>' if inc_hc else ''}

{'<h2>Methodology Notes</h2><p>Maturity was assessed using the Jarvie (2007) Ro proxy: <code>Ro = 0.018 × Tmax − 7.16</code>. Hydrocarbon potential was classified according to Peters &amp; Cassa (1994) TOC thresholds. Spatial interpolation used cubic spline gridding. HC generation transformation ratio estimated following Pepper &amp; Corvi (1995).</p>' if inc_methods else ''}

<div class="footer">
  PETROSTREAM ULTRA 2.0 · © {report_date} {report_author} · SBAA BASIN ANALYSIS
</div>
</body>
</html>"""

        # Show live preview in expander
        with st.expander("  Live HTML Preview (scroll to inspect)", expanded=True):
            st.components.v1.html(html_report, height=600, scrolling=True)

        if generate_btn:
            st.success(" Report ready — click Download below")

        st.download_button(
            label="⬇  Download HTML Report",
            data=html_report.encode('utf-8'),
            file_name=f"PetroStream_Report_{report_date}.html",
            mime="text/html",
            use_container_width=True,
        )

        st.markdown("""
        <div style="background:rgba(0,212,170,0.06);border:1px solid #005a46;border-left:3px solid #00d4aa;
                    border-radius:4px;padding:10px 14px;margin-top:12px;
                    font-family:'Barlow Condensed',sans-serif;font-size:0.85rem;color:#8a9ab5;">
         <strong style="color:#00d4aa;">Tip:</strong>
        Open the downloaded .html file in any browser and use <strong>File → Print → Save as PDF</strong>
        for a pixel-perfect PDF with the dark theme preserved.
        </div>
        """, unsafe_allow_html=True)
