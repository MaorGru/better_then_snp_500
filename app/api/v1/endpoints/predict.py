from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def predict():
    # Empty stub for now
    return {"message": "predict endpoint placeholder"}
