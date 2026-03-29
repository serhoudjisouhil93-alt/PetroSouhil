import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import io

# --- 1. App Configuration ---
st.set_page_config(page_title="PetroStream Ultra", layout="wide")

# --- 2. Professional UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 5px; border: 1px solid #dee2e6; }
    h1, h2, h3 { color: #002b36; font-family: 'Arial'; }
    .stButton>button { background-color: #004c6d; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar: Data Management ---
st.sidebar.title("PetroStream Ultra")
st.sidebar.subheader("Data Management")

# --- NEW: Download Demo Template Feature ---
demo_data = """Well,X,Y,Thickness,COT,S2,Tmax
SBAA-1,10,50,70,1.44,4.39,446
DECH-1,25,65,68,2.65,16.04,440
OTLA-1,15,55,54,1.49,6.91,437
BDW-1,35,75,48,0.57,2.04,460
ODZ-1,30,70,185,5.74,4.06,445
OTRT-1,5,45,188,0.97,0.79,452
LT-1bis,12,48,173,0.61,0.43,443
MGR-1,20,52,253,0.71,1.88,454"""

st.sidebar.download_button(
    label="Download Demo CSV Template",
    data=demo_data,
    file_name="petrostream_template.csv",
    mime="text/csv"
)

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload Your Basin Data", type=["csv", "xlsx"])

# Function to load data
def load_data():
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            else:
                return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    else:
        # Fallback to internal demo data
        return pd.read_csv(io.StringIO(demo_data))

df = load_data()

if df is not None:
    # Calculations
    df['HI'] = (df['S2'] / df['COT']) * 100

    # --- 4. Navigation ---
    menu = st.sidebar.radio("Analysis Modules", ["Executive Summary", "Geochemical Cards", "Isopach Interpolation"])

    # --- 5. Module: Executive Summary ---
    if menu == "Executive Summary":
        st.header("SBAA Basin Overview")
        m1, m2, m3 = st.columns(3)
        m1.metric("Average TOC", f"{df['COT'].mean():.2f}%")
        m2.metric("Max Thickness", f"{df['Thickness'].max()} m")
        m3.metric("Well Count", len(df))
        
        st.subheader("Active Reservoir Dataset")
        st.dataframe(df, use_container_width=True)

    # --- 6. Module: Geochemical Cards ---
    elif menu == "Geochemical Cards":
        st.header("Source Rock Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Generative Potential (TOC vs S2)")
            fig, ax = plt.subplots()
            ax.scatter(df['COT'], df['S2'], c='#004c6d', s=100, edgecolors='white', alpha=0.8)
            ax.set_xlabel("TOC (%)"); ax.set_ylabel("S2 (mg HC/g rock)")
            ax.grid(True, linestyle=':', alpha=0.6)
            st.pyplot(fig)

        with col2:
            st.write("### Thermal Maturity (HI vs Tmax)")
            fig, ax = plt.subplots()
            ax.scatter(df['Tmax'], df['HI'], c='#d4a017', s=100, edgecolors='black')
            ax.axvline(435, color='red', linestyle='--', label='Oil Window')
            ax.set_xlabel("Tmax (°C)"); ax.set_ylabel("HI (mg HC/g TOC)")
            ax.grid(True, linestyle=':', alpha=0.6)
            st.pyplot(fig)

    # --- 7. Module: Isopach Interpolation ---
    elif menu == "Isopach Interpolation":
        st.header("Advanced Isopach Mapping")
        
        xi = np.linspace(df.X.min()-5, df.X.max()+5, 100)
        yi = np.linspace(df.Y.min()-5, df.Y.max()+5, 100)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata((df.X, df.Y), df.Thickness, (xi, yi), method='cubic')

        fig, ax = plt.subplots(figsize=(10, 8))
        contour = ax.contourf(xi, yi, zi, levels=15, cmap='viridis')
        plt.colorbar(contour, label='Thickness (m)')
        ax.scatter(df.X, df.Y, c='white', marker='^', edgecolors='black', s=150)
        
        for i, txt in enumerate(df.Well):
            ax.annotate(txt, (df.X[i], df.Y[i]), fontsize=10, fontweight='bold', xytext=(5,5), textcoords='offset points')
        
        st.pyplot(fig)
else:
    st.warning("Please upload a valid data file to begin analysis.")
