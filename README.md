<div align="center">
  <h1>
    <img src="./assets/ralts.png" width="60" height="60" alt="Ralts Logo" style="vertical-align: middle; margin-right: 10px;">
    Ralts
  </h1>

  <p>API simples para coleta e armazenamento de produtos (FastAPI + SQLAlchemy + Scrapy).</p>
</div>


## Visão geral
- FastAPI app em `app/`
- Scrapy project em `scrapy/scrapy_datahunt/`
- Banco: por padrão SQLite, configurável via `DATABASE_URL` (suporta Postgres async via `asyncpg`)
- Docker + docker-compose para orquestração (serve Postgres + app)

## Requisitos
- Python 3.9+
- docker & docker-compose (opcional para execução em contêiner)
- (local) criar virtualenv e instalar dependências:
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt

## Executando localmente (desenvolvimento)
1. Instale dependências (veja acima).
2. Rodar com uvicorn:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Acesse:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - OpenAPI JSON: http://localhost:8000/openapi.json

## Executando com Docker Compose
1. Copie `.env.example` para `.env` e ajuste se necessário.
2. Subir services:
   ```bash
   make up
   ```
   ou
   ```bash
   docker-compose up --build
   ```
3. Parar:
   ```bash
   make down
   ```

Observação: por padrão o `docker-compose.yml` tenta iniciar um serviço Postgres e injeta `DATABASE_URL`. Para usar SQLite, sobrescreva `DATABASE_URL` no `.env` com `sqlite+aiosqlite:///./ralts.db`.

## Makefile úteis
- `make build` — build das imagens
- `make up` — sobe os serviços em background
- `make down` — derruba serviços
- `make logs` — acompanha logs
- `make test` — roda testes (usa container app)
- `make shell` — shell no container app

## Endpoints principais

- GET /healthcheck
  - Descrição: verifica se a API está viva.
  - Exemplo:
    ```bash
    curl http://localhost:8000/healthcheck
    ```
  - Resposta:
    ```json
    { "status": "ok" }
    ```

- POST /products
  - Descrição: cria um produto.
  - Exemplo:
    ```bash
    curl -X POST http://localhost:8000/products \
      -H "Content-Type: application/json" \
      -d '{"name": "Celular X", "price": 999.9}'
    ```
  - Resposta:
    ```json
    {
      "id": 1,
      "name": "Celular X",
      "price": 999.9,
      "created_at": "2025-10-31T12:00:00"
    }
    ```

- GET /products
  - Descrição: lista todos os produtos.
  - Exemplo:
    ```bash
    curl http://localhost:8000/products
    ```
  - Resposta (array):
    ```json
    [
      {"id":1,"name":"Celular X","price":999.9,"created_at":"2025-10-31T12:00:00"},
      {"id":2,"name":"Fone Y","price":199.0,"created_at":"2025-10-31T12:10:00"}
    ]
    ```

- GET /products/{id}
  - Descrição: obtém produto por id.
  - Exemplo:
    ```bash
    curl http://localhost:8000/products/1
    ```

- GET /products/stats?top=5
  - Descrição: estatísticas (média de preços, top N mais caros/baratos, contagem por source).
  - Exemplo:
    ```bash
    curl http://localhost:8000/products/stats?top=3
    ```
  - Resposta (exemplo):
    ```json
    {
      "average_price": 550.3,
      "most_expensive":[{"id":4,"name":"High-End","price":2500.0}],
      "cheapest":[{"id":3,"name":"Budget","price":49.9}],
      "count_by_source":{"mercadolivre":10,"unknown":2}
    }
    ```

- POST /scrape/start
  - Descrição: inicia o scraper (executa spider em processo separado).
  - Exemplo:
    ```bash
    curl -X POST http://localhost:8000/scrape/start
    ```
  - Resposta:
    ```json
    {"status":"started","pid":12345,"spider":"product_spider","started":true}
    ```

## Swagger / OpenAPI
O FastAPI expõe automaticamente a documentação interativa:
- Swagger UI (interface): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

Se desejar exportar o OpenAPI em YAML/JSON, use o endpoint `/openapi.json` e converta conforme necessário.

## Testes
- Local:
  ```bash
  python -m pytest -q
  ```
- Via Docker (Makefile):
  ```bash
  make test
  ```

## Observações finais
- Ajuste `DATABASE_URL` via `.env` para usar Postgres/SQLite conforme necessário.
- O Scrapy pipeline salva itens diretamente no banco (ver `scrapy_datahunt/pipelines.py`).
- Para depuração rápida use `make shell` e rode comandos dentro do container app.

## Futuras implementações (alto volume)

Para cenários de alto volume de dados (coletas e ingestão em larga escala) pretendo evoluir a arquitetura com:

- Fila de tarefas:
  - Redis como broker rápido em memória para enfileirar jobs de scraping e processamento.
  - Celery (workers) para executar tarefas assíncronas e escaláveis (vários workers por nó).

- Padrões e práticas:
  - Batch inserts: acumular itens em lotes e inserir no banco em operações atômicas para reduzir overhead.
  - Idempotência e deduplicação: garantir que reprocessamentos não criem duplicatas (hashes/UUIDs).
  - Retry/backoff: políticas de retentativa para falhas transientes com limites e dead-letter queues.
  - Rate limiting / backpressure: controlar taxa de requests para evitar bloqueios dos sites alvo.

- Escalabilidade e infraestrutura:
  - Separar componentes: scrapers (collectors) → fila → workers de processamento → banco.
  - Usar Redis Streams se precisar de retenção/consumo múltiplo e processamento reordenável.

- Observabilidade e operações:
  - Monitoramento: Prometheus + Grafana para métricas (throughput, latência, falhas).
  - Tracing/Logs: OpenTelemetry / ELK para rastrear jobs e depurar falhas.
  - Healthchecks, readiness/liveness para orquestração (K8s).

Implementar essa camada assíncrona para isolar a coleta do processamento e aumentar a resiliência/throughput sem sobrecarregar a API principal.
