import os
import requests
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, city):
        """Get current weather for a city"""
        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric" # Use Celsius
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error fetching data: {response.status_code}"}
        
    def get_forecast(self, city, days=5):
        """Get weather forecast for a city"""
        url = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "cnt": days * 8 # API return data in 3-hour increments
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error fetching forecast: {response.status_code}"}