from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, RedirectResponse
from database import db_connected

router = APIRouter()

@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@router.get("/health")
def health_check():
    """
    Endpoint para verificar a saúde da aplicação.
    Retorna um status de 'ok' se a aplicação estiver funcionando corretamente.
    """
    if db_connected:
        return {"status": "ok"}
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "degraded", "db": "not_connected"}
        )