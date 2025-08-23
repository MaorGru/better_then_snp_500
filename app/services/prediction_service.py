import logging
from datetime import date
from typing import Optional

import pandas as pd

from app.clients.market_client import MarketClient
from app.schemas.prediction_models import (
    ComparisonResult,
    ComparisonResultData,
    PredictionResult,
)

logger = logging.getLogger(__name__)

DEFAULT_WINDOW_DAYS: int = 5  # default moving-average window
SP500_TICKER: str = "^GSPC"  # Yahoo Finance symbol for S&P 500


class PredictionService:
    def __init__(
        self, market_client: MarketClient, window_days: int = DEFAULT_WINDOW_DAYS
    ) -> None:
        self.market: MarketClient = market_client
        self.window_days: int = window_days

    def predict_percentage_change_moving_average(
        self,
        symbol: str,
        reference_date: date,
        window_days: Optional[int] = None,
    ) -> PredictionResult:
        """
        Predict tomorrow's percentage change using a simple moving average (SMA):
          pct_change = (SMA(last `window_days` closes) - last_close) / last_close * 100
        The price history is taken up to and including `reference_date`.
        """
        days_to_use: int = window_days or self.window_days

        history: pd.DataFrame = self.market.get_ticker_history(
            symbol=symbol,
            ref_date=reference_date,
            days=days_to_use,
        )

        if history.empty or "Close" not in history:
            raise ValueError(f"No closing price data available for {symbol}.")

        recent_closes = history["Close"].tail(days_to_use)
        moving_average: float = float(recent_closes.mean())
        last_closing_price: float = float(recent_closes.iloc[-1])

        if last_closing_price == 0:
            predicted_percentage_change = 0.0
        else:
            predicted_percentage_change = (
                (moving_average - last_closing_price) / last_closing_price
            ) * 100.0

        # TODO: change to debug
        logger.info(
            "Prediction for %s: last_close=%.2f, SMA=%.2f, predicted_change=%.2f%%",
            symbol,
            last_closing_price,
            moving_average,
            predicted_percentage_change,
        )

        return PredictionResult(
            last_closing_price=last_closing_price,
            moving_average=moving_average,
            window_days=days_to_use,
            predicted_percentage_change=round(predicted_percentage_change, 2),
        )

    def compare_stock_with_sp500(
        self,
        symbol: str,
        reference_date: date,
        window_days: Optional[int] = None,
    ) -> ComparisonResultData:
        """
        Compare the stock's predicted percentage change vs. S&P 500 (^GSPC) over the same window.
        Returns a structured result with both predictions and an enum:
          OUTPERFORM | UNDERPERFORM | EQUAL
        """
        stock_result = self.predict_percentage_change_moving_average(
            symbol, reference_date, window_days
        )
        sp500_result = self.predict_percentage_change_moving_average(
            SP500_TICKER, reference_date, window_days
        )
        comparison = self.get_comparison_result(stock_result, sp500_result)

        # TODO: change to debug
        logger.info(
            "Comparison result for %s vs S&P 500: stock=%.2f%%, sp500=%.2f%%, outcome=%s",
            symbol,
            stock_result.predicted_percentage_change,
            sp500_result.predicted_percentage_change,
            comparison.name,
        )

        return ComparisonResultData(
            stock=stock_result,
            sp500=sp500_result,
            comparison=comparison,
        )

    @staticmethod
    def get_comparison_result(
        prediction_result_1: PredictionResult, prediction_result_2: PredictionResult
    ) -> ComparisonResult:
        if (
            prediction_result_1.predicted_percentage_change
            > prediction_result_2.predicted_percentage_change
        ):
            return ComparisonResult.OUTPERFORM
        elif (
            prediction_result_1.predicted_percentage_change
            < prediction_result_2.predicted_percentage_change
        ):
            return ComparisonResult.UNDERPERFORM
        return ComparisonResult.EQUAL
