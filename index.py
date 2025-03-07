from flask import Flask, jsonify
import os
import sys
import traceback
import json

# Initialize Flask app
app = Flask(__name__)

# Error logging function
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
        return jsonify({
            "message": "Welcome to the Weather Dashboard API",
            "endpoints": {
                "/api/hello": "Basic hello world endpoint",
                "/api/health": "Health check endpoint",
                "/api/debug": "Debug information endpoint"
            }
        })
    except Exception as e:
        log_error(f"Error in index route: {str(e)}")
        return jsonify({"error": "Error in index page", "details": str(e)}), 500

@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/debug')
def debug():
    try:
        # Return basic debug information
        debug_info = {
            "status": "ok",
            "message": "Debug endpoint is working",
            "python_version": sys.version,
            "environment": "Vercel"
        }
        
        return jsonify(debug_info)
    except Exception as e:
        error_details = {
            "exception": str(e),
            "traceback": traceback.format_exc()
        }
        log_error("Error in debug endpoint", error_details)
        return jsonify({"error": "Error in debug endpoint", "details": error_details}), 500

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not found", "details": str(e)}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "details": str(e)}), 500

# This is for Vercel serverless deployment
app.debug = False

if __name__ == '__main__':
    # This is for local development only
    app.run(debug=True) 