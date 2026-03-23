# course/pdf-dist/AGENTS.md

## OVERVIEW

Standalone Flask + SvelteKit PDF chat application. Users upload PDFs, which get embedded into Pinecone; conversations are LangChain RAG chains with configurable LLM/memory/retriever per-conversation. Background processing via Celery + Redis.

**Stack:** Flask · SQLAlchemy (SQLite) · Celery · Redis · Pinecone · LangFuse · SvelteKit (built static)

## STRUCTURE

```
pdf-dist/
├── app/             # Python Flask backend (Poetry package)
│   ├── chat/        # LLM orchestration: chains, memory, vectorstores, embeddings
│   └── web/         # Flask app factory, routes, DB models, API helpers
├── client/          # SvelteKit frontend (pnpm workspace, builds to client/build/)
├── tasks.py         # Invoke task definitions (dev, devworker commands)
├── pyproject.toml   # Standalone Poetry project
├── dump.rdb         # Redis snapshot (local dev artifact)
└── instance/        # SQLite DB lives here (local dev artifact)
    └── sqlite.db
```

## WHERE TO LOOK

| Task                   | Location                                                               |
| ---------------------- | ---------------------------------------------------------------------- |
| Flask app factory      | `app/web/__init__.py` — `create_app()`                                 |
| LLM chat entry point   | `app/chat/chat.py` — `build_chat()`                                    |
| PDF embedding pipeline | `app/chat/create_embeddings.py`, `app/web/tasks/embeddings.py`         |
| Celery worker          | `app/celery/worker.py`                                                 |
| DB init command        | `flask --app app.web init-db` (registered in `app/web/db/__init__.py`) |
| Dev run tasks          | `tasks.py` — `inv dev`, `inv devworker`                                |

## CONVENTIONS

- Flask static files served from `client/build/` — SvelteKit adapter-static output
- Celery only initialized if `Config.CELERY["broker_url"]` is set
- All DB models inherit from `app.web.db.models.base.BaseModel`
- Conversation components (LLM name, retriever name, memory name) stored in `Conversation` model and selected via weighted random scoring (`app/chat/score.py`)

## ANTI-PATTERNS

- Do not use `pip install` — this is a Poetry project (`poetry install` from repo root)
- Flask app uses `langchain==0.0.x` — modern langchain chain APIs don't apply here
- `instance/sqlite.db` and `dump.rdb` are local dev artifacts — not production state

## COMMANDS

```bash
# DB setup (first time)
flask --app app.web init-db

# Dev (three separate terminals)
inv dev           # Flask server
inv devworker     # Celery worker
redis-server      # Redis

# SvelteKit frontend
pnpm -C course/pdf-dist/client run dev    # from repo root
pnpm -C course/pdf-dist/client run build  # build static assets to client/build/
```

## NOTES

- `client/build/` is served as Flask static folder — run `pnpm build` in client before deploying
- LangFuse tracing is optional — only activated if `LANGFUSE_PUBLIC_KEY`/`SECRET_KEY` are set
- Conversation component selection uses weighted scoring to A/B test different LLM/retriever combos
