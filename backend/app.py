from flask import Flask
from flask_cors import CORS
from routes import api_blueprint

def create_app():
    """
    Application Factory Pattern.
    Instantiates and configures the Flask application.
    """
    # 1. Initialize the Flask application
    app = Flask(__name__)
    
    # 2. Enable CORS (Cross-Origin Resource Sharing)
    # This is CRITICAL. Without it, the browser will block our frontend (HTML)
    # from talking to our backend (Python) because they are running on different ports.
    CORS(app)
    
    # 3. Register the API endpoints we created in routes.py
    # We add a URL prefix, so every route starts with /api (e.g., /api/predict/news)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # A simple health-check route to verify the server is running
    @app.route('/', methods=['GET'])
    def home():
        return "AI Fraud Detector Backend is Running!", 200
        
    return app

# Only run the server if this file is executed directly 
if __name__ == '__main__':
    app = create_app()
    # debug=True allows the server to auto-restart when we save file changes.
    # We run on port 5000, which matches the endpoint in our JS file.
    print("\n[INFO] Starting API Server on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)