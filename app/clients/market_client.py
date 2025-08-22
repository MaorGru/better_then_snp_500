from datetime import date, timedelta
import logging

import yfinance as yf

logger = logging.getLogger(__name__)


class MarketClient:
    def get_ticker_history(self, symbol: str, ref_date: date, days: int):
        #TODO: wrap in async function
        #TODO: handle weekends/holidays
        df = yf.Ticker(symbol).history(
            start=ref_date - timedelta(days=days),
            end=ref_date + timedelta(days=1)
        )
        #TODO: add validation on data
        return df.tail(days)