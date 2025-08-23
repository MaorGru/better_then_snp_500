from unittest.mock import patch

import pandas as pd
import pytest
from tenacity import RetryError

from app.clients.wikipedia_client import WikipediaClient


@pytest.fixture(autouse=True)
def clear_wikipedia_cache():
    """Clear WikipediaClient cache before each test."""
    WikipediaClient._cache.clear()


def test_get_sp500_symbols_happy_flow():
    with patch("httpx.get") as mock_get, patch("pandas.read_html") as mock_read_html:
        mock_get.return_value.text = "<html></html>"
        mock_read_html.return_value = [
            pd.DataFrame({"Symbol": ["AAPL", "MSFT", "GOOGL"]})
        ]

        result = WikipediaClient.get_sp500_symbols()

        assert result == {"AAPL", "MSFT", "GOOGL"}


def test_get_sp500_symbols_http_error():
    with patch("httpx.get") as mock_get:
        mock_get.side_effect = Exception("HTTP Error")

        with pytest.raises(RetryError):
            WikipediaClient.get_sp500_symbols()
