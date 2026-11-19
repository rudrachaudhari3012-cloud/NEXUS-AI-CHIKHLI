
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from database import init_db, get_readings, get_alerts, clear_alerts
from weather import get_weather
from river import add_demo_reading, import_river_csv
from simulator import predict_river_trend, rainfall_scenario

st.set_page_config(
    page_title="NEXUS INFINITY",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# ---------------- LANGUAGE ----------------

LANG = {
    "English": {
        "overview": "City Overview",
        "weather": "Weather Intelligence",
        "river": "Ambika River Intelligence",
        "simulator": "AI Simulator",
        "alerts": "Alert Center",
        "settings": "Settings",
        "temp": "Temperature",
        "humidity": "Humidity",
        "rain": "Rainfall",
        "wind": "Wind Speed",
        "uv": "UV Index",
        "map": "Monitoring Locations",
        "demo": "Sensor Demonstration",
        "level": "Water Level (metres)",
        "save": "Save Sensor Reading",
        "threshold": "Alert Threshold (metres)",
        "prediction": "River Trend Prediction",
        "upload": "Upload River CSV",
        "scenario": "Rainfall Scenario",
        "increase": "Rainfall Increase (%)",
        "run": "Run Simulation",
        "history": "Alert History",
        "clear": "Clear Alert History",
        "no_data": "No river data available.",
        "model": "Weather values are model-based, not physical local sensor readings.",
        "safety": "Prototype only. Follow official government warnings. No emergency service is contacted."
    },
    "ગુજરાતી": {
        "overview": "શહેરની ઝાંખી",
        "weather": "હવામાન ઇન્ટેલિજન્સ",
        "river": "અંબિકા નદી મોનિટરિંગ",
        "simulator": "AI સિમ્યુલેટર",
        "alerts": "ચેતવણી કેન્દ્ર",
        "settings": "સેટિંગ્સ",
        "temp": "તાપમાન",
        "humidity": "ભેજ",
        "rain": "વરસાદ",
        "wind": "પવનની ઝડપ",
        "uv": "UV સૂચકાંક",
        "map": "મોનિટરિંગ સ્થળો",
        "demo": "સેન્સર ડેમો",
        "level": "પાણીનું સ્તર (મીટર)",
        "save": "સેન્સર રીડિંગ સાચવો",
        "threshold": "ચેતવણી મર્યાદા (મીટર)",
        "prediction": "નદીના સ્તરનો ટ્રેન્ડ",
        "upload": "River CSV અપલોડ કરો",
        "scenario": "વરસાદનું સિમ્યુલેશન",
        "increase": "વરસાદમાં વધારો (%)",
        "run": "સિમ્યુલેશન ચલાવો",
        "history": "ચેતવણીનો ઇતિહાસ",
        "clear": "ચેતવણીનો ઇતિહાસ સાફ કરો",
        "no_data": "નદીનો ડેટા ઉપલબ્ધ નથી.",
        "model": "હવામાનના આંકડા મોડેલ આધારિત છે, સ્થાનિક ભૌતિક સેન્સર રીડિંગ નથી.",
        "safety": "આ માત્ર પ્રોટોટાઇપ છે. સત્તાવાર સરકારી ચેતવણીઓ અનુસરો. કોઈ ઇમરજન્સી સેવાને સંદેશ મોકલાતો નથી."
    }
}

st.sidebar.markdown("# 🌐 NEXUS ∞")
st.sidebar.caption("SMART CITY DIGITAL TWIN")

language = st.sidebar.selectbox(
    "Language / ભાષા",
    ["English", "ગુજરાતી"]
)

T = LANG[language]

pages = [
    T["overview"],
    T["weather"],
    T["river"],
    T["simulator"],
    T["alerts"],
    T["settings"]
]

page = st.sidebar.radio("Navigation", pages)

# ---------------- PREMIUM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+Gujarati:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: Inter, 'Noto Sans Gujarati', sans-serif;
}

.stApp {
    background:
    radial-gradient(circle at 10% 0%, #153B58 0%, transparent 35%),
    linear-gradient(135deg,#061321,#0B2034,#071725);
    color: #F4FAFF;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#102B43,#071522);
}

.block-container {
    padding-top: 2rem;
    max-width: 1600px;
}

.hero {
    padding: 32px;
    border-radius: 22px;
    background: linear-gradient(115deg,#123653,#07576C,#102B43);
    border: 1px solid #35D7F2;
    margin-bottom: 25px;
    box-shadow: 0 12px 40px #0008;
}

.hero h1 {
    color: white;
    font-size: 46px;
    font-weight: 900;
}

.hero p {
    color: #BDECF6;
    font-size: 15px;
}

.metric {
    background: linear-gradient(145deg,#143550,#0B2035);
    border: 1px solid #23617B;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
}

.metric h2 {
    color: #39D8F1;
    font-size: 14px;
}

.metric h1 {
    color: white;
    font-size: 30px;
}

.stButton button {
    background: linear-gradient(90deg,#0786A5,#1268A5);
    color: white;
    border: 1px solid #4CDCF0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}

.stButton button:hover {
    border: 1px solid white;
}

.stTabs [aria-selected="true"] {
    color: #42DDF5 !important;
}

div[data-testid="stMetric"] {
    background: #102B43;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #23617B;
}

div[data-testid="stMetric"] label {
    color: #C5DDED !important;
}

div[data-testid="stMetricValue"] {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <p>SMART CITY · DIGITAL TWIN · ENVIRONMENTAL INTELLIGENCE</p>
    <h1>NEXUS ∞ INFINITY</h1>
    <p>DETECT → PREDICT → SIMULATE → DECIDE</p>
    <p>CHIKHLI RAINFALL | BILIMORA AMBIKA RIVER</p>
</div>
""", unsafe_allow_html=True)

# ---------------- WEATHER DATA ----------------

@st.cache_data(ttl=600)
def load_weather(city):
    return get_weather(city)

# ---------------- OVERVIEW ----------------

if page == T["overview"]:

    st.title("🌐 " + T["overview"])

    chikhli = load_weather("Chikhli")
    bilimora = load_weather("Bilimora")

    c1, c2, c3, c4 = st.columns(4)

    def show_metric(col, title, value):
        with col:
            st.markdown(
                f'<div class="metric"><h2>{title}</h2>'
                f'<h1>{value}</h1></div>',
                unsafe_allow_html=True
            )

    show_metric(c1, "Chikhli Temperature",
                f'{chikhli["temperature"]} °C')

    show_metric(c2, "Chikhli Rainfall",
                f'{chikhli["rain"]} mm')

    show_metric(c3, "Bilimora Temperature",
                f'{bilimora["temperature"]} °C')

    show_metric(c4, "Bilimora UV Index",
                str(bilimora["uv"]))

    st.info(T["model"])

    st.subheader("🗺️ " + T["map"])

    map_data = pd.DataFrame({
        "latitude": [20.75, 20.77],
        "longitude": [73.06, 72.97]
    })

    st.map(map_data, zoom=10)

    st.markdown("### 📍 Monitoring Zones")

    a, b = st.columns(2)

    with a:
        st.info("CHIKHLI | NAVSARI DISTRICT")
        st.write("Weather, Rainfall and Forecast Monitoring")

    with b:
        st.info("BILIMORA | GANDEVI TALUKA")
        st.write("Ambika River Monitoring Target")

    st.warning(T["safety"])

# ---------------- WEATHER PAGE ----------------

elif page == T["weather"]:

    st.title("🌦️ " + T["weather"])

    city = st.selectbox(
        "Select Location",
        ["Chikhli", "Bilimora"]
    )

    if st.button("Refresh Weather"):
        load_weather.clear()
        st.rerun()

    try:
        data = load_weather(city)

        a, b, c, d, e = st.columns(5)

        a.metric(T["temp"], f'{data["temperature"]} °C')
        b.metric(T["humidity"], f'{data["humidity"]}%')
        c.metric(T["rain"], f'{data["rain"]} mm')
        d.metric(T["wind"], f'{data["wind"]} km/h')
        e.metric(T["uv"], data["uv"])

        st.info(T["model"])

        forecast = pd.DataFrame(data["hourly"])

        if not forecast.empty:
            st.subheader("Hourly Temperature Forecast")
            st.line_chart(
                forecast.set_index("time")[["temperature"]]
            )

            st.subheader("Hourly Rainfall Forecast")
            st.bar_chart(
                forecast.set_index("time")[["rain"]]
            )

        st.subheader("5-Day Weather Forecast")
        st.dataframe(
            pd.DataFrame(data["daily"]),
            use_container_width=True
        )

    except Exception as error:
        st.error(f"Weather unavailable: {error}")

# ---------------- RIVER PAGE ----------------

elif page == T["river"]:

    st.title("🌊 " + T["river"])

    st.info("AMBİKA RIVER | BILIMORA | NAVSARI")

    st.warning(
        "No verified live Bilimora river gauge is configured. "
        "Demo readings are not real river measurements."
    )

    st.subheader("📂 " + T["upload"])

    uploaded = st.file_uploader(
        "Upload historical river CSV",
        type=["csv"]
    )

    if uploaded:
        if st.button("Import CSV Data"):
            try:
                count = import_river_csv(uploaded)
                st.success(f"{count} records imported.")
                st.rerun()
            except Exception as error:
                st.error(str(error))

    st.divider()

    st.subheader("🧪 " + T["demo"])

    st.warning("SIMULATED DATA ONLY — NOT ACTUAL AMBIKA RIVER LEVEL")

    with st.form("sensor_form"):

        level = st.number_input(
            T["level"],
            min_value=0.0,
            max_value=100.0,
            value=2.0,
            step=0.1
        )

        threshold = st.number_input(
            T["threshold"],
            min_value=0.1,
            max_value=100.0,
            value=5.0
        )

        save = st.form_submit_button(T["save"])

    if save:
        add_demo_reading(level, threshold)
        st.success("Demo reading saved.")
        st.rerun()

    readings = get_readings()

    if not readings.empty:

        st.subheader(T["prediction"])

        st.line_chart(
            readings.set_index("timestamp")[["level_m"]]
        )

        prediction = predict_river_trend(readings)

        if prediction is not None:
            st.metric(
                "Illustrative 12-hour trend",
                f"{prediction:.2f} m"
            )

        st.caption(
            "Linear trend prototype only; not an official flood forecast."
        )

        st.dataframe(readings, use_container_width=True)

    else:
        st.info(T["no_data"])

# ---------------- SIMULATOR PAGE ----------------

elif page == T["simulator"]:

    st.title("🧠 " + T["simulator"])

    st.info("Illustrative scenario, not a calibrated flood model.")

    base_rain = st.number_input(
        "Base Rainfall (mm)",
        min_value=0.0,
        value=40.0
    )

    increase = st.slider(
        T["increase"],
        min_value=-50,
        max_value=300,
        value=50
    )

    if st.button(T["run"]):

        result = rainfall_scenario(
            base_rain,
            increase
        )

        st.metric(
            "Scenario Rainfall",
            f"{result:.2f} mm"
        )

        fig = go.Figure()

        fig.add_bar(
            x=["Base Rainfall", "Scenario Rainfall"],
            y=[base_rain, result]
        )

        fig.update_layout(
            template="plotly_dark",
            title="Rainfall Scenario Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.warning(
            "This scenario does not predict actual river levels."
        )

# ---------------- ALERT PAGE ----------------

elif page == T["alerts"]:

    st.title("🚨 " + T["alerts"])

    st.info(
        "Prototype alerts only. No police, fire station, SMS "
        "or emergency authority is contacted."
    )

    alerts = get_alerts()

    if not alerts.empty:
        st.dataframe(
            alerts,
            use_container_width=True
        )
    else:
        st.info("No alerts recorded.")

    if st.button(T["clear"]):
        clear_alerts()
        st.success("Alert history cleared.")
        st.rerun()

# ---------------- SETTINGS ----------------

elif page == T["settings"]:

    st.title("⚙️ " + T["settings"])

    st.write("PROJECT: NEXUS INFINITY")
    st.write("DISTRICT: NAVSARI")
    st.write("CHIKHLI: WEATHER AND RAINFALL")
    st.write("BILIMORA: AMBIKA RIVER")
    st.write("RIVER TARGET TALUKA: GANDEVI")

    st.write("Technology: Python + Streamlit + SQLite")
    st.write("Weather: Open-Meteo API")
    st.write("Database: SQLite")

    st.warning(T["safety"])

# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    """
    <center>
    <h3 style="color:#35D7F2">NEXUS ∞ INFINITY</h3>
    SMART CITY DIGITAL TWIN<br>
    NAVSARI · GUJARAT · INDIA<br>
    <small>Educational Prototype | Version 1.0</small>
    </center>
    """,
    unsafe_allow_html=True
)
