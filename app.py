from flask import Flask, render_template, request, redirect, url_for, jsonify
from weather_service import WeatherService
from data_processor import WeatherDataProcessor
import os
import traceback
import json

# Initialize Flask app
app = Flask(__name__)

# Initialize services
try:
    weather_service = WeatherService()
    data_processor = WeatherDataProcessor(use_memory_storage=True)  # Use in-memory storage instead of file system
except Exception as e:
    print(f"Error initializing services: {str(e)}")
    traceback.print_exc()

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
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Weather Dashboard API is running"})

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
    """Debug endpoint to check environment variables and system status"""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        api_key_status = "Set" if api_key else "Not set"
        
        # Check environment
        env_info = {
            "api_key_status": api_key_status,
            "python_version": os.sys.version,
            "environment": os.environ.get("VERCEL_ENV", "unknown"),
            "region": os.environ.get("VERCEL_REGION", "unknown")
        }
        
        return jsonify({
            "status": "ok",
            "environment": env_info
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Internal server error. Please try again later."), 500

# This is for Vercel serverless deployment
app.debug = False

if __name__ == '__main__':
    # This is for local development only
    # Create directories for local development
    if not os.environ.get("VERCEL_ENV"):
        os.makedirs('data', exist_ok=True)
        os.makedirs('static/images', exist_ok=True)
    app.run(debug=True)