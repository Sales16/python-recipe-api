from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from database import get_db
from schemas import ReceitaCreate, ReceitaUpdate, Receita
from models import Receita as ReceitaModel, ReceitaIngrediente as ReceitaIngredienteModel
from loki_config import logger

router = APIRouter()

@router.post("/receitas/", response_model=Receita)
def criar_receita(receita: ReceitaCreate, db: Session = Depends(get_db)):
    logger.info("Iniciando criação de nova receita.")
    try:
        nova_receita = ReceitaModel(
            nome=receita.nome,
            modo_preparo=receita.modo_preparo
        )
        db.add(nova_receita)
        db.commit()
        db.refresh(nova_receita)
        logger.info(f"Receita criada com ID {nova_receita.id}.")

        for item in receita.ingredientes:
            relacao = ReceitaIngredienteModel(
                receita_id=nova_receita.id,
                ingrediente_id=item.ingrediente_id,
                quantidade=item.quantidade
            )
            db.add(relacao)

        db.commit()
        logger.info(f"Relacionamentos de ingredientes salvos para a receita ID {nova_receita.id}.")
        db.refresh(nova_receita)

        return nova_receita

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao criar receita: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao criar receita: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")


@router.get("/receitas/", response_model=List[Receita])
def listar_receitas(db: Session = Depends(get_db)):
    logger.info("Listando todas as receitas.")
    try:
        receitas = db.query(ReceitaModel).all()
        logger.info(f"{len(receitas)} receita(s) encontrada(s).")
        return receitas
    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao listar receitas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao listar receitas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")


@router.put("/receitas/{receita_id}", response_model=Receita)
def atualizar_receita(receita_id: int, dados: ReceitaUpdate, db: Session = Depends(get_db)):
    logger.info(f"Iniciando atualização da receita ID {receita_id}.")
    try:
        receita = db.query(ReceitaModel).filter(ReceitaModel.id == receita_id).first()
        if not receita:
            logger.warning(f"Receita ID {receita_id} não encontrada.")
            raise HTTPException(status_code=404, detail="Receita não encontrada.")

        receita.nome = dados.nome
        receita.modo_preparo = dados.modo_preparo

        db.query(ReceitaIngredienteModel).filter(
            ReceitaIngredienteModel.receita_id == receita_id
        ).delete()

        for item in dados.ingredientes:
            novo_item = ReceitaIngredienteModel(
                receita_id=receita_id,
                ingrediente_id=item.ingrediente_id,
                quantidade=item.quantidade
            )
            db.add(novo_item)

        db.commit()
        db.refresh(receita)
        logger.info(f"Receita ID {receita_id} atualizada com sucesso.")
        return receita

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao atualizar receita ID {receita_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao atualizar receita ID {receita_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")


@router.delete("/receitas/{receita_id}")
def deletar_receita(receita_id: int, db: Session = Depends(get_db)):
    logger.info(f"Tentando deletar receita ID {receita_id}.")
    try:
        receita = db.query(ReceitaModel).filter(ReceitaModel.id == receita_id).first()
        if not receita:
            logger.warning(f"Receita ID {receita_id} não encontrada para exclusão.")
            raise HTTPException(status_code=404, detail="Receita não encontrada.")

        db.delete(receita)
        db.commit()

        logger.info(f"Receita ID {receita_id} deletada com sucesso.")
        return {"mensagem": f"Receita com ID {receita_id} deletada com sucesso!"}

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao deletar receita ID {receita_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao deletar receita ID {receita_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
