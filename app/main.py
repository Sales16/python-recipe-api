"""Módulo principal da aplicação."""

from fastapi import FastAPI
from database import Base, engine
from crud.ingredientes import router as ingredientes_router
from crud.receitas import router as receitas_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ingredientes_router)
app.include_router(receitas_router)
 