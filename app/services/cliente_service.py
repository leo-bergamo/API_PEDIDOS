"""Regras de negócio (services) para Cliente."""
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.cliente_repository import ClienteRepository
from app.schemas.schemas import ClienteCreate, ClienteUpdate


class ClienteService:
    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    def criar_cliente(self, dados: ClienteCreate):
        if self.repo.buscar_por_email(dados.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um cliente com este e-mail")
        return self.repo.criar(dados)

    def listar_clientes(self):
        return self.repo.listar()

    def obter_cliente(self, cliente_id: uuid.UUID):
        cliente = self.repo.buscar_por_id(cliente_id)
        if not cliente:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente não encontrado")
        return cliente

    def atualizar_cliente(self, cliente_id: uuid.UUID, dados: ClienteUpdate):
        cliente = self.obter_cliente(cliente_id)
        if dados.email and dados.email != cliente.email and self.repo.buscar_por_email(dados.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um cliente com este e-mail")
        return self.repo.atualizar(cliente, dados)

    def remover_cliente(self, cliente_id: uuid.UUID):
        cliente = self.obter_cliente(cliente_id)
        self.repo.remover(cliente)
