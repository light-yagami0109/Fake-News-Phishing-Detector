from flask import Blueprint, request, jsonify
from utils import predict_news, predict_phishing

# Create a Blueprint named 'api'. This groups our routes together.
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/predict/news', methods=['POST'])
def handle_news():
    """
    Endpoint: POST /api/predict/news
    Receives JSON containing {'text': '...'}
    """
    # 1. Parse the incoming JSON payload from the frontend
    data = request.get_json()
    
    # 2. Input Validation (Checking for bad data)
    if not data or 'text' not in data:
        # Return a 400 Bad Request error if the text is missing
        return jsonify({"error": "Missing 'text' key in JSON payload"}), 400
    
    text_content = data['text']
    
    # 3. Pass data to our AI Utility function
    result = predict_news(text_content)
    
    # 4. Return the result as JSON with a 200 OK status
    return jsonify(result), 200


@api_blueprint.route('/predict/url', methods=['POST'])
def handle_url():
    """
    Endpoint: POST /api/predict/url
    Receives JSON containing {'url': '...'}
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' key in JSON payload"}), 400
        
    url_content = data['url']
    
    result = predict_phishing(url_content)
    
    return jsonify(result), 200