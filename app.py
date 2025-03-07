from flask import Flask, render_template, request, redirect, url_for
from weather_service import WeatherService
from data_processor import WeatherDataProcessor
from visualizer import WeatherVisualizer
import os

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('static/images', exist_ok=True)

app = Flask(__name__)

# Initialize services
weather_service = WeatherService()
data_processor = WeatherDataProcessor()
visualizer = WeatherVisualizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city', '')
    if not city:
        return redirect(url_for('index'))
    
    # Get current weather and forecast
    current_weather = weather_service.get_current_weather(city)
    forecast = weather_service.get_forecast(city)

    # Process data
    processed_current = data_processor.process_current_weather(current_weather)
    processed_forecast = data_processor.processed_forecast(forecast)

    # Get historical data
    historical_data = data_processor.get_historical_data(city)

    # Create visualizations
    visualizer.create_temperature_chart(processed_forecast)
    visualizer.create_weather_dashboard(processed_current, processed_forecast)

    return render_template(
        'weather.html',
        current=processed_current,
        forecast=processed_forecast,
        history=historical_data
    )

# This is for Vercel serverless deployment
app.debug = False

if __name__ == '__main__':
    # This is for local development only
    app.run(debug=True)