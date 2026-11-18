import streamlit as st
from nexus_common import page_header

st.set_page_config(page_title="NEXUS | What-if", page_icon="🌦️", layout="wide")
page_header("What-if Simulation", "Explore hypothetical rainfall and Ambika River conditions.")
rain=st.slider("Rainfall change (%)",-50,150,25)
river=st.slider("Starting river-level scenario (m)",0.0,12.0,3.0,0.1)
hours=st.slider("Scenario duration (hours)",1,48,12)
# Explicit illustrative calculation only, not hydrological modelling.
estimated=river + max(0,rain)*0.004*(hours/12)
st.metric("Illustrative scenario level",f"{estimated:.2f} m")
st.caption("Formula: starting level + max(0, rainfall change) × 0.004 × (hours / 12). This is a toy simulation, not a river hydraulics model.")
st.info("For a scientifically meaningful Ambika River model, we need verified gauge time-series, rainfall over the catchment, river cross-sections and calibrated hydrological modelling.")
