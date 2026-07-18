import unittest
import json
from app import create_app

class TestFraudDetectorAPI(unittest.TestCase):
    """
    Test suite for the Fake News and Phishing Detection REST APIs.
    Inherits from unittest.TestCase.
    """

    # ==========================================
    # 1. Setup Phase
    # ==========================================
    def setUp(self):
        """
        This function runs automatically BEFORE every single test.
        It sets up a simulated server so we don't need to run app.py manually.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Sample Data for Testing
        self.fake_news_payload = {
            "text": "BREAKING: Aliens have landed and are giving away free iPhones!"
        }
        self.phishing_url_payload = {
            "url": "http://192.168.1.1/secure-login-paypal"
        }
        self.empty_payload = {}

    # ==========================================
    # 2. Testing News Endpoint
    # ==========================================
    def test_news_endpoint_success(self):
        """
        Tests if the /api/predict/news endpoint successfully processes valid JSON text.
        """
        # Simulate a POST request from the frontend
        response = self.client.post(
            '/api/predict/news', 
            json=self.fake_news_payload
        )
        
        # Parse the JSON response
        data = json.loads(response.data)
        
        # Assertions (Checking if the output matches our expectations)
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', data)
        self.assertIn('confidence', data)

    def test_news_endpoint_missing_data(self):
        """
        Edge Case: Tests how the server handles a request with no text.
        """
        response = self.client.post(
            '/api/predict/news', 
            json=self.empty_payload
        )
        
        data = json.loads(response.data)
        
        # We expect a 400 Bad Request error
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "Missing 'text' key in JSON payload")

    # ==========================================
    # 3. Testing URL Endpoint
    # ==========================================
    def test_url_endpoint_success(self):
        """
        Tests if the /api/predict/url endpoint successfully processes valid JSON URLs.
        """
        response = self.client.post(
            '/api/predict/url', 
            json=self.phishing_url_payload
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', data)
        self.assertIn('confidence', data)

    def test_url_endpoint_missing_data(self):
        """
        Edge Case: Tests how the server handles a request with no URL.
        """
        response = self.client.post(
            '/api/predict/url', 
            json=self.empty_payload
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "Missing 'url' key in JSON payload")

# ==========================================
# 4. Execution
# ==========================================
if __name__ == '__main__':
    # Runs all functions starting with the word 'test'
    unittest.main()