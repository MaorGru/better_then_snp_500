from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.errors import register_exception_handlers

app = FastAPI(
    title="Prediction Service",
    version="1.0.0",
)

# Include API routers
app.include_router(api_router, prefix="/api/v1")
register_exception_handlers(app)

@app.get("/health")
async def health():
    return {"status": "ok"}
