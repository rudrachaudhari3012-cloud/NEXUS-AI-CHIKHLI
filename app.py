import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from nexus_common import apply_theme, page_card, page_header
from weather_service import get_chikhli_weather, weather_error_message

st.set_page_config(page_title="NEXUS ∞ | Chikhli", page_icon="🌐", layout="wide")
apply_theme()

st.markdown("""
<div class="hero">
  <div class="eyebrow">NAVSARI DISTRICT • GUJARAT</div>
  <h1>NEXUS <span>∞</span></h1>
  <h3>Chikhli Local Weather & River Intelligence</h3>
  <p>DETECT → PREDICT → SIMULATE → DECIDE</p>
  <p class="small">Chikhli Taluka • Ambika River, Bilimora monitoring workspace</p>
</div>
""", unsafe_allow_html=True)

st.caption("Weather data is retrieved online from Open-Meteo for Chikhli town coordinates. It may differ from a local rain gauge.")
with st.spinner("Fetching current weather for Chikhli..."):
    weather, error = get_chikhli_weather()

if weather:
    current = weather.get("current", {})
    cols = st.columns(5)
    metrics = [
        ("🌡️ Temperature", current.get("temperature_2m"), "°C"),
        ("💧 Humidity", current.get("relative_humidity_2m"), "%"),
        ("🌧️ Rain", current.get("rain"), "mm"),
        ("🌬️ Wind", current.get("wind_speed_10m"), "km/h"),
        ("☁️ Cloud cover", current.get("cloud_cover"), "%"),
    ]
    for col, (label, value, unit) in zip(cols, metrics):
        col.metric(label, f"{value if value is not None else '—'} {unit}")
    st.caption(f"Weather observation time: {current.get('time', 'Not supplied')} • Timezone: Asia/Kolkata")
    hourly = weather.get("hourly", {})
    if hourly.get("time") and hourly.get("precipitation_probability"):
        chart_df = pd.DataFrame({
            "Time": hourly["time"][:24],
            "Rain probability (%)": hourly["precipitation_probability"][:24],
            "Precipitation (mm)": hourly.get("precipitation", [])[:24],
        })
        st.markdown("### 🌧️ Next 24 hours — rainfall outlook")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=chart_df["Time"], y=chart_df["Precipitation (mm)"], name="Precipitation (mm)"))
        fig.add_trace(go.Scatter(x=chart_df["Time"], y=chart_df["Rain probability (%)"], name="Rain probability (%)", yaxis="y2", mode="lines+markers"))
        fig.update_layout(template="plotly_dark", height=330, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          yaxis=dict(title="Precipitation (mm)"), yaxis2=dict(title="Probability (%)", overlaying="y", side="right", range=[0,100]))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(weather_error_message(error))
    st.info("Weather page માં ફરી Refresh દબાવીને તપાસો. API ઉપલબ્ધ ન હોય ત્યારે ખોટા live values બતાવવામાં આવતા નથી.")

st.markdown("### Explore local modules")
cards = [
    ("🌦️ Full Weather", "Current conditions, hourly and 7-day forecast.", "pages/1_Weather.py"),
    ("🌧️ Rainfall Analysis", "Daily precipitation, rain probability and forecast chart.", "pages/2_Rainfall.py"),
    ("🌊 Ambika River — Bilimora", "River-level monitoring workspace; live gauge source must be verified.", "pages/3_Ambika_River.py"),
    ("🔮 AI Prediction", "Educational prediction demonstration using weather features.", "pages/4_AI_Prediction.py"),
    ("🌦️ What-if Simulation", "Explore hypothetical rainfall and river-level scenarios.", "pages/5_What_If_Simulation.py"),
    ("🧭 Decision Advisor", "Transparent information-based suggestions.", "pages/6_Decision_Advisor.py"),
    ("📄 Reports", "Download current forecast data as CSV.", "pages/7_Reports.py"),
    ("⚙️ Settings", "Location and data-source information.", "pages/8_Settings.py"),
]
cols = st.columns(4)
for i, (title, desc, path) in enumerate(cards):
    with cols[i % 4]:
        page_card(title, desc)
        st.page_link(path, label="Open module →", use_container_width=True)

st.markdown("---")
st.caption("NEXUS ∞ is an educational prototype. It is not an official flood-warning service. Follow IMD and district administration advisories.")
