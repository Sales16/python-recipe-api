from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import IngredienteCreate, IngredienteUpdate, Ingrediente
from models import Ingrediente as IngredienteModel
from sqlalchemy.exc import SQLAlchemyError
from typing import List

router = APIRouter()

@router.post("/ingredientes/")
def criar_ingrediente(ingrediente: IngredienteCreate, db: Session = Depends(get_db)):
    try:
        ingrediente_existente = db.query(IngredienteModel).filter(IngredienteModel.nome == ingrediente.nome).first()
        if ingrediente_existente:
            raise HTTPException(status_code=400, detail="Ingrediente já existe.")

        novo_ingrediente = IngredienteModel(nome=ingrediente.nome, unidade=ingrediente.unidade)
        db.add(novo_ingrediente)
        db.commit()
        db.refresh(novo_ingrediente)
        return {"mensagem": "Ingrediente criado com sucesso!", "id": novo_ingrediente.id, "nome": novo_ingrediente.nome, "unidade": novo_ingrediente.unidade}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")


@router.get("/ingredientes/", response_model=List[Ingrediente])
def listar_ingredientes(db: Session = Depends(get_db)):
    try:
        ingredientes = db.query(IngredienteModel).all()
        return ingredientes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
    

@router.put("/ingredientes/{ingrediente_id}")
def atualizar_ingrediente(ingrediente_id: int, dados: IngredienteUpdate, db: Session = Depends(get_db)):
    try:
        ingrediente = db.query(IngredienteModel).filter(IngredienteModel.id == ingrediente_id).first()

        if not ingrediente:
            raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")

        ingrediente.nome = dados.nome
        ingrediente.unidade = dados.unidade

        db.commit()
        db.refresh(ingrediente)

        return {"mensagem": "Ingrediente atualizado com sucesso!", "ingrediente": {
            "id": ingrediente.id,
            "nome": ingrediente.nome,
            "unidade": ingrediente.unidade
        }}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")    
    

@router.delete("/ingredientes/{ingrediente_id}")
def deletar_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    try:
        ingrediente = db.query(IngredienteModel).filter(IngredienteModel.id == ingrediente_id).first()

        if not ingrediente:
            raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")

        db.delete(ingrediente)
        db.commit()

        return {"mensagem": f"Ingrediente com ID {ingrediente_id} deletado com sucesso!"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")

