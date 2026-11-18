import streamlit as st
import pandas as pd
from datetime import datetime
from nexus_common import page_header

st.set_page_config(page_title="NEXUS | Ambika River", page_icon="🌊", layout="wide")
page_header("Ambika River — Bilimora", "River-level monitoring workspace for the Ambika River near Bilimora.")
st.info("Live Bilimora gauge feed has not yet been verified/connected. This page does not invent a live river level.")
st.markdown("### River gauge data")
st.write("Enter a measured value only when you have it from an official gauge / authority update. The saved entry is a manual observation, not an automatic live reading.")
with st.form("river_entry"):
    observed_at=st.date_input("Observation date")
    observed_time=st.time_input("Observation time")
    level=st.number_input("Water level (metres)",min_value=0.0,max_value=50.0,value=0.0,step=0.01,format="%.2f")
    source=st.text_input("Measurement source / station name",placeholder="e.g. official gauge station")
    submitted=st.form_submit_button("Add observation")
if submitted:
    if not source.strip() or level <= 0:
        st.error("Please enter a positive measured level and its source.")
    else:
        row={"Date":str(observed_at),"Time":str(observed_time),"Water level (m)":level,"Source":source.strip()}
        st.session_state.setdefault("ambika_observations",[])
        st.session_state["ambika_observations"].append(row)
        st.success("Manual observation added for this session.")
rows=st.session_state.get("ambika_observations",[])
if rows:
    df=pd.DataFrame(rows)
    st.dataframe(df,use_container_width=True,hide_index=True)
    st.download_button("Download observations CSV",df.to_csv(index=False).encode("utf-8"),"ambika_bilimora_manual_observations.csv","text/csv")
else:
    st.caption("No river-level observation has been entered in this session.")
st.markdown("### Official reference links")
st.markdown("- [Gujarat Water Resources Department](https://guj-nwrws.gujarat.gov.in/)")
st.markdown("- [Gujarat State Water Data Centre](https://swhydrology.gujarat.gov.in/)")
st.markdown("- [National Water Data Portal — river telemetry datasets](https://nwdp.nwic.gov.in/dataset/river-water-level-telemetry-hourly-gujarat-surface-water-and-ground-water-department)")
st.warning("A Gujarat river-gauge availability document lists Harangam, Chikhali, on the Ambika River, with records shown only through 2010. That historical listing does not confirm a current live Bilimora feed. Confirm the correct Bilimora gauge and data access with the Water Resources Department before presenting live levels.")
