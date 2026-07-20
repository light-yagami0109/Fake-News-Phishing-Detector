# 🛡️ AI Fraud Detector: Fake News & Phishing 

## 📖 1. Project Overview
The AI Fraud Detector is a full-stack Machine Learning web application designed to protect users from two major cybersecurity threats: misinformation and deceptive links.
By utilizing Natural Language Processing (NLP) and Random Forest feature extraction, this tool mathematically predicts the probability of text being Fake News or a URL being a Phishing trap.

## ⚙️ 2. Technology Stack
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
*   **Backend:** Python, Flask, REST APIs
*   **Machine Learning:** scikit-learn, NLTK, pandas, NumPy
*   **Deployment:** Vercel (UI), Render (API)

---

## 🚀 3. Installation Guide (Local Development)

### Prerequisites
*   Python 3.8+
*   Git

### Step-by-Step Setup
1. **Clone the Repository**
   ```bash
   git clone [https://github.com/YourUsername/Fake-News-Phishing-Detector.git](https://github.com/YourUsername/Fake-News-Phishing-Detector.git)
   cd Fake-News-Phishing-Detector

```

2. **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. **Install Dependencies**
```bash
pip install -r backend/requirements.txt

```


4. **Train the Models (Mandatory before starting server)**
```bash
cd ml
python train_fake_news.py
python train_phishing.py

```


5. **Start the Flask Backend**
```bash
cd ../backend
python app.py

```


6. **Launch the Frontend**
Open `frontend/index.html` in your web browser.

---

## 🖥️ 4. User Guide

1. Navigate to the frontend UI.
2. Select the **Fake News** tab or **Phishing URL** tab.
3. **For News:** Paste the article text (minimum 10 characters) into the text box and click **Analyze Text**.
4. **For URLs:** Paste the web link (must include `http://` or `https://`) into the input box and click **Scan Link**.
5. The system will instantly display a confidence percentage and a visual probability doughnut graph indicating the risk level.

---

## 📡 5. API Documentation

The backend exposes two REST API endpoints. Both accept `POST` requests and return `JSON`.

### A. Predict Fake News

* **URL:** `/api/predict/news`
* **Method:** `POST`
* **Request Body:**
```json
{
  "text": "Your news article goes here..."
}

```


* **Success Response (200 OK):**
```json
{
  "prediction": "Fake",
  "confidence": 92.5
}

```


* **Error Response (400 Bad Request):**
```json
{
  "error": "Missing 'text' key in JSON payload"
}

```



### B. Predict Phishing URL

* **URL:** `/api/predict/url`
* **Method:** `POST`
* **Request Body:**
```json
{
  "url": "[http://example-phishing-site.com](http://example-phishing-site.com)"
}

```


* **Success Response (200 OK):**
```json
{
  "prediction": "Phishing",
  "confidence": 88.0
}

```



---

## 🛠️ 6. Developer Guide

### System Architecture Breakdown

* `frontend/`: Contains static UI assets. Uses the JavaScript Fetch API to send asynchronous JSON payloads.
* `backend/`: Flask WSGI server acting as a routing middleman. Includes `utils.py` for safe ML model deserialization.
* `ml/`: Standalone training scripts. These isolate data cleaning and vectorization logic away from the web server.
* `models/`: Directory where trained `.pkl` binaries are dynamically cached.

### Contribution Rules

1. **Updating AI Models:** If you alter the ML algorithms or utilize larger Kaggle datasets, you must completely re-run the scripts in the `ml/` folder to overwrite the previous `.pkl` files.
2. **Continuous Integration Testing:** Always validate changes to the routing engine by running the integration tests before executing a Git commit.
```bash
cd backend
python test_api.py
