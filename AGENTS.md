# AGENTS.md

**Generated:** 2026-03-25 | **Commit:** 7af32e0 | **Branch:** main

## OVERVIEW

Polyglot AI/LLM experimentation monorepo — LangChain-based copilot experiments. Contains a production-ish Flask + SvelteKit PDF chat app (`course/pdf-dist`) and standalone Python/TypeScript tutorial scripts. Course/exploration code, not a shipped product.

**Stack:** Python 3.14 (Poetry) · TypeScript 5.3 (pnpm 10) · Flask · SvelteKit · LangChain 0.3 · OpenAI v1 · Pinecone · Redis · Celery · SQLAlchemy

**Tooling:** mise (tool version manager) · Renovate (automated dependency updates)

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
├── pnpm-workspace.yaml  # JS workspaces + pnpm settings (replaces .npmrc)
├── mise.toml            # Tool versions: python, node, pnpm, poetry
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
| Tool versions           | `mise.toml`                                                |
| Renovate config         | `.github/renovate.json5`                                   |

## CONVENTIONS

- **Tool management**: mise manages all tool versions (Python, Node, pnpm, Poetry) — see `mise.toml`
- **TypeScript**: Extends `@tsconfig/strictest` — maximum strictness; no `any`, no suppression
- **Module format**: `"module": "nodenext"` — requires `.js` extensions in TS imports
- **Prettier**: `singleQuote: true`, `bracketSpacing: false`, `tabWidth: 2`; `.svelte` files use svelte parser
- **Python**: `^3.14`, managed by Poetry; each subdirectory is an independent Poetry project
- **Package manager**: pnpm 10 only for JS/TS — never npm or yarn in this repo
- **pnpm settings**: Configured in `pnpm-workspace.yaml` (not `.npmrc`)
- **Line endings**: LF, enforced by EditorConfig across all files
- **SvelteKit path aliases**: `$c` → `src/components`, `$s` → `src/store`, `$api` → `src/api/axios.js`
- **GitHub Actions**: Pin actions by full SHA hash (security practice); Renovate updates them

## ANTI-PATTERNS

- **`.env` contains real committed secrets** — never copy or commit actual API keys
- **No tests** — `pnpm test` intentionally exits with error; no pytest setup exists
- **`copiloting/__init__.py`** is an empty stub — not a real importable package
- **Python code imports are stale** — deps were recently upgraded (pydantic v2, openai v1, langchain 0.3, chromadb 1.x) but application code has not been updated to match new APIs

## COMMANDS

```bash
# From repo root — JS/TS
pnpm install --frozen-lockfile       # install all workspaces
pnpm build                           # build all workspaces recursively
pnpm check-format                    # Prettier format check (runs in CI)
pnpm format                          # Prettier auto-fix

# From repo root — Python
poetry install                       # install all Python deps
poetry lock                          # regenerate lock file

# Verification (run before committing)
pnpm check-format                    # must pass
pnpm build                           # must pass
poetry install                       # must pass
```

## NOTES

- Renovate auto-updates deps; CI action pins use full SHA hashes (security practice)
- Renovate `postUpgradeTasks` runs `poetry lock` for Python dep updates (scoped to poetry manager)
- CI runs format check + build for Node, `poetry install` only for Python (no lint/test)
- `poetry.lock` covers all Poetry groups including `pdf-dist` and `sections` path deps
- Both `pnpm` and `poetry` run independently — no cross-language tooling bridge
- `course/pdf-dist` has its own `dump.rdb` and `instance/sqlite.db` — local dev state artifacts
