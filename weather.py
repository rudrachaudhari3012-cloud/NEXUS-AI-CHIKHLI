
import requests
import pandas as pd


LOCATIONS = {
    "Chikhli": {
        "latitude": 20.75,
        "longitude": 73.06
    },
    "Bilimora": {
        "latitude": 20.77,
        "longitude": 72.97
    }
}


def get_weather(city):

    if city not in LOCATIONS:
        raise ValueError("Unknown monitoring location")

    location = LOCATIONS[city]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "uv_index"
        ],

        "hourly": [
            "temperature_2m",
            "precipitation",
            "precipitation_probability",
            "uv_index"
        ],

        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "uv_index_max",
            "precipitation_probability_max"
        ],

        "forecast_days": 5,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    current = data.get("current", {})

    hourly = data.get("hourly", {})
    daily = data.get("daily", {})

    hourly_df = pd.DataFrame({
        "time": hourly.get("time", []),
        "temperature": hourly.get("temperature_2m", []),
        "rain": hourly.get("precipitation", []),
        "rain_probability": hourly.get(
            "precipitation_probability", []
        ),
        "uv": hourly.get("uv_index", [])
    })

    daily_df = pd.DataFrame(daily)

    return {
        "temperature": round(
            current.get("temperature_2m", 0), 1
        ),

        "humidity": current.get(
            "relative_humidity_2m", 0
        ),

        "rain": current.get("precipitation", 0),

        "wind": current.get("wind_speed_10m", 0),

        "uv": current.get("uv_index", 0),

        "time": current.get("time", "Unavailable"),

        "hourly": hourly_df,

        "daily": daily_df,

        "source": "Open-Meteo"
    }
