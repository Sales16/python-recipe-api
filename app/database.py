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
db_connected = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def try_connect_db():
    global engine, SessionLocal, db_connected
    if not DATABASE_URL:
        logger.warning("DATABASE_URL não encontrado. Aguardando configuração do banco de dados...")
        return
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with engine.connect() as conn:
            pass
        db_connected = True
        logger.info("Conexão com o banco de dados estabelecida.")
    except Exception as e:
        db_connected = False
        logger.error(f"Banco de dados não encontrado ou indisponível: {e}")

try_connect_db()

def get_db():
    global db_connected
    if not db_connected:
        try_connect_db()  # Tenta conectar novamente
        if not db_connected:
            raise Exception("Banco de dados não conectado")
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
