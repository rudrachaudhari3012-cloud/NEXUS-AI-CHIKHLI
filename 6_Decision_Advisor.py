import streamlit as st
from nexus_common import page_header

st.set_page_config(page_title="NEXUS | Decision Advisor", page_icon="🧭", layout="wide")
page_header("Decision Advisor", "General information prompts based on entered conditions.")
rain=st.number_input("Observed / forecast rainfall (mm)",min_value=0.0,max_value=500.0,value=20.0)
river_trend=st.selectbox("Verified river gauge trend",["Not available","Rising","Stable","Falling"])
st.markdown("### Review checklist")
if rain>=50:
    st.warning("High rainfall amount entered. Check the latest IMD bulletin and district administration updates.")
else:
    st.info("Continue checking official weather updates; this rainfall input alone does not determine flood risk.")
if river_trend=="Rising":
    st.warning("Gauge trend marked rising. Check official local authority advisories.")
elif river_trend=="Not available":
    st.info("No verified live gauge trend is connected. Do not infer river safety from missing data.")
else:
    st.write(f"Entered gauge trend: {river_trend}. Confirm the timestamp and station source.")
st.markdown("- [IMD official API and weather information](https://api.imd.gov.in/public/)")
st.markdown("- [Navsari District official website](https://navsari.nic.in/)")
st.error("This student prototype is not an emergency alert system. Follow official authorities for safety decisions.")
