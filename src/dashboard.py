import requests
import streamlit as st

# Setup page presentation metrics
st.set_page_config(page_title="Patient Health Risk Assessment Core", page_icon="🏥", layout="centered")

st.title("🏥 Patient Health Risk Diagnostics Portal")
st.markdown("Enterprise MLOps Live Production Model Evaluation Node")
st.write("---")

# 1. Structure the visual input forms
st.subheader("👨‍⚕️ Enter Patient Vital Metrics")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Patient Age", min_value=1, max_value=120, value=45)
    bmi = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=60.0, value=24.5, step=0.1)
    alcohol = st.slider("Alcohol Consumption (drinks/week)", min_value=0, max_value=50, value=2)
    sleep = st.slider("Sleep Duration (hours/day)", min_value=1.0, max_value=14.0, value=7.5, step=0.5)

with col2:
    gender = st.selectbox("Gender Identity Profile", ["Male", "Female", "Other"])
    smoking = st.selectbox("Smoking Habits Tier", ["Never", "Current", "Former", "Unknown"])
    activity = st.number_input("Physical Activity (hours/week)", min_value=0.0, max_value=40.0, value=3.5, step=0.1)
    disease = st.selectbox("Chronic Disease History", ["None", "Hypertension", "Diabetes", "Heart Disease", "Other"])
    stress = st.slider("Psychological Stress Index (1-10)", min_value=1, max_value=10, value=4)

st.write("---")

# 2. Add the action execution trigger button
if st.button("🚀 Calculate Patient Health Risk Stratification", type="primary"):
    
    # 🔥 FIXED: Map the form variables directly to match your upgraded API requirements
    # Use the specific underscore key name "Chronic_Disease_History" to satisfy your current Pydantic model
    payload = {
        "Age": int(age),
        "Gender": str(gender),
        "BMI": float(bmi),
        "Smoking Status": str(smoking),
        "Alcohol Consumption (per week)": int(alcohol),
        "Physical Activity (hours/week)": float(activity),
        "Sleep Duration (hours/day)": float(sleep),
        "Chronic_Disease_History": str(disease), 
        "Stress Level (1-10)": int(stress)
    }
    
    # Direct live Hugging Face gateway serving URL
    API_ENDPOINT = "https://akash671-health-risk-mlops-pipeline.hf.space/predict"
    
    with st.spinner("Querying secure cloud prediction matrices..."):
        try:
            response = requests.post(API_ENDPOINT, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                # Extract the key name explicitly matching your upgraded FastAPI payload response scheme
                risk_tier = result.get("assigned_health_risk_tier", "Unknown")
                
                # 3. Present outputs with custom medical visual feedback blocks
                if risk_tier == "Low":
                    st.success(f"### Diagnostic Assignment: {risk_tier} Risk Profile")
                elif risk_tier == "Medium":
                    st.warning(f"### Diagnostic Assignment: {risk_tier} Risk Profile")
                elif risk_tier == "High":
                    st.error(f"### Diagnostic Assignment: {risk_tier} Risk Profile")
                else:
                    st.info(f"### Diagnostic Assignment: {risk_tier} Risk Profile")
                    
                st.info(f"💡 Analytical insight logged to server archive. Calculated for Age: {result.get('patient_age_analyzed')}")
            else:
                st.error(f"❌ API Error Core: Received Status Code {response.status_code}")
                st.json(response.json()) # Prints out the exact error payload from Pydantic for easier logging
                
        except Exception as e:
            st.error(f"Failed to communicate with live web service node: {e}")
