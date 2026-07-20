import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from feature_extractor import extract_url_features

# ==========================================
# 1. Dataset Loading & Processing
# ==========================================
def load_and_prepare_data():
    print("[INFO] Loading Phishing Dataset...")
    try:
        # CRITICAL FIX: Read the whole file first, THEN shuffle and take 50,000.
        # This guarantees a perfectly mixed balance of Safe and Phishing links.
        df = pd.read_csv('../datasets/phishing_site_urls.csv')
        df = df.sample(n=50000, random_state=42).reset_index(drop=True)
    except FileNotFoundError:
        print("[ERROR] Dataset not found!")
        return None, None
        
    print("[INFO] Mapping text labels to binary numbers (good->0, bad->1)...")
    df['Label'] = df['Label'].map({'good': 0, 'bad': 1})
    
    print("[INFO] Extracting URL structural features (This will take a few minutes)...")
    extracted_features = df['URL'].apply(extract_url_features)
    
    X = pd.DataFrame(extracted_features.tolist(), columns=[
        'Has_IP', 'URL_Length', 'Is_Shortened', 'Has_At_Symbol', 
        'Has_Double_Slash', 'Has_Hyphen', 'Domain_Dots', 'HTTPS_in_Domain'
    ])
    Y = df['Label']
    return X, Y

# ==========================================
# 2. Model Training Pipeline
# ==========================================
def train_model():
    X, Y = load_and_prepare_data()
    if X is None:
        return
        
    print("[INFO] Splitting dataset into Training and Testing sets...")
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    print("[INFO] Training Random Forest Classifier (Building 100 Decision Trees)...")
    # n_estimators=100 means we build a forest of 100 trees
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, Y_train)
    
    # ==========================================
    # 3. Model Evaluation
    # ==========================================
    print("\n[INFO] Evaluating Model Performance:")
    predictions = model.predict(X_test)
    
    acc = accuracy_score(Y_test, predictions)
    print(f"Accuracy: {acc * 100:.2f}%\n")
    
    print("Classification Report:")
    # Generates precision, recall, and f1-score automatically
    print(classification_report(Y_test, predictions))
    
    print("Confusion Matrix:")
    print(confusion_matrix(Y_test, predictions))
    
    # Print Feature Importance (Shows which structural flaw the AI relies on most)
    print("\n[INFO] Feature Importances (What the AI learned matters most):")
    importances = model.feature_importances_
    for feature, importance in zip(X.columns, importances):
        print(f"{feature}: {importance * 100:.2f}%")
        
    # ==========================================
    # 4. Saving the Binary Artifact
    # ==========================================
    print("\n[INFO] Saving Phishing Model to disk...")
    with open('../models/phishing_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    print("[SUCCESS] Phishing model training complete and saved.")

if __name__ == "__main__":
    train_model()