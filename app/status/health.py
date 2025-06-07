from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from loki_config import logger
from prometheus_client import Counter

router = APIRouter()

health_check_counts = Counter("health_check_counts", "Número de chamadas do /health")

@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@router.get("/health")
def health_check():
    health_check_counts.inc()
    logger.info("Health check endpoint called.")
    return {"status": "ok"}