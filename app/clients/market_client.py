import logging
from datetime import date, timedelta
from functools import lru_cache

import yfinance as yf

logger = logging.getLogger(__name__)


class MarketClient:
    @lru_cache(maxsize=256)
    def get_ticker_history(self, symbol: str, ref_date: date, days: int):
        # TODO: wrap in async function
        # TODO: handle weekends/holidays
        df = yf.Ticker(symbol).history(
            start=ref_date - timedelta(days=days), end=ref_date + timedelta(days=1)
        )

        if df.empty:
            logger.warning(
                "No data for symbol %s between %s and %s",
                symbol,
                ref_date - timedelta(days=days),
                ref_date,
            )
            raise Exception(
                f"Failed to get ticker data on {symbol} for {ref_date} prevoius days:{days}"
            )

        logger.info("Symbol: %s, DataFrame: %s", symbol, df[["Close"]])
        return df.tail(days)
