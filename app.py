import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import plotly.graph_objects as go

# --- 1. App Configuration ---
st.set_page_config(page_title="PetroStream Ultra 2.0 Premium", layout="wide")

# --- 2. Data Loading (V.14 SBAA Dataset) ---
@st.cache_data
def load_data():
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
    
    # --- NEW: Phase 1 Physics Calculations ---
    # 1. Calculated Vitrinite Reflectance (Ro %) - Jarvie et al. (2007)
    df['Ro_calc'] = (0.018 * df['Tmax']) - 7.16
    
    # 2. Potential Yield (PY) in mg HC/g rock
    df['PY'] = df['COT'] * 0.1 + df['S2']
    
    # 3. Transformation Ratio (TR) - Simple estimate based on Tmax
    df['TR'] = np.clip((df['Tmax'] - 435) / (470 - 435), 0, 1)
    
    return df

df = load_data()

# --- 3. Sidebar & Navigation ---
st.sidebar.title("PetroStream Ultra 2.0")
menu = st.sidebar.radio("Navigation", ["Basin Dashboard", "Advanced Analytics", "3D Isopach Mapping"])
search_well = st.sidebar.selectbox("🔍 Search Well", ["All Wells"] + list(df['Well']))

# --- 4. Module: Advanced Analytics (Maturity & Yield) ---
if menu == "Advanced Analytics":
    st.header("Phase 1: Reservoir Maturity & Yield Modeling")
    
    # Display specialized metrics
    col1, col2, col3 = st.columns(3)
    target_df = df if search_well == "All Wells" else df[df['Well'] == search_well]
    
    col1.metric("Avg Ro Equivalent", f"{target_df['Ro_calc'].mean():.2f} %")
    col2.metric("Avg Transformation Ratio", f"{target_df['TR'].mean()*100:.1f} %")
    col3.metric("Avg Potential Yield", f"{target_df['PY'].mean():.2f} mg/g")

    st.markdown("---")
    
    # Ro vs Tmax Correlation Chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df['Tmax'], df['Ro_calc'], c=df['Ro_calc'], cmap='hot_r', edgecolors='black')
    ax.set_xlabel("Tmax (°C)")
    ax.set_ylabel("Calculated Ro (%)")
    ax.set_title("Thermal Maturity Conversion (Jarvie Method)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# --- 5. Module: 3D Isopach Mapping (Phase 2 Preview) ---
elif menu == "3D Isopach Mapping":
    st.header("SBAA Basin: 3D Stratigraphic Surface")
    
    # Create grid for 3D
    xi = np.linspace(df.X.min()-1, df.X.max()+1, 50)
    yi = np.linspace(df.Y.min()-1, df.Y.max()+1, 50)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((df.X, df.Y), df.Thickness, (xi, yi), method='cubic')

    # Plotly 3D Surface
    fig = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi, colorscale='Viridis')])
    fig.update_layout(title='Upper Devonian Thickness Surface', autosize=False,
                      width=800, height=800,
                      margin=dict(l=65, r=50, b=65, t=90))
    st.plotly_chart(fig, use_container_width=True)

# (Dashboard code remains consistent with previous versions)
elif menu == "Basin Dashboard":
    st.header("Basin Registry & QC")
    st.dataframe(df.style.background_gradient(subset=['Ro_calc', 'PY'], cmap='YlOrRd'))
