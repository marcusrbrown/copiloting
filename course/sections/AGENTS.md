# course/sections/AGENTS.md

## OVERVIEW

Python AI section demo modules — four standalone LangChain demos exposed as Poetry CLI scripts. Each submodule is a self-contained experiment.

## STRUCTURE

```
sections/
├── agents/          # SQL agent — queries SQLite via LangChain OpenAIFunctionsAgent
│   ├── __init__.py  # Entry point: builds agent + executor, runs two example queries
│   ├── tools/       # Custom tools: sql.py (describe/query), report.py (write HTML)
│   └── handlers/    # ChatModelStartHandler — logs LLM calls to console
├── chain/           # SequentialChain demo: code generation → test generation
│   └── __init__.py  # CLI with --task and --language args
├── facts/           # RAG demo with Chroma vector store
│   ├── __init__.py  # Entry: loads embeddings, runs retrieval QA chain
│   ├── facts.txt    # Source document for RAG
│   ├── redundant_filter_retriever.py  # Custom retriever deduplicating results
│   ├── scores.ipynb # Jupyter notebook for scoring experiments
│   └── .embeddings/ # Persisted Chroma DB (local dev artifact)
├── tchat/           # Terminal chat loop
│   └── __init__.py  # Interactive REPL using LangChain chat model
└── utilities/       # Shared helpers
    └── __init__.py
```

## WHERE TO LOOK

| Task                    | Location                                                    |
| ----------------------- | ----------------------------------------------------------- |
| SQL agent with tools    | `agents/__init__.py` + `agents/tools/`                      |
| SequentialChain example | `chain/__init__.py`                                         |
| RAG with Chroma         | `facts/__init__.py` + `facts/redundant_filter_retriever.py` |
| Custom LLM callback     | `agents/handlers/chat_model_start_handler.py`               |
| Shared utilities        | `utilities/__init__.py`                                     |

## CONVENTIONS

- All modules use `langchain==0.0.352` (Python) — not compatible with modern langchain 0.1+/0.3+ APIs
- `load_dotenv()` called at module init — reads from root `.env`
- Each module is runnable via `poetry run <script>` from repo root (defined in root `pyproject.toml`)
- SQLite DB for agents demo: `agents/db.sqlite`

## ANTI-PATTERNS

- Do not use modern langchain imports (`from langchain_openai import ...`) — only `langchain.llms.openai`, `langchain.chat_models`, etc. work at `0.0.352`
- Do not add new Poetry scripts here — they're declared in root `pyproject.toml`, not this `pyproject.toml`

## COMMANDS

```bash
# From repo root
poetry run agents                  # SQL agent demo
poetry run course                  # LangChain chain demo
poetry run facts                   # facts RAG demo (needs embeddings first)
poetry run facts-create-embeddings # create Chroma embeddings into facts/.embeddings/
poetry run tchat                   # terminal chat
```

## NOTES

- `facts/.embeddings/` contains persisted Chroma SQLite — delete to force rebuild
- `agents/db.sqlite` is a pre-populated local SQLite DB for the SQL agent demo
