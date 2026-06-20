import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def run_etl():
    db_url = os.environ.get("SUPABASE_DB_URL")
    if not db_url:
        raise ValueError("Missing SUPABASE_DB_URL environment variable!")
    
    engine = create_engine(db_url)
    csv_path = os.path.join("data", "healthcare_real_time_dataset.csv")
    
    # Extract Raw Data
    raw_df = pd.read_csv(csv_path)
    
    # Sync and archive Raw Data to Supabase
    raw_df.to_sql("raw_patient_records", con=engine, if_exists="append", index=False)
    
    # Process Target Variable
    raw_df['Health Risk Level'] = raw_df['Health Risk Level'].astype(str).str.strip().str.title()
    target_mapping = {'Low': 0, 'Moderate': 1, 'High': 2}
    y = raw_df['Health Risk Level'].map(target_mapping).fillna(-1).astype(int)
    
    # Process Features
    num_cols = ['Age', 'BMI', 'Alcohol Consumption (per week)', 
                'Physical Activity (hours/week)', 'Sleep Duration (hours/day)', 'Stress Level (1-10)']
    cat_cols = ['Gender', 'Smoking Status', 'Chronic Disease History']
    
    raw_df[cat_cols] = raw_df[cat_cols].fillna('Unknown')
    
    # Impute & Clip Outliers
    num_imputer = SimpleImputer(strategy='median')
    num_imputed = num_imputer.fit_transform(raw_df[num_cols])
    q1, q3 = np.percentile(num_imputed, [25, 75], axis=0)
    iqr = q3 - q1
    num_clipped = np.clip(num_imputed, np.clip(q1 - 1.5 * iqr, 0, None), q3 + 1.5 * iqr)
    
    # Encode & Scale
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_cat = encoder.fit_transform(raw_df[cat_cols])
    
    scaler = StandardScaler()
    scaled_num = scaler.fit_transform(num_clipped)
    
    # Recombine & Sync Clean Data Tier
    processed_df = pd.concat([
        pd.DataFrame(scaled_num, columns=num_cols),
        pd.DataFrame(encoded_cat, columns=encoder.get_feature_names_out(cat_cols))
    ], axis=1)
    processed_df['Target_Health_Risk'] = y
    
    processed_df.to_sql("processed_patient_data", con=engine, if_exists="replace", index=False)
    print("ETL Pipeline completed successfully.")

if __name__ == "__main__":
    run_etl()
