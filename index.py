from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Weather Dashboard API"})

@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/debug')
def debug():
    return jsonify({"status": "ok", "message": "Debug endpoint is working"})

# This is for Vercel serverless deployment
app.debug = False

if __name__ == '__main__':
    # This is for local development only
    app.run(debug=True) 