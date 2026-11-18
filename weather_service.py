import json
import urllib.parse
import urllib.request
import streamlit as st

# Approximate coordinates for Chikhli town, Navsari, Gujarat.
CHIKHLI_LAT = 20.75814
CHIKHLI_LON = 73.05990

@st.cache_data(ttl=900, show_spinner=False)
def get_chikhli_weather():
    params = {
        "latitude": CHIKHLI_LAT,
        "longitude": CHIKHLI_LON,
        "timezone": "Asia/Kolkata",
        "forecast_days": 7,
        "current": ",".join([
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "is_day", "precipitation", "rain", "showers", "weather_code",
            "cloud_cover", "pressure_msl", "wind_speed_10m", "wind_direction_10m",
            "wind_gusts_10m"
        ]),
        "hourly": ",".join([
            "temperature_2m", "relative_humidity_2m", "precipitation_probability",
            "precipitation", "rain", "showers", "weather_code", "cloud_cover",
            "wind_speed_10m"
        ]),
        "daily": ",".join([
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "precipitation_sum", "rain_sum", "precipitation_probability_max",
            "wind_speed_10m_max", "sunrise", "sunset", "uv_index_max"
        ])
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "NEXUS-Chikhli-Student-Project/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8")), None
    except Exception as exc:
        return None, str(exc)

def weather_error_message(error):
    return f"Chikhli weather service હાલમાં મળતી નથી. Internet/API connection તપાસો. Details: {error or 'Unknown error'}"
