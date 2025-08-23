from datetime import date
from unittest.mock import MagicMock

import pandas as pd
import pytest

from app.schemas.prediction_models import (
    ComparisonResult,
    ComparisonResultData,
    PredictionResult,
)
from app.services.prediction_service import PredictionService


@pytest.fixture
def mock_market_client():
    return MagicMock()


@pytest.fixture
def prediction_service(mock_market_client):
    return PredictionService(market_client=mock_market_client)


def test_predict_percentage_change_happy_flow(prediction_service, mock_market_client):
    mock_market_client.get_ticker_history.return_value = pd.DataFrame(
        {"Close": [100, 102, 104, 106, 108]}
    )

    result = prediction_service.predict_percentage_change_moving_average(
        symbol="AAPL", reference_date=date(2025, 8, 22), window_days=5
    )

    assert isinstance(result, PredictionResult)
    assert result.last_closing_price == 108
    assert result.moving_average == 104
    assert result.predicted_percentage_change == pytest.approx(-3.7, 0.1)


def test_predict_percentage_change_missing_data(prediction_service, mock_market_client):
    mock_market_client.get_ticker_history.return_value = pd.DataFrame()

    with pytest.raises(ValueError, match="No closing price data available"):
        prediction_service.predict_percentage_change_moving_average(
            symbol="AAPL", reference_date=date(2025, 8, 22), window_days=5
        )


def test_compare_stock_with_sp500_happy_flow(prediction_service, mock_market_client):
    mock_market_client.get_ticker_history.side_effect = [
        pd.DataFrame({"Close": [100, 102, 104, 106, 108]}),  # Stock data
        pd.DataFrame({"Close": [200, 202, 204, 206, 208]}),  # S&P 500 data
    ]

    result = prediction_service.compare_stock_with_sp500(
        symbol="AAPL", reference_date=date(2025, 8, 22), window_days=5
    )

    assert isinstance(result, ComparisonResultData)
    assert result.comparison == ComparisonResult.UNDERPERFORM


def test_compare_stock_with_sp500_invalid_data(prediction_service, mock_market_client):
    mock_market_client.get_ticker_history.side_effect = [
        pd.DataFrame(),  # Stock data missing
        pd.DataFrame({"Close": [200, 202, 204, 206, 208]}),  # S&P 500 data
    ]

    with pytest.raises(ValueError, match="No closing price data available"):
        prediction_service.compare_stock_with_sp500(
            symbol="AAPL", reference_date=date(2025, 8, 22), window_days=5
        )
