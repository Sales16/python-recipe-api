from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from database import get_db
from schemas import IngredienteCreate, IngredienteUpdate, Ingrediente
from models import Ingrediente as IngredienteModel
from loki_config import logger 

router = APIRouter()

@router.post("/ingredientes/")
def criar_ingrediente(ingrediente: IngredienteCreate, db: Session = Depends(get_db)):
    logger.info(f"Tentando criar ingrediente: {ingrediente.nome}")
    try:
        ingrediente_existente = db.query(IngredienteModel).filter(IngredienteModel.nome == ingrediente.nome).first()
        if ingrediente_existente:
            logger.warning(f"Ingre­diente '{ingrediente.nome}' já existe.")
            raise HTTPException(status_code=400, detail="Ingrediente já existe.")

        novo_ingrediente = IngredienteModel(nome=ingrediente.nome, unidade=ingrediente.unidade)
        db.add(novo_ingrediente)
        db.commit()
        db.refresh(novo_ingrediente)

        logger.info(f"Ingre­diente criado com sucesso: ID {novo_ingrediente.id}")
        return {
            "mensagem": "Ingrediente criado com sucesso!",
            "id": novo_ingrediente.id,
            "nome": novo_ingrediente.nome,
            "unidade": novo_ingrediente.unidade
        }

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao criar ingrediente: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao criar ingrediente: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")


@router.get("/ingredientes/", response_model=List[Ingrediente])
def listar_ingredientes(db: Session = Depends(get_db)):
    logger.info("Listando todos os ingredientes.")
    try:
        ingredientes = db.query(IngredienteModel).all()
        logger.info(f"{len(ingredientes)} ingrediente(s) encontrado(s).")
        return ingredientes
    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao listar ingredientes: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao listar ingredientes: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")


@router.put("/ingredientes/{ingrediente_id}")
def atualizar_ingrediente(ingrediente_id: int, dados: IngredienteUpdate, db: Session = Depends(get_db)):
    logger.info(f"Iniciando atualização do ingrediente ID {ingrediente_id}.")
    try:
        ingrediente = db.query(IngredienteModel).filter(IngredienteModel.id == ingrediente_id).first()
        if not ingrediente:
            logger.warning(f"Ingrediente ID {ingrediente_id} não encontrado.")
            raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")

        ingrediente.nome = dados.nome
        ingrediente.unidade = dados.unidade

        db.commit()
        db.refresh(ingrediente)

        logger.info(f"Ingrediente ID {ingrediente_id} atualizado com sucesso.")
        return {
            "mensagem": "Ingrediente atualizado com sucesso!",
            "ingrediente": {
                "id": ingrediente.id,
                "nome": ingrediente.nome,
                "unidade": ingrediente.unidade
            }
        }

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao atualizar ingrediente ID {ingrediente_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao atualizar ingrediente ID {ingrediente_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")


@router.delete("/ingredientes/{ingrediente_id}")
def deletar_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    logger.info(f"Tentando deletar ingrediente ID {ingrediente_id}.")
    try:
        ingrediente = db.query(IngredienteModel).filter(IngredienteModel.id == ingrediente_id).first()
        if not ingrediente:
            logger.warning(f"Ingrediente ID {ingrediente_id} não encontrado para exclusão.")
            raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")

        db.delete(ingrediente)
        db.commit()

        logger.info(f"Ingrediente ID {ingrediente_id} deletado com sucesso.")
        return {"mensagem": f"Ingrediente com ID {ingrediente_id} deletado com sucesso!"}

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao deletar ingrediente ID {ingrediente_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao deletar ingrediente ID {ingrediente_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
