import requests
import os

def fetch_raw_data(city: str, api_token: str) -> dict:
    """
    Fetch real-time air quality index (AQI) and forecast data for a given city.

    Args:
        city (str): The name or ID of the city (e.g., "shanghai" or "@7397").
        api_token (str): Your AQICN API token.

    Returns:
        dict: Parsed JSON response containing AQI and forecast data.

    Raises:
        Exception: If the API request fails or returns an error status.
    """
    url = f"https://api.waqi.info/feed/{city}/"
    params = {"token": api_token}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

    data = response.json()

    if data.get("status") != "ok":
        raise Exception(f"API Error: {data.get('message', 'Unknown error')}")

    return data


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv

    # Load API token from .env file
    load_dotenv()
    api_token = os.getenv("AQICN_API_TOKEN")

    if not api_token:
        raise ValueError("API token is not set. Please define AQICN_API_TOKEN in your .env file.")

    city = "barcelona"  # Replace with your city or station ID
    try:
        data = fetch_raw_data(city, api_token)
        print("Fetched Data:", data)
    except Exception as e:
        print("Error:", e)
