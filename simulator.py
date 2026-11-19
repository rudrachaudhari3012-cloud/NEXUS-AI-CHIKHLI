
import numpy as np
import pandas as pd


def predict_river_trend(readings):

    if readings is None or readings.empty:
        return None

    df = readings.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    df["level_m"] = pd.to_numeric(
        df["level_m"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["timestamp", "level_m"]
    )

    if len(df) < 3:
        return None

    df = df.sort_values("timestamp").tail(48)

    x = (
        df["timestamp"] - df["timestamp"].min()
    ).dt.total_seconds() / 3600

    if x.nunique() < 2:
        return None

    y = df["level_m"].to_numpy(dtype=float)

    slope, intercept = np.polyfit(
        x.to_numpy(dtype=float),
        y,
        1
    )

    future_x = float(x.max()) + 12

    prediction = (
        slope * future_x + intercept
    )

    return round(float(prediction), 3)


def rainfall_scenario(base_rainfall, increase_percent):

    base_rainfall = float(base_rainfall)

    increase_percent = float(
        increase_percent
    )

    result = base_rainfall * (
        1 + increase_percent / 100
    )

    return round(result, 2)


def classify_river_trend(readings):

    prediction = predict_river_trend(readings)

    if prediction is None:
        return {
            "status": "INSUFFICIENT DATA",
            "prediction": None
        }

    return {
        "status": "TREND ESTIMATE",
        "prediction": prediction
    }
