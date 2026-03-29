import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import plotly.graph_objects as go
import lasio
import io
from fpdf import FPDF

# --- 1. App Configuration ---
st.set_page_config(page_title="PetroStream Ultra 2.0 | Serhoudji Souhil", layout="wide")

# --- 2. Professional CSS ---
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
    </style>
    """, unsafe_allow_html=True)

# --- 3. Dataset Engine ---
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

# --- 4. PDF Report Generator Function ---
def create_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="PetroStream Ultra 2.0 - Basin Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Lead Developer: Serhoudji Souhil", ln=True, align='C')
    pdf.ln(10)
    
    # Add Table Header
    pdf.set_font("Arial", 'B', 8)
    cols = ['Well', 'Thickness', 'COT', 'Tmax', 'Ro_calc']
    for col in cols:
        pdf.cell(35, 10, col, 1)
    pdf.ln()
    
    # Add Data
    pdf.set_font("Arial", size=8)
    for index, row in dataframe.iterrows():
        for col in cols:
            pdf.cell(35, 10, str(row[col]), 1)
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

# --- 5. Sidebar Branding & Export ---
st.sidebar.title("PetroStream Ultra 2.0")
st.sidebar.subheader("Serhoudji Souhil")
st.sidebar.markdown("*Master's Student | Petroleum Geology*")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Project Hub", 
    ["Home: Project Overview", "Basin Registry", "Geochemical Analytics", "3D Mapping", "Log Viewer"])

# PDF Export Button
st.sidebar.markdown("### 📄 Reporting")
pdf_data = create_pdf(df)
st.sidebar.download_button(
    label="Download Basin PDF Report",
    data=pdf_data,
    file_name="SBAA_Basin_Report.pdf",
    mime="application/pdf"
)

# --- 6. Modules ---
if menu == "Home: Project Overview":
    st.title("Project Overview: SBAA Basin Analysis")
    st.header("1. Abstract")
    st.write("""
    Characterization of the **Upper Devonian source rock** within the **SBAA Basin** using integrated 
    Rock-Eval and stratigraphic data. Lead Developer: **Serhoudji Souhil**.
    """)
    st.header("2. Methodology")
    st.info("Utilizing Jarvie (2007) maturity modeling and Cubic Spline interpolation.")

elif menu == "Basin Registry":
    st.title("Integrated Reservoir Registry")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg TOC", f"{df['COT'].mean():.2f}%")
    c2.metric("Max Thickness", f"{df['Thickness'].max()}m")
    c3.metric("Avg Ro", f"{df['Ro_calc'].mean():.2f}%")
    c4.metric("Wells", len(df))
    st.dataframe(df.round(2).style.background_gradient(cmap='YlGnBu'), use_container_width=True)

# ... [Geochemical, 3D Mapping, and Log Viewer code remains identical to previous version] ...
