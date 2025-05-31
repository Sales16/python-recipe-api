from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    unidade = Column(String)


class Receita(Base):
    __tablename__ = "receitas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    modo_preparo = Column(Text)

    ingredientes = relationship("ReceitaIngrediente", back_populates="receita", cascade="all, delete-orphan")


class ReceitaIngrediente(Base):
    __tablename__ = "receita_ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    receita_id = Column(Integer, ForeignKey("receitas.id"))
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"))
    quantidade = Column(Float)

    receita = relationship("Receita", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente")