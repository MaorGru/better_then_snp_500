from fastapi import APIRouter, Depends
from app.api.deps import get_prediction_service
from app.schemas.prediction import PredictRequest, PredictResponse
from app.schemas.prediction_models import ComparisonResult
from app.services.prediction_service import PredictionService

router = APIRouter()


@router.post("/", response_model=PredictResponse)
async def predict(req: PredictRequest, service: PredictionService = Depends(get_prediction_service)) -> PredictResponse:
    result = service.compare_stock_with_sp500(
        symbol=req.symbol,
        reference_date=req.date,
    )
    return PredictResponse(
        symbol=req.symbol,
        date=req.date,
        prediction=result.comparison == ComparisonResult.OUTPERFORM,
        confidence=1
    )