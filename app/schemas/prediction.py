from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator
import datetime

from app.clients.wikipedia_client import get_sp500_symbols

class PredictRequest(BaseModel):
    symbol: str = Field(..., description="Ticker symbol, e.g., AAPL")
    date: datetime.date = Field(..., description="Date for prediction (YYYY-MM-DD)")

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str):
        symbols = get_sp500_symbols()  # cached set
        if v.upper() not in symbols:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Symbol '{v}' is not in S&P 500 list"
            )
        return v.upper()  # normalize

class PredictResponse(BaseModel):
    symbol: str
    date: datetime.date
    prediction: bool
    confidence: float
