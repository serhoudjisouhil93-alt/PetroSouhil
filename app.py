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

# Custom Professional CSS
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3b4e, #2e3b4e); color: white; }
    h1 { color: #004c6d; font-family: 'Segoe UI'; border-bottom: 2px solid #d4a017; }
    .stMetric { background-color: white; border: 1px solid #e0e0e0; padding: 10px; border-radius: 10px; }
    footer {visibility: hidden;}
    .reportview-container .main footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Integrated Data Engine ---
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
    # Jarvie (2007) Thermal Maturity Conversion
    df['Ro_calc'] = (0.018 * df['Tmax']) - 7.16
    return df

df = load_v14_data()

# --- 3. Sidebar Navigation & Branding ---
st.sidebar.title("PetroStream Ultra 2.0")
st.sidebar.markdown("**Lead Developer:** \n**Serhoudji Souhil Abderrhaim**")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Analysis Modules", 
    ["Basin Dashboard", "Geochemical Maturity", "3D Sweet Spot Mapping", "Petrophysical Log Viewer"])

# --- 4. Module: Basin Dashboard ---
if menu == "Basin Dashboard":
    st.title("SBAA Basin: Integrated Reservoir Registry")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg TOC", f"{df['COT'].mean():.2f}%")
    col2.metric("Max Thickness", f"{df['Thickness'].max()}m")
    col3.metric("Maturity Range", f"{df['Ro_calc'].min():.2f}-{df['Ro_calc'].max():.2f}% Ro")
    col4.metric("Well Control", len(df))

    st.subheader("Master Dataset (V.14 Stable)")
    st.dataframe(df.style.background_gradient(cmap='YlGnBu'), use_container_width=True)

# --- 5. Module: Geochemical Maturity ---
elif menu == "Geochemical Maturity":
    st.title("Advanced Source Rock Characterization")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("### Kerogen Typing (Van Krevelen)")
        fig, ax = plt.subplots()
        ax.scatter(df['IO'], df['IH'], c=df['Ro_calc'], cmap='plasma', s=100, edgecolors='black')
        ax.set_xlabel("Oxygen Index (OI)"); ax.set_ylabel("Hydrogen Index (HI)")
        st.pyplot(fig)
        
    with c2:
        st.write("### Maturity Trend (Tmax vs Ro)")
        fig, ax = plt.subplots()
        ax.plot(df['Tmax'], df['Ro_calc'], 'r--', alpha=0.5)
        ax.scatter(df['Tmax'], df['Ro_calc'], c='#004c6d', s=100)
        ax.set_xlabel("Tmax (°C)"); ax.set_ylabel("Calculated Ro (%)")
        st.pyplot(fig)

# --- 6. Module: 3D Sweet Spot Mapping ---
elif menu == "3D Sweet Spot Mapping":
    st.title("Exploration Strategy: 3D Sweet Spot Detection")
    
    st.sidebar.subheader("🎯 Screening Criteria")
    min_toc = st.sidebar.slider("Min TOC (%)", 0.0, 6.0, 1.5)
    min_thick = st.sidebar.slider("Min Thickness (m)", 0, 300, 100)
    
    df['is_sweet'] = (df['COT'] >= min_toc) & (df['Thickness'] >= min_thick)
    
    xi = np.linspace(df.X.min()-1, df.X.max()+1, 50)
    yi = np.linspace(df.Y.min()-1, df.Y.max()+1, 50)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((df.X, df.Y), df.Thickness, (xi, yi), method='cubic')

    fig = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi, colorscale='Viridis', opacity=0.7)])
    
    # Plot Sweet Spots
    sweet = df[df['is_sweet']]
    fig.add_trace(go.Scatter3d(x=sweet['X'], y=sweet['Y'], z=sweet['Thickness'], 
                               mode='markers+text', text=sweet['Well'],
                               marker=dict(size=10, color='red', symbol='diamond')))
    
    st.plotly_chart(fig, use_container_width=True)

# --- 7. Module: Petrophysical Log Viewer ---
elif menu == "Petrophysical Log Viewer":
    st.title("Precision Petrophysics (LAS Viewer)")
    las_file = st.sidebar.file_uploader("Upload .LAS File", type=["las"])
    
    if las_file:
        string_io = io.StringIO(las_file.getvalue().decode("utf-8"))
        l = lasio.read(string_io)
        ldf = l.df().reset_index()
        
        st.success(f"Well: {l.well.WELL.value} | Location: {l.well.LOC.value}")
        curves = st.multiselect("Select Logs", ldf.columns, default=ldf.columns[1:3])
        
        fig, axes = plt.subplots(1, len(curves), figsize=(len(curves)*3, 10), sharey=True)
        if len(curves) == 1: axes = [axes]
        for i, col in enumerate(curves):
            axes[i].plot(ldf[col], ldf.iloc[:,0], lw=0.7)
            axes[i].set_title(col); axes[i].invert_yaxis(); axes[i].grid(True)
        st.pyplot(fig)
    else:
        st.info("Upload an LAS file to start log analysis. (Compatible with Petrel/Techlog exports)")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 PetroStream Ultra | Developed by Serhoudji Souhil")
