import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import plotly.graph_objects as go
import io

# --- 1. App Configuration ---
st.set_page_config(page_title="PetroStream Ultra 2.0 Premium", layout="wide")

# --- 2. Data Loading (V.14 SBAA Integrated Dataset) ---
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
    # Physics Calculations from Phase 1
    df['Ro_calc'] = (0.018 * df['Tmax']) - 7.16
    return df

df = load_data()

# --- 3. Sidebar: Sweet Spot Controls ---
st.sidebar.title("PetroStream Ultra 2.0")
menu = st.sidebar.radio("Navigation", ["Basin Dashboard", "3D Sweet Spot Mapping"])

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Sweet Spot Criteria")
min_toc = st.sidebar.slider("Min TOC (%)", 0.0, 10.0, 1.5)
min_thick = st.sidebar.slider("Min Thickness (m)", 0, 300, 100)
temp_range = st.sidebar.slider("Tmax Range (°C)", 400, 500, (435, 460))

# Apply Sweet Spot Logic
df['is_sweet_spot'] = (
    (df['COT'] >= min_toc) & 
    (df['Thickness'] >= min_thick) & 
    (df['Tmax'].between(temp_range[0], temp_range[1]))
)

# --- 4. Module: 3D Sweet Spot Mapping ---
if menu == "3D Sweet Spot Mapping":
    st.header("SBAA Basin: 3D Surface & Sweet Spot Detection")
    
    # Grid for smooth surface
    xi = np.linspace(df.X.min()-1, df.X.max()+1, 50)
    yi = np.linspace(df.Y.min()-1, df.Y.max()+1, 50)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((df.X, df.Y), df.Thickness, (xi, yi), method='cubic')

    # Create 3D Surface
    fig = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi, colorscale='Blues', opacity=0.8, name='Formation Top')])
    
    # Highlight Sweet Spots with Red Stars
    sweet_spots = df[df['is_sweet_spot'] == True]
    non_sweet = df[df['is_sweet_spot'] == False]
    
    fig.add_trace(go.Scatter3d(
        x=sweet_spots['X'], y=sweet_spots['Y'], z=sweet_spots['Thickness'],
        mode='markers+text',
        marker=dict(size=10, color='red', symbol='star'),
        text=sweet_spots['Well'],
        name='Sweet Spot'
    ))
    
    fig.add_trace(go.Scatter3d(
        x=non_sweet['X'], y=non_sweet['Y'], z=non_sweet['Thickness'],
        mode='markers',
        marker=dict(size=5, color='black', symbol='circle'),
        name='Standard Well'
    ))

    fig.update_layout(scene=dict(zaxis_title='Thickness (m)'), width=900, height=700)
    st.plotly_chart(fig, use_container_width=True)
    
    if not sweet_spots.empty:
        st.success(f"Found {len(sweet_spots)} wells matching your Sweet Spot criteria!")
        st.dataframe(sweet_spots[['Well', 'Thickness', 'COT', 'Tmax', 'Ro_calc']])
    else:
        st.warning("No wells match the current Sweet Spot criteria. Adjust sliders to expand search.")

# --- 5. Dashboard (Simplified) ---
elif menu == "Basin Dashboard":
    st.header("Basin Registry & QC")
    st.dataframe(df.style.apply(lambda x: ['background-color: #ffcccc' if x.is_sweet_spot else '' for i in x], axis=1))
