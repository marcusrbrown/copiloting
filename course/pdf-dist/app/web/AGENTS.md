# course/pdf-dist/app/web/AGENTS.md

## OVERVIEW

Flask web layer — app factory, routes (blueprints), DB models (SQLAlchemy), auth hooks, and API helper functions used by both views and chat layer.

## STRUCTURE

```
web/
├── __init__.py       # App factory: create_app(), registers extensions/blueprints/hooks
├── api.py            # DB helper functions (messages, conversations) used by chat layer
├── hooks.py          # before_request: load_logged_in_user; error handler
├── config/           # Config object loaded from env vars
│   └── __init__.py
├── db/
│   ├── __init__.py   # SQLAlchemy db object + init_db_command CLI
│   └── models/
│       ├── base.py      # BaseModel with shared CRUD helpers
│       ├── user.py      # User (UUID PK, email, password, relationships)
│       ├── pdf.py       # Pdf (linked to user, tracks embedding status)
│       ├── conversation.py  # Conversation (stores llm/memory/retriever component names)
│       ├── message.py   # Message (role, content, linked to conversation)
│       └── __init__.py  # Re-exports all models
├── files.py          # File upload helpers (PDF validation, save to disk)
├── views/
│   ├── auth_views.py          # /auth/signin, /signup, /signout
│   ├── pdf_views.py           # /api/pdfs — upload, list, get
│   ├── conversation_views.py  # /api/conversations — CRUD + messaging
│   ├── score_views.py         # /api/scores — A/B test component scoring
│   └── client_views.py        # Catch-all: serves SvelteKit build for all non-API routes
└── tasks/
    └── embeddings.py  # Celery task: process PDF → create embeddings → store in Pinecone
```

## WHERE TO LOOK

| Task                     | Location                                                                                                       |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Add a new Flask route    | `views/` — create blueprint function, register in `__init__.py`                                                |
| DB models                | `db/models/` — each model has `create()`, `find_by()`, `update()` from BaseModel                               |
| Auth (current user)      | `hooks.py` — `load_logged_in_user` sets `g.user`                                                               |
| Config / env vars        | `config/__init__.py`                                                                                           |
| PDF upload handling      | `files.py` + `views/pdf_views.py`                                                                              |
| Background embedding job | `tasks/embeddings.py` (dispatched via Celery)                                                                  |
| API helpers for chat     | `api.py` — `get_messages_by_conversation_id`, `add_message_to_conversation`, `get/set_conversation_components` |

## CONVENTIONS

- All models extend `BaseModel` — shared `create()`, `find_by()`, `update()`, `delete()` methods
- `db.session` used directly in `api.py` — no repository pattern
- Flask blueprints registered in `register_blueprints()` in `__init__.py`
- `client_views.py` is the SPA fallback — returns `client/build/index.html` for unmatched routes
- `g.user` populated by `load_logged_in_user` before every request

## ANTI-PATTERNS

- Do not call LangChain from views — all LLM work goes through `app.chat`
- Do not bypass `BaseModel` for DB ops — use `Model.create()`, `.find_by()`, `.update()`
- Do not import from `app.web.db.models` submodules directly — use the re-export in `models/__init__.py`

## NOTES

- `flask --app app.web init-db` drops + recreates all tables (destructive)
- `Conversation` model stores `llm`, `memory`, `retriever` string names — used for A/B component selection
