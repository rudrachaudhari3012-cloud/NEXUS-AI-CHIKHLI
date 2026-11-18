import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from nexus_common import page_header
from weather_service import get_chikhli_weather, weather_error_message

st.set_page_config(page_title="NEXUS | Rainfall", page_icon="🌧️", layout="wide")
page_header("Rainfall Analysis — Chikhli", "Hourly precipitation outlook and daily rainfall forecast.")
data,error=get_chikhli_weather()
if not data:
    st.error(weather_error_message(error)); st.stop()
hourly=data.get("hourly",{})
if hourly.get("time"):
    df=pd.DataFrame({
        "Time":hourly["time"],"Rain (mm)":hourly.get("rain",[]),
        "Precipitation (mm)":hourly.get("precipitation",[]),
        "Rain probability (%)":hourly.get("precipitation_probability",[])
    })
    st.markdown("### Next 7 days — hourly data")
    st.dataframe(df.head(48),use_container_width=True,hide_index=True)
    fig=go.Figure()
    fig.add_trace(go.Bar(x=df["Time"][:48],y=df["Precipitation (mm)"][:48],name="Precipitation (mm)"))
    fig.add_trace(go.Scatter(x=df["Time"][:48],y=df["Rain probability (%)"][:48],name="Rain probability (%)",yaxis="y2",mode="lines+markers"))
    fig.update_layout(template="plotly_dark",height=370,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                      yaxis=dict(title="mm"),yaxis2=dict(title="Probability (%)",overlaying="y",side="right",range=[0,100]))
    st.plotly_chart(fig,use_container_width=True)
daily=data.get("daily",{})
if daily.get("time"):
    daily_df=pd.DataFrame({"Date":daily["time"],"Rain (mm)":daily.get("rain_sum",[]),
                           "Total precipitation (mm)":daily.get("precipitation_sum",[]),
                           "Max rain probability (%)":daily.get("precipitation_probability_max",[])})
    st.markdown("### Daily rainfall forecast")
    st.dataframe(daily_df,use_container_width=True,hide_index=True)
st.info("Open-Meteo precipitation is model-based grid data for the Chikhli coordinates. It is not a direct reading from a physical rain gauge.")
