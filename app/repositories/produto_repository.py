"""Camada de acesso a dados (repositories) para Produto."""
import uuid

from sqlalchemy.orm import Session

from app.models.models import Produto
from app.schemas.schemas import ProdutoCreate, ProdutoUpdate


class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, dados: ProdutoCreate) -> Produto:
        produto = Produto(**dados.model_dump())
        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def listar(self) -> list[Produto]:
        return self.db.query(Produto).order_by(Produto.criado_em.desc()).all()

    def buscar_por_id(self, produto_id: uuid.UUID) -> Produto | None:
        return self.db.query(Produto).filter(Produto.id == produto_id).first()

    def atualizar(self, produto: Produto, dados: ProdutoUpdate) -> Produto:
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(produto, campo, valor)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def remover(self, produto: Produto) -> None:
        self.db.delete(produto)
        self.db.commit()
