import pytest
from unittest.mock import patch
from app.clients.wikipedia_client import WikipediaClient

# Happy Flow Test: Get S&P 500 symbols
def test_get_sp500_symbols_happy_flow():
    with patch("httpx.get") as mock_get, patch("pandas.read_html") as mock_read_html:
        mock_get.return_value.text = "<html></html>"
        mock_read_html.return_value = [{"Symbol": ["AAPL", "MSFT", "GOOGL"]}]

        result = WikipediaClient.get_sp500_symbols()

        assert result == {"AAPL", "MSFT", "GOOGL"}

# Error Test: Handle HTTP error
def test_get_sp500_symbols_http_error():
    with patch("httpx.get") as mock_get:
        mock_get.side_effect = Exception("HTTP Error")

        with pytest.raises(Exception, match="HTTP Error"):
            WikipediaClient.get_sp500_symbols()
