import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# API Fortran keyword: API configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """Fetch weather data for a given city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Use Celsius
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "city": city,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "precipitation": data.get("rain", {}).get("1h", 0)  # Rain in last hour, default 0
        }
    except requests.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

def get_all_weather_data(cities=["Moscow", "London", "New York"]):
    """Fetch weather data for multiple cities."""
    weather_data = []
    for city in cities:
        data = get_weather_data(city)
        if data:
            weather_data.append(data)
    return weather_data