"""Rotas da API para Produto."""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import ProdutoCreate, ProdutoOut, ProdutoUpdate
from app.services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=ProdutoOut, status_code=status.HTTP_201_CREATED)
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    return ProdutoService(db).criar_produto(dados)


@router.get("", response_model=list[ProdutoOut])
def listar_produtos(db: Session = Depends(get_db)):
    return ProdutoService(db).listar_produtos()


@router.get("/{produto_id}", response_model=ProdutoOut)
def obter_produto(produto_id: uuid.UUID, db: Session = Depends(get_db)):
    return ProdutoService(db).obter_produto(produto_id)


@router.put("/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(produto_id: uuid.UUID, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    return ProdutoService(db).atualizar_produto(produto_id, dados)


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(produto_id: uuid.UUID, db: Session = Depends(get_db)):
    ProdutoService(db).remover_produto(produto_id)
