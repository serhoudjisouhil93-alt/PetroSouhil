import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from fpdf import FPDF
import io

# 1. Page Configuration
st.set_page_config(page_title="PetroStream Ultra", layout="wide")

# 2. Professional Styling (CSS)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #004c6d; }
    .stButton>button { width: 100%; background-color: #004c6d; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Loading (V.14 SBAA Dataset)
@st.cache_data
def load_data():
    data = {
        'Well': ['SBAA-1', 'DECH-1', 'OTLA-1', 'BDW-1', 'ODZ-1', 'OTRT-1', 'LT-1bis', 'MGR-1'],
        'X': [10, 25, 15, 35, 30, 5, 12, 20],  # Example UTM-style Coords
        'Y': [50, 65, 55, 75, 70, 45, 48, 52],
        'Thickness': [70, 68, 54, 48, 185, 188, 173, 253],
        'COT': [1.44, 2.65, 1.49, 0.57, 5.74, 0.97, 0.61, 0.71],
        'S2': [4.39, 16.04, 6.91, 2.04, 4.06, 0.79, 0.43, 1.88],
        'Tmax': [446, 440, 437, 460, 445, 452, 443, 454]
    }
    df = pd.DataFrame(data)
    df['HI'] = (df['S2'] / df['COT']) * 100
    return df

df = load_data()

# 4. Navigation Sidebar
st.sidebar.title("PetroStream Ultra")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Geochemical Plots", "Isopach Map"])

# 5. Dashboard Module
if menu == "Dashboard":
    st.header("Basin Executive Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg TOC", f"{df['COT'].mean():.2f}%")
    c2.metric("Max Thickness", f"{df['Thickness'].max()}m")
    c3.metric("Maturity", "Oil Window")
    c4.metric("Status", "V.14 Stable")
    
    st.subheader("Raw Geological Data")
    st.dataframe(df, use_container_width=True)

# 6. Geochemical Module
elif menu == "Geochemical Plots":
    st.header("Source Rock Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### TOC vs S2 (Potential)")
        fig, ax = plt.subplots()
        ax.scatter(df['COT'], df['S2'], c='#004c6d', edgecolors='white')
        ax.set_xlabel("TOC (%)"); ax.set_ylabel("S2 (mg HC/g)")
        st.pyplot(fig)

    with col2:
        st.write("### HI vs Tmax (Maturity)")
        fig, ax = plt.subplots()
        ax.scatter(df['Tmax'], df['HI'], c='#d4a017', edgecolors='black')
        ax.axvline(435, color='red', linestyle='--')
        ax.set_xlabel("Tmax (°C)"); ax.set_ylabel("HI")
        st.pyplot(fig)

# 7. Isopach Mapping Module
elif menu == "Isopach Map":
    st.header("Lithostratigraphic Interpolation")
    grid_x, grid_y = np.mgrid[df.X.min()-5:df.X.max()+5:100j, df.Y.min()-5:df.Y.max()+5:100j]
    grid_z = griddata(df[['X', 'Y']].values, df['Thickness'].values, (grid_x, grid_y), method='cubic')

    fig, ax = plt.subplots(figsize=(10, 8))
    cp = ax.contourf(grid_x, grid_y, grid_z, levels=15, cmap='viridis')
    plt.colorbar(cp, label='Thickness (m)')
    ax.scatter(df['X'], df['Y'], c='white', edgecolors='black', marker='^', s=100)
    for i, txt in enumerate(df['Well']):
        ax.annotate(txt, (df['X'][i], df['Y'][i]), fontsize=9)
    st.pyplot(fig)
