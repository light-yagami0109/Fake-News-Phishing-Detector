from flask import Flask
from flask_cors import CORS
from routes import api_blueprint

def create_app():
    """
    Application Factory Pattern.
    Instantiates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # Enable Cross-Origin Resource Sharing
    CORS(app)
    
    # Register the API endpoints
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    @app.route('/', methods=['GET'])
    def home():
        return "AI Fraud Detector Backend is Running!", 200
        
    return app

# --- CRITICAL FIX FOR PRODUCTION DEPLOYMENT ---
# Exposing 'app' at the root module level so Gunicorn can find it during import
app = create_app()

# This block is now strictly used ONLY for local manual testing
if __name__ == '__main__':
    print("\n[INFO] Starting API Server locally on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)