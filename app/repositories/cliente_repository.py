"""Camada de acesso a dados (repositories) para Cliente."""
import uuid

from sqlalchemy.orm import Session

from app.models.models import Cliente
from app.schemas.schemas import ClienteCreate, ClienteUpdate


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, dados: ClienteCreate) -> Cliente:
        cliente = Cliente(**dados.model_dump())
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def listar(self) -> list[Cliente]:
        return self.db.query(Cliente).order_by(Cliente.criado_em.desc()).all()

    def buscar_por_id(self, cliente_id: uuid.UUID) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def buscar_por_email(self, email: str) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.email == email).first()

    def atualizar(self, cliente: Cliente, dados: ClienteUpdate) -> Cliente:
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(cliente, campo, valor)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def remover(self, cliente: Cliente) -> None:
        self.db.delete(cliente)
        self.db.commit()
