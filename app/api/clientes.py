"""Rotas da API para Cliente."""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import ClienteCreate, ClienteOut, ClienteUpdate
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService(db).criar_cliente(dados)


@router.get("", response_model=list[ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return ClienteService(db).listar_clientes()


@router.get("/{cliente_id}", response_model=ClienteOut)
def obter_cliente(cliente_id: uuid.UUID, db: Session = Depends(get_db)):
    return ClienteService(db).obter_cliente(cliente_id)


@router.put("/{cliente_id}", response_model=ClienteOut)
def atualizar_cliente(cliente_id: uuid.UUID, dados: ClienteUpdate, db: Session = Depends(get_db)):
    return ClienteService(db).atualizar_cliente(cliente_id, dados)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_cliente(cliente_id: uuid.UUID, db: Session = Depends(get_db)):
    ClienteService(db).remover_cliente(cliente_id)
