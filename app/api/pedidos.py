"""Rotas da API para Pedido."""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import PedidoCreate, PedidoOut, PedidoStatusUpdate
from app.services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    return PedidoService(db).criar_pedido(dados)


@router.get("", response_model=list[PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    return PedidoService(db).listar_pedidos()


@router.get("/{pedido_id}", response_model=PedidoOut)
def obter_pedido(pedido_id: uuid.UUID, db: Session = Depends(get_db)):
    return PedidoService(db).obter_pedido(pedido_id)


@router.patch("/{pedido_id}/status", response_model=PedidoOut)
def atualizar_status_pedido(pedido_id: uuid.UUID, dados: PedidoStatusUpdate, db: Session = Depends(get_db)):
    return PedidoService(db).atualizar_status(pedido_id, dados.status)


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_pedido(pedido_id: uuid.UUID, db: Session = Depends(get_db)):
    PedidoService(db).remover_pedido(pedido_id)
