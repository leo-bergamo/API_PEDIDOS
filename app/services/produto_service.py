"""Regras de negócio (services) para Produto."""
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.produto_repository import ProdutoRepository
from app.schemas.schemas import ProdutoCreate, ProdutoUpdate


class ProdutoService:
    def __init__(self, db: Session):
        self.repo = ProdutoRepository(db)

    def criar_produto(self, dados: ProdutoCreate):
        return self.repo.criar(dados)

    def listar_produtos(self):
        return self.repo.listar()

    def obter_produto(self, produto_id: uuid.UUID):
        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
        return produto

    def atualizar_produto(self, produto_id: uuid.UUID, dados: ProdutoUpdate):
        produto = self.obter_produto(produto_id)
        return self.repo.atualizar(produto, dados)

    def remover_produto(self, produto_id: uuid.UUID):
        produto = self.obter_produto(produto_id)
        self.repo.remover(produto)
