# Intelligent News Monitoring & Analysis System — v0.3

Production-oriented MVP for domain-based media intelligence.

## What's new in v0.3

- LangGraph pipeline with **parallel Topic + Impact analysis** after story clustering.
- Deterministic semantic pre-filter plus embeddings.
- PostgreSQL + pgvector storage with an HNSW cosine index.
- Source reliability scoring.
- User-configurable rule engine: minimum priority, required/excluded topics, source allow/deny lists and alert toggle.
- Redis-backed ingestion queue and dedicated worker.
- Agent-run audit records with latency/status.
- Alert persistence.
- Refined Next.js intelligence dashboard.
- Mock embeddings + mock structured LLM mode for local development without API keys.

## Architecture

```text
RSS / APIs / Web
       ↓
Collector + Cleaning
       ↓
Embedding + semantic pre-filter
       ↓
Context Validation
       ↓
Story Clustering
       ↓
 ┌────────────┬─────────────┐
 ↓            ↓             ↓
Topics      Impact       (future agents)
 └────────────┴─────────────┘
       ↓
Importance + reliability
       ↓
Summary
       ↓
Rule & Priority Engine
       ↓
PostgreSQL + pgvector
       ↓
Dashboard / Alerts
```

## Run

```bash
cd backend
cp .env.example .env
cd ..
docker compose up --build
```

API: http://localhost:8000/docs

Then run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Dashboard: http://localhost:3000

For a no-key demo, keep `MOCK_LLM=true`. The embedding fallback is deterministic, so the full pipeline can be exercised locally.

## Real model mode

Set `MOCK_LLM=false` and provide `OPENAI_API_KEY`. The LLM provider is isolated in `backend/app/agents/llm.py`. Embeddings are isolated in `backend/app/services/embeddings.py`.

## API

- `POST /api/pipeline/run` — process supplied articles immediately.
- `POST /api/rss/run` — fetch RSS feeds and process immediately.
- `POST /api/jobs/rss` — enqueue RSS ingestion for the Redis worker.
- `GET /health` — service health.

## Next production upgrades

1. Add Alembic migrations instead of `create_all`.
2. Add authentication and tenant/user IDs to every persisted object.
3. Add scheduled feed configurations and cron jobs in the worker.
4. Add source-specific connectors for YouTube, publisher pages and approved social APIs.
5. Add email/Slack/Teams delivery workers and delivery retries.
6. Add evaluation datasets, prompt/version tracking and tracing.
7. Add rate limiting, secret management and production observability.

---

# 👥 5-Member Agent Development

This repository is now organized for a five-member beginner-friendly team. **Read `team/TEAM_TASKS.md` first.** It contains the exact assignment, input/output contract, implementation steps, Git branch and definition of done for each member.

## Five branches

```text
feature/agent-discovery
feature/agent-validation
feature/agent-clustering
feature/agent-importance
feature/agent-summary
```

These are **Git branches**, not five separate copies of the project.

| Member | Branch | Owns |
|---|---|---|
| 1 | `feature/agent-discovery` | Semantic Discovery Agent |
| 2 | `feature/agent-validation` | Context Validation Agent |
| 3 | `feature/agent-clustering` | Story Clustering Agent |
| 4 | `feature/agent-importance` | Importance Analysis Agent |
| 5 | `feature/agent-summary` | Summary Agent |

### Beginner starting point

1. Read `docs/agent-development-guide.md`.
2. Open your member folder under `team/`.
3. Read your section in `team/TEAM_TASKS.md`.
4. Checkout your Git branch.
5. Keep `MOCK_LLM=true` while learning.
6. Run `pytest -q` before and after changes.
7. Commit and push only your assigned work.
8. Open a Pull Request; do not merge directly into `main`.

### Shared contract

All five agents communicate through `backend/app/graph/state.py` and the Pydantic models in `backend/app/schemas/news.py`. The integration owner controls those shared contracts and `backend/app/graph/workflow.py`.

### Agent files

```text
backend/app/agents/
├── discovery.py      # Member 1
├── validation.py     # Member 2
├── clustering.py     # Member 3
├── importance.py     # Member 4
└── summary.py        # Member 5
```

See `docs/architecture.md` for the full pipeline.
