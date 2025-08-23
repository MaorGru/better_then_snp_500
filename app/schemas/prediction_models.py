from dataclasses import dataclass
from enum import Enum


class ComparisonResult(str, Enum):
    OUTPERFORM = "outperform"
    UNDERPERFORM = "underperform"
    EQUAL = "equal"


@dataclass(frozen=True)
class PredictionResult:
    last_closing_price: float
    moving_average: float
    window_days: int
    predicted_percentage_change: float


@dataclass(frozen=True)
class ComparisonResultData:
    stock: PredictionResult
    sp500: PredictionResult
    comparison: ComparisonResult
