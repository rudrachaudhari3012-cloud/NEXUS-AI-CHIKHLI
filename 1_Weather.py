import streamlit as st
import pandas as pd
from nexus_common import page_header
from weather_service import get_chikhli_weather, weather_error_message

st.set_page_config(page_title="NEXUS | Chikhli Weather", page_icon="🌦️", layout="wide")
page_header("Chikhli Weather", "Current conditions and a 7-day forecast for Chikhli town.")
if st.button("🔄 Refresh weather"):
    st.cache_data.clear()
data, error = get_chikhli_weather()
if not data:
    st.error(weather_error_message(error))
    st.stop()
cur = data.get("current", {})
st.caption(f"Updated: {cur.get('time','—')} • Asia/Kolkata • Source: Open-Meteo")
metrics = [
    ("Temperature",cur.get("temperature_2m"),"°C"),("Feels like",cur.get("apparent_temperature"),"°C"),
    ("Humidity",cur.get("relative_humidity_2m"),"%"),("Rain",cur.get("rain"),"mm"),
    ("Precipitation",cur.get("precipitation"),"mm"),("Wind",cur.get("wind_speed_10m"),"km/h"),
    ("Wind gust",cur.get("wind_gusts_10m"),"km/h"),("Cloud cover",cur.get("cloud_cover"),"%"),
    ("Pressure",cur.get("pressure_msl"),"hPa")
]
for start in range(0,len(metrics),3):
    cols=st.columns(3)
    for col,(name,val,unit) in zip(cols,metrics[start:start+3]):
        col.metric(name, f"{val if val is not None else '—'} {unit}")
daily=data.get("daily",{})
if daily.get("time"):
    df=pd.DataFrame({
        "Date":daily["time"],"Min temp (°C)":daily.get("temperature_2m_min",[]),
        "Max temp (°C)":daily.get("temperature_2m_max",[]),"Rain (mm)":daily.get("rain_sum",[]),
        "Precipitation (mm)":daily.get("precipitation_sum",[]),
        "Rain chance (%)":daily.get("precipitation_probability_max",[]),
        "Max wind (km/h)":daily.get("wind_speed_10m_max",[])
    })
    st.markdown("### 7-day forecast")
    st.dataframe(df, use_container_width=True, hide_index=True)
st.caption("Forecast is model-based guidance, not a guarantee. Local conditions can vary across Chikhli Taluka.")
