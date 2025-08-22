import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Happy Flow Test: Predict endpoint
def test_predict_endpoint_happy_flow():
    response = client.post(
        "/",
        json={"symbol": "AAPL", "date": "2025-08-22"}
    )

    assert response.status_code == 200
    assert response.json()["symbol"] == "AAPL"
    assert "prediction" in response.json()

# Error Test: Invalid request
def test_predict_endpoint_invalid_request():
    response = client.post(
        "/",
        json={"symbol": "", "date": "2025-08-22"}
    )

    assert response.status_code == 422

# Error Test: Symbol not in S&P 500
def test_predict_endpoint_symbol_not_in_sp500():
    response = client.post(
        "/",
        json={"symbol": "INVALID", "date": "2025-08-22"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Symbol not found in S&P 500"
