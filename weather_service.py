import os
import requests
from dotenv import load_dotenv
import traceback

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is not set")
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, city):
        """Get current weather for a city"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric" # Use Celsius
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": f"City '{city}' not found. Please check the spelling and try again."}
            elif response.status_code == 401:
                return {"error": "API key is invalid or expired."}
            else:
                return {"error": f"Error fetching data: {response.status_code}"}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Please try again later."}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection error. Please check your internet connection."}
        except Exception as e:
            print(f"Unexpected error in get_current_weather: {str(e)}")
            traceback.print_exc()
            return {"error": "An unexpected error occurred while fetching weather data."}
        
    def get_forecast(self, city, days=5):
        """Get weather forecast for a city"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8 # API return data in 3-hour increments
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": f"City '{city}' not found. Please check the spelling and try again."}
            elif response.status_code == 401:
                return {"error": "API key is invalid or expired."}
            else:
                return {"error": f"Error fetching forecast: {response.status_code}"}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Please try again later."}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection error. Please check your internet connection."}
        except Exception as e:
            print(f"Unexpected error in get_forecast: {str(e)}")
            traceback.print_exc()
            return {"error": "An unexpected error occurred while fetching forecast data."}