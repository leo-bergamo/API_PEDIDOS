"""Ponto de entrada da API de Pedidos."""
import logging
import time

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.api import clientes, pedidos, produtos
from app.core.config import settings
from app.core.database import Base, engine
from app.models import models  # noqa: F401  (garante o registro das tabelas no metadata)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-pedidos")

app = FastAPI(
    title=settings.app_name,
    description="API para gerenciamento de Clientes, Produtos e Pedidos",
    version="1.0.0",
)


def _aguardar_banco_e_criar_tabelas(tentativas: int = 10, espera_segundos: int = 3) -> None:
    """Aguarda o PostgreSQL ficar disponível e cria as tabelas, se necessário.

    Necessário porque o container da aplicação pode subir antes do banco
    estar pronto para aceitar conexões (docker compose não garante ordem de prontidão).
    """
    for tentativa in range(1, tentativas + 1):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Conexão com o banco de dados estabelecida e tabelas verificadas.")
            return
        except OperationalError as exc:
            logger.warning(
                "Banco de dados indisponível (tentativa %s/%s): %s", tentativa, tentativas, exc
            )
            time.sleep(espera_segundos)
    raise RuntimeError("Não foi possível conectar ao banco de dados após múltiplas tentativas.")


@app.on_event("startup")
def on_startup() -> None:
    _aguardar_banco_e_criar_tabelas()


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(clientes.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
