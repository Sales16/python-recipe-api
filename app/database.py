from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None
Base = declarative_base()

if not DATABASE_URL:
    print("DATABASE_URL não encontrado. Aguardando configuração do banco de dados...")
else:
    connected = False
    while not connected:
        try:
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            with engine.connect() as conn:
                pass
            connected = True
            print("Conexão com o banco de dados estabelecida.")
        except Exception as e:
            print(f"Banco de dados não encontrado ou indisponível: {e}")
            print("Tentando novamente em 20 segundos...")
            time.sleep(20)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
