import streamlit as st
from nexus_common import page_header
from weather_service import CHIKHLI_LAT,CHIKHLI_LON

st.set_page_config(page_title="NEXUS | Settings", page_icon="⚙️", layout="wide")
page_header("Settings & Data Sources", "Location and connected data providers.")
st.markdown("### Project location")
st.write("Chikhli, Navsari District, Gujarat")
st.write(f"Coordinates used for town-level weather grid: {CHIKHLI_LAT}, {CHIKHLI_LON}")
st.markdown("### Weather provider")
st.markdown("- [Open-Meteo API documentation](https://open-meteo.com/en/docs)")
st.write("Weather values are fetched directly by Python from Open-Meteo. No separate weather-app login is used in this starter project.")
st.markdown("### Official Indian weather information")
st.markdown("- [IMD API portal](https://api.imd.gov.in/public/)")
st.markdown("- [Mausam official website](https://mausam.imd.gov.in/)")
st.markdown("### River information")
st.markdown("- [Gujarat State Water Data Centre](https://swhydrology.gujarat.gov.in/)")
st.markdown("- [National Water Data Portal](https://nwdp.nwic.gov.in/)")
st.caption("To connect a live Ambika River gauge, obtain the exact station/feed/API details from the responsible department.")
