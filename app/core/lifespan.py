from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx
from app.core.logging import get_logger

logger = get_logger("app.lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create shared resources once
    app.state.httpx_client = httpx.AsyncClient(timeout=20)
    logger.info("HTTP client initialized")

    # Example: place other singletons here (Redis, DB engine, services, threadpools, etc.)
    # app.state.prediction_service = PredictionService(...)

    try:
        yield
    finally:
        # Shutdown: close resources
        await app.state.httpx_client.aclose()
        logger.info("HTTP client closed")
