from pydantic import BaseModel
from typing import List

class IngredienteCreate(BaseModel):
    nome: str
    unidade: str
    
class Ingrediente(IngredienteCreate):
    id: int

    class Config:
        orm_mode = True

class IngredienteUpdate(BaseModel):
    nome: str
    unidade: str

class ReceitaIngredienteBase(BaseModel):
    ingrediente_id: int
    quantidade: float

class ReceitaIngredienteCreate(ReceitaIngredienteBase):
    pass

class ReceitaIngrediente(ReceitaIngredienteBase):
    id: int
    ingrediente: Ingrediente

    class Config:
        orm_mode = True

class ReceitaBase(BaseModel):
    nome: str
    modo_preparo: str

class ReceitaCreate(ReceitaBase):
    ingredientes: List[ReceitaIngredienteCreate]

class Receita(ReceitaBase):
    id: int
    ingredientes: List[ReceitaIngrediente]

    class Config:
        orm_mode = True

class ReceitaUpdate(ReceitaBase):
    ingredientes: List[ReceitaIngredienteCreate]
