import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Health Risk Microservice API")

# Dynamically load the serialized training artifact model
model_path = "model.pkl"
model = joblib.load(model_path) if os.path.exists(model_path) else None

class PredictionInput(BaseModel):
    features: list

@app.get("/")
def read_root():
    return {"status": "Online", "model_loaded": model is not None}

@app.post("/predict")
def predict(payload: PredictionInput):
    if not model:
        raise HTTPException(status_code=503, detail="Model binary artifact unavailable.")
    try:
        # Expected input format: Preprocessed numeric list array matching final feature schema length
        prediction = model.predict([payload.features])
        risk_labels = {0: 'Low', 1: 'Medium', 2: 'High'}
        return {"health_risk_prediction": risk_labels.get(int(prediction), "Unknown")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



