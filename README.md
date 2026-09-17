# API Pedidos

API REST para gerenciamento de **Clientes**, **Produtos** e **Pedidos**, desenvolvida com **FastAPI** e **PostgreSQL**, totalmente containerizada com Docker.

## Integrantes do grupo

- Cauã Petras

## Tecnologias utilizadas

- **Python 3.12**
- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **PostgreSQL 16** — banco de dados relacional
- **Docker / Docker Compose** — containerização e orquestração
- **Pydantic** — validação de dados

## Arquitetura do projeto

```
/
├── app/
│   ├── main.py            # ponto de entrada da aplicação (FastAPI)
│   ├── api/                # rotas HTTP (controllers)
│   │   ├── clientes.py
│   │   ├── produtos.py
│   │   └── pedidos.py
│   ├── services/           # regras de negócio
│   │   ├── cliente_service.py
│   │   ├── produto_service.py
│   │   └── pedido_service.py
│   ├── repositories/       # acesso a dados (SQLAlchemy)
│   │   ├── cliente_repository.py
│   │   ├── produto_repository.py
│   │   └── pedido_repository.py
│   ├── models/              # modelos ORM
│   │   └── models.py
│   ├── schemas/              # schemas Pydantic (DTOs)
│   │   └── schemas.py
│   └── core/                 # configuração e conexão com banco
│       ├── config.py
│       └── database.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

A aplicação segue uma arquitetura em camadas: **API (rotas)** → **Service (regras de negócio)** → **Repository (acesso a dados)** → **Model (ORM)**.

## Modelo de domínio

- **Cliente**: `id`, `nome`, `email` (único), `telefone`, `criado_em`
- **Produto**: `id`, `nome`, `descricao`, `preco`, `estoque`, `criado_em`
- **Pedido**: `id`, `cliente_id`, `status`, `valor_total`, `criado_em`, `atualizado_em`, `itens[]`
- **ItemPedido**: `id`, `pedido_id`, `produto_id`, `quantidade`, `preco_unitario`

### Status do pedido e transições permitidas

`PENDENTE → PROCESSANDO → ENVIADO → ENTREGUE`, com possibilidade de `CANCELADO` a partir de `PENDENTE` ou `PROCESSANDO`.

Ao criar um pedido, o estoque dos produtos é validado e decrementado, e o `valor_total` é calculado automaticamente a partir dos itens.

## Como executar

### Pré-requisitos

- Docker e Docker Compose instalados (não é necessário Python, PostgreSQL ou qualquer dependência instalada localmente).

### Passos

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
docker compose up -d --build
```

A aplicação estará disponível em:

- **API**: http://localhost:8000
- **Documentação interativa (Swagger)**: http://localhost:8000/docs
- **Documentação alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

O serviço `pedidos` aguarda automaticamente o banco de dados (`postgres`) ficar disponível e cria as tabelas na primeira inicialização — nenhum passo manual adicional é necessário.

### Variáveis de ambiente

O `docker-compose.yml` já define valores padrão de ambiente (usuário, senha e nome do banco) suficientes para rodar em uma máquina limpa. O arquivo `.env.example` documenta essas variáveis caso se deseje executar a aplicação fora do Docker (ex.: localmente com um PostgreSQL próprio) — nesse caso, copie-o para `.env` e ajuste os valores.

### Parar a aplicação

```bash
docker compose down
```

Para remover também o volume de dados do banco:

```bash
docker compose down -v
```

## Principais endpoints

| Método | Rota                        | Descrição                                  |
|--------|-----------------------------|---------------------------------------------|
| POST   | `/clientes`                 | Cria um cliente                             |
| GET    | `/clientes`                 | Lista clientes                              |
| GET    | `/clientes/{id}`            | Obtém um cliente                            |
| PUT    | `/clientes/{id}`            | Atualiza um cliente                         |
| DELETE | `/clientes/{id}`            | Remove um cliente                           |
| POST   | `/produtos`                 | Cria um produto                             |
| GET    | `/produtos`                 | Lista produtos                              |
| GET    | `/produtos/{id}`            | Obtém um produto                            |
| PUT    | `/produtos/{id}`            | Atualiza um produto                         |
| DELETE | `/produtos/{id}`            | Remove um produto                           |
| POST   | `/pedidos`                  | Cria um pedido (com itens)                  |
| GET    | `/pedidos`                  | Lista pedidos                               |
| GET    | `/pedidos/{id}`             | Obtém um pedido                             |
| PATCH  | `/pedidos/{id}/status`      | Atualiza o status do pedido                 |
| DELETE | `/pedidos/{id}`             | Remove um pedido                            |
| GET    | `/health`                   | Verifica se a API está no ar                |

Consulte `/docs` para exemplos completos de payloads e respostas.

## Exemplo de uso

```bash
# Criar cliente
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria Silva", "email": "maria@email.com", "telefone": "11999999999"}'

# Criar produto
curl -X POST http://localhost:8000/produtos \
  -H "Content-Type: application/json" \
  -d '{"nome": "Teclado", "descricao": "Teclado mecânico", "preco": 250.00, "estoque": 10}'

# Criar pedido (substitua os IDs pelos retornados acima)
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente_id": "<ID_CLIENTE>", "itens": [{"produto_id": "<ID_PRODUTO>", "quantidade": 2}]}'
```

## Versão entregue

A versão avaliada deste projeto está identificada pela tag `APIPedidos-1-final`.
