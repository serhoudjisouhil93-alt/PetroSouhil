import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import plotly.graph_objects as go
import lasio
import io

# --- 1. App Configuration & Branding ---
st.set_page_config(page_title="PetroStream Ultra 2.0 | Serhoudji Souhil", layout="wide")

# --- 2. Professional CSS (Fixes White Boxes & Theme) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stMetricValue"] { color: #004c6d !important; }
    [data-testid="stMetricLabel"] { color: #31333F !important; font-weight: bold; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #d4a017;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    h1, h2, h3 { color: #ffffff; font-family: 'Segoe UI'; }
    .stHeader { border-bottom: 2px solid #d4a017; }
    .css-1d391kg { background-color: #1a2433; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Dataset Engine (V.14 Stable) ---
@st.cache_data
def load_v14_data():
    data = {
        'Well': ['SBAA-1', 'DECH-1', 'OTLA-1', 'BDW-1', 'ODZ-1', 'OTRT-1', 'LT-1bis', 'MGR-1'],
        'X': [7.5, 6.5, 1.8, 6.2, 5.8, 4.2, 2.0, 5.9], 
        'Y': [5.5, 7.5, 1.2, 6.1, 5.0, 4.3, 2.1, 4.8],
        'Thickness': [70, 68, 54, 48, 185, 188, 173, 253],
        'COT': [1.44, 2.65, 1.49, 0.57, 5.74, 0.97, 0.61, 0.71],
        'S2': [4.39, 16.04, 6.91, 2.04, 4.06, 0.79, 0.43, 1.88],
        'Tmax': [446, 440, 437, 460, 445, 452, 443, 454],
        'IH': [315, 484, 467, 404, 292, 93, 53, 128],
        'IO': [19, 26, 33, 24, 46, 13, 48, 22]
    }
    df = pd.DataFrame(data)
    df['Ro_calc'] = ((0.018 * df['Tmax']) - 7.16).round(2)
    return df

df = load_v14_data()

# --- 4. Sidebar Branding ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1032/1032821.png", width=80)
st.sidebar.title("PetroStream Ultra 2.0")
st.sidebar.subheader("Serhoudji Souhil")
st.sidebar.markdown("*Master's Student | Petroleum Geology*")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Project Hub", 
    ["Home: Project Overview", "Basin Registry", "Geochemical Analytics", "3D Mapping", "Log Viewer"])

# --- 5. Module: Home (Project Overview) ---
if menu == "Home: Project Overview":
    st.title("Project Overview: SBAA Basin Analysis")
    st.image("https://images.unsplash.com/photo-1581092583537-20d51b4b4f1b?auto=format&fit=crop&q=80&w=1500", use_container_width=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("1. Abstract")
        st.write("""
        This project focuses on the characterization of the **Upper Devonian source rock** within the **SBAA Basin**. 
        By integrating Rock-Eval pyrolysis data, stratigraphic thickness measurements, and digital well logs, 
        **PetroStream Ultra 2.0** provides a high-fidelity environment for evaluating generative potential 
        and thermal maturity.
        """)
        
        st.header("2. Study Area")
        st.write("""
        The dataset consists of **8 key wells** (including SBAA-1 and MGR-1) strategically distributed across 
        the basin to capture lateral variations in organic richness (TOC) and thermal evolution (Tmax).
        """)
    
    with col2:
        st.header("3. Methodology")
        st.info("""
        - **Maturity:** Jarvie et al. (2007) Equation.
        - **Interpolation:** Cubic Spline for Isopach surfaces.
        - **Petrophysics:** LASIO-based curve parsing.
        - **Kerogen:** Van Krevelen classification.
        """)

# --- 6. Module: Basin Registry ---
elif menu == "Basin Registry":
    st.title("Integrated Reservoir Registry")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg TOC", f"{df['COT'].mean():.2f}%")
    c2.metric("Max Thickness", f"{df['Thickness'].max()}m")
    c3.metric("Avg Ro", f"{df['Ro_calc'].mean():.2f}%")
    c4.metric("Wells", len(df))
    st.dataframe(df.round(2).style.background_gradient(cmap='YlGnBu'), use_container_width=True)

# --- 7. Module: Geochemical Analytics ---
elif menu == "Geochemical Analytics":
    st.title("Geochemical Characterization")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Kerogen Type (Van Krevelen)")
        fig, ax = plt.subplots()
        ax.scatter(df['IO'], df['IH'], c=df['Ro_calc'], cmap='plasma', s=100, edgecolors='white')
        ax.set_xlabel("OI"); ax.set_ylabel("HI"); st.pyplot(fig)
    with col2:
        st.write("### Maturity Trend")
        fig, ax = plt.subplots()
        ax.scatter(df['Tmax'], df['Ro_calc'], color='#d4a017', s=100); st.pyplot(fig)

# --- 8. Module: 3D Mapping ---
elif menu == "3D Mapping":
    st.title("3D Isopach Surface")
    xi = np.linspace(df.X.min()-1, df.X.max()+1, 50)
    yi = np.linspace(df.Y.min()-1, df.Y.max()+1, 50)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((df.X, df.Y), df.Thickness, (xi, yi), method='cubic')
    fig = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi, colorscale='Viridis')])
    st.plotly_chart(fig, use_container_width=True)

# --- 9. Module: Log Viewer ---
elif menu == "Log Viewer":
    st.title("LAS Log Viewer")
    las_file = st.sidebar.file_uploader("Upload .LAS", type=["las"])
    if las_file:
        l = lasio.read(io.StringIO(las_file.getvalue().decode("utf-8")))
        ldf = l.df().reset_index()
        curves = st.multiselect("Select Logs", ldf.columns, default=ldf.columns[1:3])
        fig, axes = plt.subplots(1, len(curves), figsize=(len(curves)*3, 10), sharey=True)
        if len(curves) == 1: axes = [axes]
        for i, col in enumerate(curves):
            axes[i].plot(ldf[col], ldf.iloc[:,0], lw=0.7); axes[i].invert_yaxis(); axes[i].grid(True)
        st.pyplot(fig)
    else:
        st.info("Awaiting .LAS file upload.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 PetroStream Ultra | Serhoudji Souhil")
