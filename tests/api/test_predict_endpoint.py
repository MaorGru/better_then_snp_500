import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

PREDICT_ENDPOINT = "/api/v1/predict/"

# Mock S&P 500 symbols
@pytest.fixture(autouse=True)
def mock_sp500_symbols():
    with patch("app.clients.wikipedia_client.WikipediaClient.get_sp500_symbols", return_value={"AAPL", "MSFT", "GOOGL"}):
        yield

# Happy Flow Test: Predict endpoint
def test_predict_endpoint_happy_flow():
    response = client.post(
        PREDICT_ENDPOINT,
        json={"symbol": "AAPL", "date": "2025-08-22"}
    )

    assert response.status_code == 200
    assert response.json()["symbol"] == "AAPL"
    assert "prediction" in response.json()

# Error Test: Invalid request
def test_predict_endpoint_invalid_request():
    response = client.post(
        PREDICT_ENDPOINT,
        json={"symbol": "", "date": "2025-08-22"}
    )

    assert response.status_code == 422

# Error Test: Symbol not in S&P 500
def test_predict_endpoint_symbol_not_in_sp500():
    response = client.post(
        PREDICT_ENDPOINT,
        json={"symbol": "CCC", "date": "2025-08-22"}
    )

    assert response.status_code == 422
    assert response.json()["details"] == "Symbol 'CCC' is not in S&P 500 list"
