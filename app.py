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

# --- 2. Advanced CSS (Fixes the White Boxes & Branding) ---
st.markdown("""
    <style>
    /* Main Background */
    .main { background-color: #0e1117; color: white; }
    
    /* FIX: Metric Card Styling (Dark text on White cards) */
    [data-testid="stMetricValue"] {
        color: #004c6d !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stMetricLabel"] {
        color: #31333F !important;
        font-weight: bold;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #d4a017; /* Gold Accent */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    
    /* Headers */
    h1, h2, h3 { color: #ffffff; font-family: 'Segoe UI'; }
    .stHeader { border-bottom: 2px solid #d4a017; }
    
    /* Sidebar Styling */
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
    # Geochemical Calculations
    df['Ro_calc'] = ((0.018 * df['Tmax']) - 7.16).round(2)
    return df

df = load_v14_data()

# --- 4. Sidebar: Logo, Navigation & Search ---
# Logo Placeholder (You can replace this URL with your actual logo link)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2843/2843891.png", width=100)
st.sidebar.title("PetroStream Ultra 2.0")
st.sidebar.markdown(f"**Lead Developer:** \n**Serhoudji Souhil**")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Analysis Hub", 
    ["Basin Registry", "Geochemical Analytics", "3D Mapping", "Log Viewer"])

search_well = st.sidebar.selectbox("🔍 Select Well", ["All Wells"] + list(df['Well']))
display_df = df if search_well == "All Wells" else df[df['Well'] == search_well]

# --- 5. Module: Basin Registry (The Cards & Table) ---
if menu == "Basin Registry":
    st.title("SBAA Basin: Integrated Reservoir Registry")
    
    # The Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg TOC", f"{display_df['COT'].mean():.2f}%")
    c2.metric("Max Thickness", f"{display_df['Thickness'].max()}m")
    c3.metric("Maturity (Ro)", f"{display_df['Ro_calc'].mean():.2f}%")
    c4.metric("Well Count", len(display_df))

    st.markdown("### Master Dataset (V.14 Stable)")
    # Rounded values for cleaner display
    st.dataframe(display_df.round(2).style.background_gradient(cmap='YlGnBu'), use_container_width=True)

# --- 6. Module: Geochemical Analytics ---
elif menu == "Geochemical Analytics":
    st.title("Source Rock Characterization")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Kerogen Type (Van Krevelen)")
        fig, ax = plt.subplots()
        ax.scatter(df['IO'], df['IH'], c=df['Ro_calc'], cmap='plasma', s=100, edgecolors='white')
        ax.set_xlabel("Oxygen Index (OI)"); ax.set_ylabel("Hydrogen Index (HI)")
        st.pyplot(fig)
        
    with col2:
        st.write("### Hydrocarbon Potential (S2 vs TOC)")
        fig, ax = plt.subplots()
        ax.scatter(df['COT'], df['S2'], color='#d4a017', s=100, edgecolors='black')
        ax.set_xlabel("TOC (%)"); ax.set_ylabel("S2 (mg HC/g)")
        st.pyplot(fig)

# --- 7. Module: 3D Mapping ---
elif menu == "3D Mapping":
    st.title("SBAA Basin: 3D Stratigraphic Surface")
    
    xi = np.linspace(df.X.min()-1, df.X.max()+1, 50)
    yi = np.linspace(df.Y.min()-1, df.Y.max()+1, 50)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((df.X, df.Y), df.Thickness, (xi, yi), method='cubic')

    fig = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi, colorscale='Viridis')])
    fig.update_layout(scene=dict(zaxis_title='Thickness (m)'), width=800, height=700)
    st.plotly_chart(fig, use_container_width=True)

# --- 8. Module: Log Viewer ---
elif menu == "Log Viewer":
    st.title("Petrophysical LAS Viewer")
    las_file = st.sidebar.file_uploader("Upload .LAS", type=["las"])
