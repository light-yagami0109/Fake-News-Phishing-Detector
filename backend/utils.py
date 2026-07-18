import pickle
import os

# ==========================================
# 1. Directory Configuration
# ==========================================
# Get the absolute path to the directory where this current file (utils.py) lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Navigate up one folder to find the 'models' directory
MODELS_DIR = os.path.join(BASE_DIR, '../models')

# ==========================================
# 2. Model Loading Function
# ==========================================
def load_model(filename):
    """
    Safely loads a serialized (.pkl) machine learning model.
    """
    file_path = os.path.join(MODELS_DIR, filename)
    try:
        # 'rb' stands for Read Binary. Models are saved as binary data, not plain text.
        with open(file_path, 'rb') as file:
            model = pickle.load(file)
        print(f"[SUCCESS] Loaded {filename} into memory.")
        return model
    except FileNotFoundError:
        print(f"[WARNING] {filename} not found. Ensure you run the ML training scripts first.")
        return None

# Load all models when the server starts
fake_news_model = load_model('fake_news_model.pkl')
vectorizer = load_model('vectorizer.pkl')
phishing_model = load_model('phishing_model.pkl')

# ==========================================
# 3. Prediction Functions
# ==========================================
def predict_news(text):
    """
    Takes raw text, vectorizes it, and predicts if it is Fake or Real.
    """
    # Safety check: If models aren't trained yet, return a safe fallback.
    if not fake_news_model or not vectorizer:
        return {"prediction": "Model Not Trained", "confidence": 0}
    
    try:
        # 1. Transform text into numbers using the exact vocabulary learned during training
        vectorized_text = vectorizer.transform([text])
        
        # 2. Get the mathematical prediction (usually 0 for Fake, 1 for Real)
        prediction_value = fake_news_model.predict(vectorized_text)[0]
        
        # 3. Get the confidence percentage. predict_proba returns array like [[0.1, 0.9]]
        probabilities = fake_news_model.predict_proba(vectorized_text)[0]
        confidence = round(max(probabilities) * 100, 2)
        
        # 4. Map the numeric prediction back to human text
        result = "Fake" if prediction_value == 0 else "Real"
        
        return {"prediction": result, "confidence": confidence}
    
    except Exception as e:
        print(f"[ERROR] News prediction failed: {e}")
        return {"prediction": "Processing Error", "confidence": 0}

def predict_phishing(url):
    """
    Takes a URL string, extracts its numerical features, and predicts if it is Phishing.
    """
    if not phishing_model:
        return {"prediction": "Model Not Trained", "confidence": 0}
    
    try:
        # Dynamically import the feature extractor from the ml folder
        import sys
        ml_path = os.path.join(BASE_DIR, '../ml')
        if ml_path not in sys.path:
            sys.path.append(ml_path)
        
        from feature_extractor import extract_url_features
        
        # 1. Convert the URL string into an array of numbers (features)
        features = extract_url_features(url)
        
        # 2. Feed the features to the Random Forest model
        prediction_value = phishing_model.predict([features])[0]
        probabilities = phishing_model.predict_proba([features])[0]
        confidence = round(max(probabilities) * 100, 2)
        
        # 3. Map result (assuming 1 is Phishing, 0 is Safe)
        result = "Phishing" if prediction_value == 1 else "Safe"
        
        return {"prediction": result, "confidence": confidence}
        
    except ImportError:
        print("[WARNING] feature_extractor.py not found yet. We will build this in Chapter 6.")
        return {"prediction": "Feature Extractor Missing", "confidence": 0}
    except Exception as e:
        print(f"[ERROR] URL prediction failed: {e}")
        return {"prediction": "Processing Error", "confidence": 0}