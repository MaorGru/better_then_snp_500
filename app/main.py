from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Prediction Service",
    version="1.0.0",
)

# Include API routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
