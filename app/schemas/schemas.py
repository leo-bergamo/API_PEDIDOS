"""Schemas Pydantic (DTOs) usados pela API."""
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.models import StatusPedido


# ---------- Cliente ----------
class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    telefone: str | None = Field(default=None, max_length=20)


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=120)
    email: EmailStr | None = None
    telefone: str | None = Field(default=None, max_length=20)


class ClienteOut(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    criado_em: datetime


# ---------- Produto ----------
class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=150)
    descricao: str | None = Field(default=None, max_length=500)
    preco: Decimal = Field(..., gt=0)
    estoque: int = Field(..., ge=0)


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=150)
    descricao: str | None = Field(default=None, max_length=500)
    preco: Decimal | None = Field(default=None, gt=0)
    estoque: int | None = Field(default=None, ge=0)


class ProdutoOut(ProdutoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    criado_em: datetime


# ---------- Item de Pedido ----------
class ItemPedidoCreate(BaseModel):
    produto_id: uuid.UUID
    quantidade: int = Field(..., gt=0)


class ItemPedidoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    produto_id: uuid.UUID
    quantidade: int
    preco_unitario: Decimal


# ---------- Pedido ----------
class PedidoCreate(BaseModel):
    cliente_id: uuid.UUID
    itens: list[ItemPedidoCreate] = Field(..., min_length=1)


class PedidoStatusUpdate(BaseModel):
    status: StatusPedido


class PedidoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    cliente_id: uuid.UUID
    status: StatusPedido
    valor_total: Decimal
    criado_em: datetime
    atualizado_em: datetime
    itens: list[ItemPedidoOut] = []
