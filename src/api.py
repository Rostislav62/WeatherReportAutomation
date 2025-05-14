import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# API configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast"

def get_current_weather(city, country):
    """Fetch current weather data for a given city and country."""
    query = f"{city},{country}"
    params = {
        "q": query,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL_CURRENT, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Current weather for {query}: {data}")  # Debug output
        return {
            "city": city,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "precipitation": data.get("rain", {}).get("1h", 0),
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.RequestException as e:
        print(f"Error fetching current weather for {query}: {e}")
        return None

def get_forecast_weather(city, country):
    """Fetch 5-day forecast data for a given city (closest to 12:00 each day)."""
    query = f"{city},{country}"
    params = {
        "q": query,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL_FORECAST, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Forecast for {query}: {data['list']}")  # Debug output
        forecast_data = []
        seen_dates = set()
        for entry in data["list"]:
            dt = datetime.fromtimestamp(entry["dt"])
            # Select entries closest to 12:00 (within 09:00–15:00)
            if 9 <= dt.hour <= 15 and dt.date() not in seen_dates:
                forecast_data.append({
                    "city": city,
                    "date": dt.strftime("%Y-%m-%d"),
                    "time": dt.strftime("%H:%M"),
                    "temperature": entry["main"]["temp"],
                    "humidity": entry["main"]["humidity"],
                    "precipitation": entry.get("rain", {}).get("3h", 0),
                    "pressure": entry["main"]["pressure"],
                    "wind_speed": entry["wind"]["speed"]
                })
                seen_dates.add(dt.date())
                if len(forecast_data) >= 5:  # Limit to 5 days
                    break
        print(f"Selected forecast for {query}: {forecast_data}")  # Debug output
        return forecast_data
    except requests.RequestException as e:
        print(f"Error fetching forecast for {query}: {e}")
        return []

def get_all_weather_data(cities=[
    ("Moscow", "RU"), ("Chisinau", "MD"), ("Dublin", "IE"),
    ("London", "GB"), ("Berlin", "DE"), ("Paris", "FR")
]):
    """Fetch current and forecast weather data for multiple cities."""
    weather_data = []
    for city, country in cities:
        current = get_current_weather(city, country)
        if current:
            weather_data.append(current)
        forecast = get_forecast_weather(city, country)
        if forecast:
            weather_data.extend(forecast)
        else:
            print(f"No forecast data for {city},{country}")
    print(f"Total weather data collected: {len(weather_data)} entries")  # Debug output
    return weather_data