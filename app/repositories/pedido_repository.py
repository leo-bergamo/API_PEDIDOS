"""Camada de acesso a dados (repositories) para Pedido."""
import uuid

from sqlalchemy.orm import Session, joinedload

from app.models.models import ItemPedido, Pedido, StatusPedido


class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, cliente_id: uuid.UUID, itens: list[ItemPedido], valor_total) -> Pedido:
        pedido = Pedido(cliente_id=cliente_id, status=StatusPedido.PENDENTE, valor_total=valor_total)
        pedido.itens = itens
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def listar(self) -> list[Pedido]:
        return (
            self.db.query(Pedido)
            .options(joinedload(Pedido.itens))
            .order_by(Pedido.criado_em.desc())
            .all()
        )

    def buscar_por_id(self, pedido_id: uuid.UUID) -> Pedido | None:
        return (
            self.db.query(Pedido)
            .options(joinedload(Pedido.itens))
            .filter(Pedido.id == pedido_id)
            .first()
        )

    def atualizar_status(self, pedido: Pedido, status: StatusPedido) -> Pedido:
        pedido.status = status
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def remover(self, pedido: Pedido) -> None:
        self.db.delete(pedido)
        self.db.commit()
