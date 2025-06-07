import logging
from logging_loki import LokiHandler

LOKI_URL = "http://localhost:3100/loki/api/v1/push"
APP_NAME = "Python-Recipe-Api"

logger = logging.getLogger("app-logger")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    loki_handler = LokiHandler(
        url=LOKI_URL,
        tags={"application": APP_NAME},
        version="1",
    )
    logger.addHandler(loki_handler)

    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
