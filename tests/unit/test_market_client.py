import pytest
from datetime import date, timedelta
from unittest.mock import MagicMock, patch
from app.clients.market_client import MarketClient
import pandas as pd

@pytest.fixture
def market_client():
    return MarketClient()

# Happy Flow Test: Get ticker history
def test_get_ticker_history_happy_flow(market_client):
    with patch("yfinance.Ticker.history") as mock_history:
        mock_history.return_value = pd.DataFrame({"Close": [100, 102, 104, 106, 108]})

        result = market_client.get_ticker_history(
            symbol="AAPL",
            ref_date=date(2025, 8, 22),
            days=5
        )

        assert "Close" in result
        assert len(result["Close"]) == 5

# Error Test: Handle missing data
def test_get_ticker_history_missing_data(market_client):
    with patch("yfinance.Ticker.history") as mock_history:
        mock_history.return_value = pd.DataFrame({})

        with pytest.raises(Exception, match="Failed to get ticker data on AAPL for 2025-08-22 prevoius days:5"):
            market_client.get_ticker_history(
              symbol="AAPL",
              ref_date=date(2025, 8, 22),
              days=5
            )
    