import requests

# Your live backend endpoint
API_URL = "https://akash671-health-risk-mlops-pipeline.hf.space/predict"


#API_URL = "https://hf.space"

# 🔥 FIXED: Changed 'Chronic Disease History' to 'Chronic_Disease_History' 
# to satisfy the backend model's direct field name requirements.
raw_payload = {
    "Age": 48,
    "Gender": "Male",
    "BMI": 29.4,
    "Smoking Status": "Never",
    "Alcohol Consumption (per week)": 3,
    "Physical Activity (hours/week)": 4.5,
    "Sleep Duration (hours/day)": 7.0,
    "Chronic_Disease_History": "Hypertension", # Standardized field key
    "Stress Level (1-10)": 6
}

try:
    response = requests.post(API_URL, json=raw_payload)
    print("Upgraded API Status Code Response:", response.status_code)
    print("Upgraded Live Prediction Output:", response.json())
except Exception as e:
    print(f"Connection Error: {e}")
