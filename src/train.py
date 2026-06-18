import os
import joblib
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier

def train_model():
    db_url = os.environ.get("SUPABASE_DB_URL")
    engine = create_engine(db_url)
    
    # 1. Pull the preprocessed cumulative data matrix to fit the model
    df = pd.read_sql_table("processed_patient_data", con=engine)
    df = df[df['Target_Health_Risk'] != -1]
    
    X = df.drop(columns=['Target_Health_Risk', 'id'], errors='ignore')
    y = df['Target_Health_Risk']
    
    # Train the Production Model Architecture
    model = RandomForestClassifier(
        n_estimators=100, max_depth=5, min_samples_leaf=4, 
        class_weight='balanced', random_state=42
    )
    model.fit(X, y)
    
    # Export Model Deployment Package Artifact
    joblib.dump(model, 'model.pkl')
    print("🎉 Success: model.pkl saved successfully.")

if __name__ == "__main__":
    train_model()
