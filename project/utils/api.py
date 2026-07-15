import requests
import config
from typing import Dict, Any, Optional

def fetch_weather_data(city: str = "New York") -> Dict[str, Any]:
    """
    Fetch live weather data from openweathermap API if API key is present.
    Otherwise, returns fallback mock data for campus location dashboard.
    """
    if not config.WEATHER_API_KEY:
        # Fallback to realistic mock smart campus weather telemetry
        return {
            "success": True,
            "city": city,
            "temp": 24.5,
            "condition": "Partly Cloudy",
            "humidity": 62,
            "wind_speed": 12.4,
            "source": "Campus Weather Station (Simulated)"
        }
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "city": city,
            "temp": data["main"]["temp"],
            "condition": data["weather"][0]["main"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "source": "OpenWeather API"
        }
    except Exception as e:
        # Graceful degradation on API failure
        return {
            "success": False,
            "error": str(e),
            "temp": 22.0,
            "condition": "Cloudy",
            "humidity": 65,
            "wind_speed": 10.0,
            "source": "Campus Station (Offline Fallback)"
        }

def get_external_notices() -> Optional[Dict[str, Any]]:
    """
    Fetch global educational notifications from a mock external feed or academic service.
    """
    try:
        # Mocking an academic REST API query
        return {
            "status": "success",
            "source": "National Educational Feed",
            "notices": [
                {"title": "National Science Scholarship 2026 Open", "date": "2026-07-10"},
                {"title": "Inter-University Coding Tournament Registrations", "date": "2026-07-08"}
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "notices": []}
