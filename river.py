
import pandas as pd

from database import save_reading, save_alert


def add_demo_reading(level, threshold):

    level = float(level)
    threshold = float(threshold)

    # This is simulated data, not a real river sensor.
    save_reading(
        level,
        source="SIMULATED SENSOR DEMO"
    )

    if level >= threshold:

        message = (
            "DEMO ALERT: Water level crossed "
            f"the configured threshold. "
            f"Level={level} m, Threshold={threshold} m"
        )

        save_alert(
            level,
            threshold,
            message,
            "SIMULATED SENSOR DEMO"
        )


def import_river_csv(uploaded_file):

    df = pd.read_csv(uploaded_file)

    # Required columns:
    # timestamp, level_m

    required = ["timestamp", "level_m"]

    if not all(col in df.columns for col in required):
        raise ValueError(
            "CSV must contain timestamp and level_m columns."
        )

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

    if df.empty:
        raise ValueError(
            "No valid river records found."
        )

    if (df["level_m"] < 0).any():
        raise ValueError(
            "Water level cannot be negative."
        )

    count = 0

    for _, row in df.iterrows():

        save_reading(
            row["level_m"],
            source="UPLOADED CSV"
        )

        count += 1

    return count
