from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import traceback
import json
from weather_service import WeatherService
from data_processor import DataProcessor
from visualizer import Visualizer

# Create necessary directories if they don't exist
os.makedirs('data', exist_ok=True)
os.makedirs('static/images', exist_ok=True)

# Initialize Flask app
app = Flask(__name__)

# Initialize services
weather_service = WeatherService()
data_processor = DataProcessor()
visualizer = Visualizer()

def log_error(error_message, details=None):
    """Log errors to help with debugging on Vercel"""
    try:
        error_log = {
            "message": error_message,
            "details": details or {}
        }
        print(f"ERROR: {json.dumps(error_log)}")
    except:
        print(f"ERROR: {error_message}")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        log_error(f"Error in index route: {str(e)}")
        return jsonify({"error": "Error rendering index page"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

@app.route('/api/weather', methods=['GET'])
def get_weather_api():
    try:
        city = request.args.get('city', '')
        if not city:
            return jsonify({"error": "City parameter is required"}), 400
        
        # Get current weather and forecast
        current_weather = weather_service.get_current_weather(city)
        if "error" in current_weather:
            log_error(f"Error fetching current weather for {city}", current_weather)
            return jsonify({"error": current_weather["error"]}), 500
            
        forecast = weather_service.get_forecast(city)
        if "error" in forecast:
            log_error(f"Error fetching forecast for {city}", forecast)
            return jsonify({"error": forecast["error"]}), 500

        # Process data
        processed_current = data_processor.process_current_weather(current_weather)
        processed_forecast = data_processor.processed_forecast(forecast)

        # Get historical data - this will be empty in serverless environment
        try:
            historical_data = data_processor.get_historical_data(city)
        except Exception as e:
            log_error(f"Error getting historical data for {city}: {str(e)}")
            historical_data = {"data": []}

        return jsonify({
            "current": processed_current,
            "forecast": processed_forecast,
            "history": historical_data
        })
    except Exception as e:
        error_details = {
            "exception": str(e),
            "traceback": traceback.format_exc()
        }
        log_error(f"Unexpected error in get_weather_api: {str(e)}", error_details)
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        city = request.form.get('city', '')
        if not city:
            return redirect(url_for('index'))
        
        return render_template(
            'weather.html',
            city=city
        )
    except Exception as e:
        log_error(f"Error in get_weather route: {str(e)}")
        return render_template('error.html', error="An unexpected error occurred. Please try again.")

@app.route('/api/debug', methods=['GET'])
def debug():
    """Minimal debug endpoint"""
    return jsonify({
        "status": "ok",
        "message": "Debug endpoint is working"
    })

@app.route('/api/hello', methods=['GET'])
def hello():
    """Basic hello world endpoint"""
    return jsonify({
        "message": "Hello, World!"
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Internal server error. Please try again later."), 500

if __name__ == '__main__':
    # This is for local development
    app.run(debug=True)