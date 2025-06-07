from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
import logging

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None
Base = declarative_base()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not DATABASE_URL:
    logger.warning("DATABASE_URL não encontrado. Aguardando configuração do banco de dados...")
else:
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

def get_db():
    if SessionLocal is None:
        raise Exception("Banco de dados não conectado")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()