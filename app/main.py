from fastapi import FastAPI
from app.core.errors import register_exception_handlers
from app.core.logging import setup_logging, get_logger
from app.core.lifespan import lifespan
from app.api.v1.router import api_router

# Configure logging before creating the app (important for uvicorn child processes)
setup_logging(level=None)  # or read from env

logger = get_logger("app.main")

app = FastAPI(
    title="Prediction Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")
register_exception_handlers(app)
@app.get("/health")
async def health():
    logger.info("Health check")
    return {"status": "ok"}
