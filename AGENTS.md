# AGENTS.md

**Generated:** 2026-03-23 | **Commit:** 89328ad | **Branch:** main

## OVERVIEW

Polyglot AI/LLM experimentation monorepo — LangChain-based copilot experiments. Contains a production-ish Flask + SvelteKit PDF chat app (`course/pdf-dist`) and standalone Python/TypeScript tutorial scripts. Course/exploration code, not a shipped product.

**Stack:** Python 3.11.7 (Poetry) · TypeScript 5.3 (pnpm) · Flask · SvelteKit · LangChain (old 0.0.x) · OpenAI · Pinecone · Redis · Celery · SQLAlchemy

## STRUCTURE

```
copiloting/
├── tutorials/           # TS LangChain tutorial scripts (pnpm workspace)
├── course/
│   ├── sections/        # Python AI modules: agents, chains, facts, tchat (Poetry pkg)
│   ├── pdf-dist/        # Flask PDF chat app + SvelteKit frontend (standalone)
│   │   ├── app/         # Python backend
│   │   │   ├── chat/    # LLM chains, retrievers, memory, embeddings, tracing
│   │   │   └── web/     # Flask views, DB models, API helpers
│   │   └── client/      # SvelteKit frontend (pnpm workspace)
│   └── local-do/        # Minimal Flask PDF upload server
├── copiloting/          # Empty Python stub (ignore)
├── package.json         # Root pnpm workspace + Prettier scripts
├── pyproject.toml       # Root Poetry config — defines CLI entry points
├── pnpm-workspace.yaml  # JS workspaces: tutorials, course/pdf-dist/client
└── tsconfig.json        # Extends @tsconfig/strictest, ES2022, nodenext
```

## WHERE TO LOOK

| Task                    | Location                                                   |
| ----------------------- | ---------------------------------------------------------- |
| LangChain TS tutorial   | `tutorials/quickstart-llms.ts`                             |
| Flask app factory       | `course/pdf-dist/app/web/__init__.py`                      |
| LLM chat orchestration  | `course/pdf-dist/app/chat/chat.py`                         |
| SvelteKit routes/pages  | `course/pdf-dist/client/src/routes/`                       |
| Svelte components       | `course/pdf-dist/client/src/components/`                   |
| Svelte state management | `course/pdf-dist/client/src/store/`                        |
| Axios API client        | `course/pdf-dist/client/src/api/axios.ts`                  |
| Python AI section demos | `course/sections/` (agents, chain, facts, tchat)           |
| Flask DB models         | `course/pdf-dist/app/web/db/models/`                       |
| Celery worker           | `course/pdf-dist/app/celery/worker.py`                     |
| Env vars                | `.env.template` (safe) / `.env` (real keys — do not share) |
| CI pipeline             | `.github/workflows/ci.yaml`                                |

## CONVENTIONS

- **TypeScript**: Extends `@tsconfig/strictest` — maximum strictness; no `any`, no suppression
- **Module format**: `"module": "nodenext"` — requires `.js` extensions in TS imports
- **Prettier**: `singleQuote: true`, `bracketSpacing: false`, `tabWidth: 2`; `.svelte` files use svelte parser
- **Python**: pinned to `3.11.7`, managed by Poetry; each subdirectory is an independent Poetry project
- **Package manager**: pnpm `≥7` only for JS/TS — never npm or yarn in this repo
- **Line endings**: LF, enforced by EditorConfig across all files
- **SvelteKit path aliases**: `$c` → `src/components`, `$s` → `src/store`, `$api` → `src/api/axios.js`

## ANTI-PATTERNS

- **`.env` contains real committed secrets** — never copy or commit actual API keys
- **LangChain versions are ancient**: JS at `0.0.212`, Python at `0.0.352` — modern LangChain docs don't apply; imports and APIs are completely different
- **No tests** — `pnpm test` intentionally exits with error; no pytest setup exists
- **`copiloting/__init__.py`** is an empty stub — not a real importable package

## COMMANDS

```bash
# From repo root — JS/TS
pnpm install --frozen-lockfile       # install all workspaces
pnpm build                           # build all workspaces recursively
pnpm check-format                    # Prettier format check (runs in CI)
pnpm format                          # Prettier auto-fix

# Run TypeScript tutorial (requires SERPAPI_API_KEY + OPENAI_API_KEY in .env)
pnpm -C tutorials run start:quickstart-llms

# SvelteKit dev server
pnpm -C course/pdf-dist/client run dev

# From repo root — Python
poetry install                       # install all Python deps
poetry run agents                    # SQL agent demo (course/sections/agents)
poetry run course                    # LangChain chain demo (course/sections/chain)
poetry run facts                     # facts RAG demo (course/sections/facts)
poetry run facts-create-embeddings   # create Chroma embeddings
poetry run tchat                     # terminal chat demo
```

## NOTES

- Renovate auto-updates deps; CI action pins use full SHA hashes (security practice)
- CI runs format check + build for Node, `poetry install` only for Python (no lint/test)
- `poetry.lock` (388KB) covers all Poetry groups including `pdf-dist` and `sections` path deps
- Both `pnpm` and `poetry` run independently — no cross-language tooling bridge
- `course/pdf-dist` has its own `dump.rdb` and `instance/sqlite.db` — local dev state artifacts
