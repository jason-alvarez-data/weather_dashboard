import json
import os
from datetime import datetime

class WeatherDataProcessor:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def process_current_weather(self, weather_data):
        """Process current weather data"""
        if "error" in weather_data:
            return weather_data
        
        # Extract relevant information
        processed_data = {
            "city": weather_data["name"],
            "country": weather_data["sys"]["country"],
            "temperature": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "weather_main": weather_data["weather"][0]["main"],
            "weather_description": weather_data["weather"][0]["description"],
            "wind_speed": weather_data["wind"]["speed"],
            "clouds": weather_data["clouds"]["all"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save data for historical tracking
        self._save_weather_data(processed_data)

        return processed_data
    
    def processed_forecast(self, forecast_data):
        """Process forecast data"""
        if "error" in forecast_data:
            return forecast_data
        
        forecast_list = forecast_data["list"]
        city = forecast_data["city"]["name"]

        processed_forecast = []
        for item in forecast_list:
            forecast_item = {
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "weather_main": item["weather"][0]["main"],
                "weather_description": item["weather"][0]["description"],
                "wind_speed": item["wind"]["speed"],
                "probability": item.get("pop", 0) * 100 # Probability of precipitation
            }
            processed_forecast.append(forecast_item)

        return {
            "city": city,
            "forecast": processed_forecast
        }
    
    def _save_weather_data(self, data):
        """Save weather data for historical tracking"""
        city = data["city"].lower()
        filename = f"{self.data_dir}/{city}_history.json"

        # Load existing data if available
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = {"data": []}
        else: 
            history = {"data": []}

        # Append new data
        history["data"].append(data)

        # Save updated data
        with open(filename, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_historical_data(self, city):
        """Get historical weather data for a city"""
        city = city.lower()
        filename = f"{self.data_dir}/{city}_history.json"

        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try: 
                    return json.load(f)
                except json.JSONDecodeError:
                    return {"data": []}
        else:
            return {"data": []}