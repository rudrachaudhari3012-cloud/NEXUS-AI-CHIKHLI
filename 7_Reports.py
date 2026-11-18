import streamlit as st
import pandas as pd
from nexus_common import page_header
from weather_service import get_chikhli_weather

st.set_page_config(page_title="NEXUS | Reports", page_icon="📄", layout="wide")
page_header("Weather Reports — Chikhli", "Export the latest forecast response available from the weather API.")
data,error=get_chikhli_weather()
if not data:
    st.error(f"Weather data unavailable: {error}")
    st.stop()
daily=data.get("daily",{})
if daily.get("time"):
    df=pd.DataFrame({"Date":daily["time"],"Min temp °C":daily.get("temperature_2m_min",[]),
                     "Max temp °C":daily.get("temperature_2m_max",[]),"Rain mm":daily.get("rain_sum",[]),
                     "Precipitation mm":daily.get("precipitation_sum",[]),
                     "Rain probability %":daily.get("precipitation_probability_max",[])})
    st.dataframe(df,use_container_width=True,hide_index=True)
    st.download_button("⬇️ Download Chikhli forecast CSV",df.to_csv(index=False).encode("utf-8"),"nexus_chikhli_weather_forecast.csv","text/csv")
