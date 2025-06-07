from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
import logging

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()
engine = None
SessionLocal = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    global engine, SessionLocal

    if not DATABASE_URL:
        logger.warning("DATABASE_URL não configurado.")
        return

    connected = False
    while not connected:
        try:
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            with engine.connect() as conn:
                pass
            connected = True
            logger.info("Conexão com o banco de dados estabelecida.")
        except Exception as e:
            logger.error(f"Banco de dados não encontrado ou indisponível: {e}")
            logger.info("Tentando novamente em 20 segundos...")
            time.sleep(20)

init_db()

def get_db():
    global SessionLocal, engine

    if SessionLocal is None:
        logger.warning("Tentando reconectar ao banco de dados em tempo de execução.")
        init_db()

    if SessionLocal is None:
        raise Exception("Banco de dados não conectado")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
