from fastapi.testclient import TestClient
import pytest
from src.app import app


@pytest.fixture(scope="module")
def client():
    """Create a TestClient fixture for reuse across tests.

    Using a fixture ensures proper startup/shutdown of the FastAPI app and
    makes it easy to add more endpoint tests that reuse the same client.
    """
    with TestClient(app) as c:
        yield c


def test_health_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    # Ensure JSON response and expected status value
    assert response.headers.get("content-type", "").startswith("application/json")
    assert response.json().get("status") == "Online"
