"""Regras de negócio (services) para Pedido."""
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import ItemPedido, StatusPedido
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.schemas import PedidoCreate

# Transições de status permitidas (regra de negócio simples de workflow de pedido)
TRANSICOES_PERMITIDAS: dict[StatusPedido, set[StatusPedido]] = {
    StatusPedido.PENDENTE: {StatusPedido.PROCESSANDO, StatusPedido.CANCELADO},
    StatusPedido.PROCESSANDO: {StatusPedido.ENVIADO, StatusPedido.CANCELADO},
    StatusPedido.ENVIADO: {StatusPedido.ENTREGUE},
    StatusPedido.ENTREGUE: set(),
    StatusPedido.CANCELADO: set(),
}


class PedidoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PedidoRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.produto_repo = ProdutoRepository(db)

    def criar_pedido(self, dados: PedidoCreate):
        cliente = self.cliente_repo.buscar_por_id(dados.cliente_id)
        if not cliente:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente não encontrado")

        itens_orm: list[ItemPedido] = []
        valor_total = 0
        for item in dados.itens:
            produto = self.produto_repo.buscar_por_id(item.produto_id)
            if not produto:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"Produto {item.produto_id} não encontrado")
            if produto.estoque < item.quantidade:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    f"Estoque insuficiente para o produto '{produto.nome}'",
                )
            produto.estoque -= item.quantidade
            subtotal = produto.preco * item.quantidade
            valor_total += subtotal
            itens_orm.append(
                ItemPedido(
                    produto_id=produto.id,
                    quantidade=item.quantidade,
                    preco_unitario=produto.preco,
                )
            )

        pedido = self.repo.criar(dados.cliente_id, itens_orm, valor_total)
        self.db.commit()
        return pedido

    def listar_pedidos(self):
        return self.repo.listar()

    def obter_pedido(self, pedido_id: uuid.UUID):
        pedido = self.repo.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")
        return pedido

    def atualizar_status(self, pedido_id: uuid.UUID, novo_status: StatusPedido):
        pedido = self.obter_pedido(pedido_id)
        permitido = TRANSICOES_PERMITIDAS.get(pedido.status, set())
        if novo_status != pedido.status and novo_status not in permitido:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f"Não é possível mudar o status de '{pedido.status.value}' para '{novo_status.value}'",
            )
        return self.repo.atualizar_status(pedido, novo_status)

    def remover_pedido(self, pedido_id: uuid.UUID):
        pedido = self.obter_pedido(pedido_id)
        self.repo.remover(pedido)
