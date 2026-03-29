import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import lasio
import io

# --- 1. App Configuration ---
st.set_page_config(page_title="PetroStream Ultra 2.0", layout="wide")

# --- 2. Sidebar Navigation ---
st.sidebar.title("PetroStream Ultra 2.0")
menu = st.sidebar.radio("Navigation", ["Basin Dashboard", "3D Sweet Spot Mapping", "Petrophysical Log Viewer"])

# --- 3. Module: Petrophysical Log Viewer ---
if menu == "Petrophysical Log Viewer":
    st.header("Well Log Analysis (LAS Integration)")
    
    # File Uploader for LAS
    las_file = st.sidebar.file_uploader("Upload LAS File", type=["las"])
    
    if las_file is not None:
        # Read the uploaded LAS file
        string_io = io.StringIO(las_file.getvalue().decode("utf-8"))
        l = lasio.read(string_io)
        ldf = l.df().reset_index() # Convert to Dataframe
        
        st.success(f"Loaded Well: {l.well.WELL.value}")
        
        # Track Selection
        tracks = st.multiselect("Select Logs to Plot", ldf.columns, default=[ldf.columns[0], ldf.columns[1]])
        
        if tracks:
            fig, axes = plt.subplots(1, len(tracks), figsize=(len(tracks)*3, 10), sharey=True)
            if len(tracks) == 1: axes = [axes] # Handle single plot
            
            for i, col in enumerate(tracks):
                axes[i].plot(ldf[col], ldf['DEPT'], color='blue' if i==0 else 'red', lw=0.5)
                axes[i].set_title(col)
                axes[i].grid(True, alpha=0.3)
                axes[i].invert_yaxis() # Depth should go down
                
            st.pyplot(fig)
    else:
        st.info("Please upload an .LAS file to view well logs. For now, here is a professional log layout example:")
        # Placeholder / Demo Plot
        depth = np.linspace(2000, 2100, 500)
        gr = np.random.normal(60, 15, 500)
        res = np.log10(np.random.uniform(1, 100, 500))
        
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 10), sharey=True)
        ax1.plot(gr, depth, color='green'); ax1.set_title('Gamma Ray (API)'); ax1.invert_yaxis()
        ax2.plot(res, depth, color='red'); ax2.set_title('Resistivity (ohm.m)')
        st.pyplot(f)

# (Previous Dashboard and 3D Mapping modules remain in the script)
