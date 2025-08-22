from fastapi import APIRouter
from app.schemas.prediction import PredictRequest, PredictResponse

router = APIRouter()


@router.post("/", response_model=PredictResponse)
async def predict(req: PredictRequest) -> PredictResponse:
    return PredictResponse(
        symbol=req.symbol,
        date=req.date,
        prediction=True,
        confidence=0.83
    )