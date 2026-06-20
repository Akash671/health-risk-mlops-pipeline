from pathlib import Path
import pandas as pd
import pytest

@pytest.fixture(scope="module")
def data_csv_path():
    """
    Resolve the data file path relative to the repository root (two levels up from tests/)
    and skip the tests if the file does not exist. This keeps unit test runs light and
    prevents CI failures when the dataset isn't available.
    """
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "data" / "healthcare_real_time_dataset.csv"
    if not csv_path.exists():
        pytest.skip(f"Dataset not found at {csv_path} — skipping integration-style ETL tests.")
    return csv_path

def test_raw_csv_asset_exists(data_csv_path):
    assert data_csv_path.exists(), f"Expected dataset at {data_csv_path}"

def test_raw_csv_schema_integrity(data_csv_path):
    # Read only the header to inspect column names (fast, no full load)
    df_header = pd.read_csv(data_csv_path, nrows=0)
    required_columns = ['Age', 'BMI', 'Health Risk Level']
    missing = [c for c in required_columns if c not in df_header.columns]
    assert not missing, f"Missing required columns in CSV: {missing}"
