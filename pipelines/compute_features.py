import pandas as pd
from datetime import datetime


def process_raw_data(raw_data: dict) -> pd.DataFrame:
    """
    Process raw AQI data to extract features and targets.

    Args:
        raw_data (dict): The raw data from the AQICN API.

    Returns:
        pd.DataFrame: Processed DataFrame containing features and targets.
    """
    if "data" not in raw_data or raw_data["status"] != "ok":
        raise ValueError("Invalid data: Missing 'data' field or status is not 'ok'.")

    data = raw_data["data"]

    # Extract current data (features)
    aqi = data.get("aqi")
    dominant_pollutant = data.get("dominentpol", None)
    timestamp = data.get("time", {}).get("s", None)
    geo_location = data.get("city", {}).get("geo", [None, None])

    # Extract individual pollutants (features)
    iaqi = data.get("iaqi", {})
    pollutants = {pollutant: iaqi.get(pollutant, {}).get("v", None) for pollutant in iaqi}

    # Add basic features
    current_data = {
        "timestamp": timestamp,
        "latitude": geo_location[0],
        "longitude": geo_location[1],
        "aqi": aqi,
        "dominant_pollutant": dominant_pollutant,
        **pollutants,  # Expand all pollutants like pm25, pm10, co, etc.
    }

    # Extract forecast data (targets)
    forecast_data = []
    for pollutant, forecasts in data.get("forecast", {}).get("daily", {}).items():
        for forecast in forecasts:
            forecast_data.append(
                {
                    **current_data,  # Include current features
                    "forecast_date": datetime.strptime(forecast["day"], "%Y-%m-%d"),
                    "pollutant": pollutant,
                    "forecast_avg": forecast["avg"],
                    "forecast_min": forecast["min"],
                    "forecast_max": forecast["max"],
                }
            )

    # Convert to DataFrame
    df = pd.DataFrame(forecast_data)

    return df


if __name__ == "__main__":
    from fetch_data import fetch_raw_data
    from dotenv import load_dotenv
    import os

    # Load API token
    load_dotenv()
    api_token = os.getenv("AQICN_API_TOKEN")

    city = "barcelona"
    raw_data = fetch_raw_data(city, api_token)

    try:
        processed_df = process_raw_data(raw_data)
        print(processed_df.head())  # Display first few rows
    except Exception as e:
        print("Error processing data:", e)
