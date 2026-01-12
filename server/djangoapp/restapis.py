import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env
load_dotenv()

# -----------------------------
# URLs for backend and sentiment analyzer
# -----------------------------
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# -----------------------------
# Generic GET request to backend
# -----------------------------
def get_request(endpoint, **kwargs):
    """
    Perform an HTTP GET request to the backend URL with optional URL parameters.
    
    :param endpoint: API endpoint (string), e.g., 'dealers'
    :param kwargs: keyword arguments to be added as URL parameters
    :return: JSON response as Python dictionary/list or None on error
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    
    request_url = backend_url.rstrip("/") + "/" + endpoint.lstrip("/")
    if params:
        request_url += "?" + params.rstrip("&")

    print(f"GET from {request_url}")
    
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return None

# -----------------------------
# Analyze sentiment of review text
# -----------------------------
def analyze_review_sentiments(text):
    """
    Calls the sentiment analyzer microservice to classify review text.
    
    :param text: string containing review text
    :return: sentiment label (string) - "positive", "neutral", or "negative"
    """
    try:
        # Ensure URL is correctly formatted
        request_url = sentiment_analyzer_url.rstrip("/") + "/analyze/" + text
        print(f"GET from {request_url}")
        
        response = requests.get(request_url)
        response.raise_for_status()
        sentiment_data = response.json()
        return sentiment_data.get("label", "neutral")  # default to neutral
    except requests.exceptions.RequestException as e:
        print(f"Sentiment analysis failed: {e}")
        return "neutral"

# -----------------------------
# POST a review to backend
# -----------------------------
def post_review(data_dict):
    """
    POST a review dictionary to backend API.
    
    :param data_dict: dict containing review data
    :return: JSON response from backend or None on error
    """
    try:
        request_url = backend_url.rstrip("/") + "/insert_review"
        print(f"POST to {request_url} with data: {data_dict}")
        
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"POST review failed: {e}")
        return None
