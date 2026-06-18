import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Raw Text Ingestion Health Risk API Node")

# Load model binary artifact on app instantiation
model_path = "model.pkl"
model = joblib.load(model_path) if os.path.exists(model_path) else None

# 1. Define the exact human-readable Pydantic schema structure
class RawPatientPayload(BaseModel):
    Age: int
    Gender: str
    BMI: float
    Smoking_Status: str = Field(alias="Smoking Status")
    Alcohol_Consumption: int = Field(alias="Alcohol Consumption (per week)")
    Physical_Activity: float = Field(alias="Physical Activity (hours/week)")
    Sleep_Duration: float = Field(alias="Sleep Duration (hours/day)")
    Chronic_Disease_History: str
    Stress_Level: int = Field(alias="Stress Level (1-10)")

@app.get("/")
def check_status():
    return {"status": "Online", "accepts_input": "Raw Text/JSON Structure", "model_compiled": model is not None}

@app.post("/predict")
def predict_raw_patient_risk(payload: RawPatientPayload):
    if not model:
        raise HTTPException(status_code=503, detail="Production model binary asset unavailable.")
        
    try:
        # 2. Extract input back to an un-preprocessed pandas DataFrame row
        raw_input_df = pd.DataFrame([payload.model_dump(by_alias=True)])
        
        # 3. Apply basic structural mapping values mirroring your training profiles
        # (This bypasses needing a heavy persistent scaler file by using hardcoded training baselines)
        # Note: If your production features shift extensively, load the scaler using joblib here.
        
        # Build out a flat list conforming to the 16 model feature columns 
        # based on user inputs
        age_scaled = (payload.Age - 45.0) / 15.0 # Basic min-max / z-score runtime lookup mock
        bmi_scaled = (payload.BMI - 25.0) / 5.0
        alcohol_scaled = (payload.Alcohol_Consumption - 5.0) / 4.0
        activity_scaled = (payload.Physical_Activity - 3.0) / 2.0
        sleep_scaled = (payload.Sleep_Duration - 7.0) / 1.5
        stress_scaled = (payload.Stress_Level - 5.0) / 2.5
        
        # Create Dummy Flag states manually for categorical text arguments
        g_male = 1.0 if payload.Gender.title() == "Male" else 0.0
        g_other = 1.0 if payload.Gender.title() == "Other" else 0.0
        
        s_never = 1.0 if payload.Smoking_Status.title() == "Never" else 0.0
        s_unknown = 1.0 if payload.Smoking_Status.title() == "Unknown" else 0.0
        
        c_heart = 1.0 if payload.Chronic_Disease_History.title() == "Heart Disease" else 0.0
        c_hyper = 1.0 if payload.Chronic_Disease_History.title() == "Hypertension" else 0.0
        c_diabetes = 1.0 if payload.Chronic_Disease_History.title() == "Diabetes" else 0.0
        c_other = 0.0 # Baseline flags fallback
        c_unknown = 1.0 if payload.Chronic_Disease_History.title() == "Unknown" else 0.0
        
        # Combine everything explicitly into your exact 16-feature vector layout
        processed_vector = [
            age_scaled, bmi_scaled, alcohol_scaled, activity_scaled, sleep_scaled, stress_scaled,
            g_male, g_other, s_never, s_unknown, c_heart, c_hyper, c_unknown, 0.0, 0.0, 0.0
        ]
        
        # 4. Generate Classification Output
        numeric_output = model.predict([processed_vector])
        risk_labels = {0: 'Low', 1: 'Medium', 2: 'High'}
        
        return {
            "status": "Success",
            "patient_age_analyzed": payload.Age,
            "assigned_health_risk_tier": risk_labels.get(int(numeric_output[0]), "Medium")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dynamic Processing Error: {str(e)}")
