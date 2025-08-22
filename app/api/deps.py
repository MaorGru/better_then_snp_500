from fastapi import Depends
from app.clients.market_client import MarketClient
from app.services.prediction_service import PredictionService

def get_market_client() -> MarketClient:
    return MarketClient()

def get_prediction_service(market: MarketClient = Depends(get_market_client)) -> PredictionService:
    return PredictionService(market_client=market)
