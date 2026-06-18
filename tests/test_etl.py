import os
import pandas as pd
import pytest

def test_raw_csv_asset_exists():
    csv_path = os.path.join("data", "healthcare_real_time_dataset.csv")
    # Verify the engineering data pipeline source asset is accessible
    assert os.path.exists(csv_path) == True

def test_raw_csv_schema_integrity():
    csv_path = os.path.join("data", "healthcare_real_time_dataset.csv")
    df = pd.read_csv(csv_path)
    required_columns = ['Age', 'BMI', 'Health Risk Level']
    for col in required_columns:
        assert col in df.columns
