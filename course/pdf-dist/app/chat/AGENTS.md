# course/pdf-dist/app/chat/AGENTS.md

## OVERVIEW

LLM orchestration layer — builds RAG chains with pluggable LLM, memory, and retriever strategies. All LangChain interaction lives here; Flask layer never touches LangChain directly.

## STRUCTURE

```
chat/
├── chat.py              # Entry: build_chat() — selects + wires components
├── chains/
│   ├── retrieval.py     # RetrievalChain: TraceableChain + StreamableChain + ConversationalRetrievalChain
│   ├── streamable.py    # Mixin: SSE streaming support
│   └── traceable.py     # Mixin: LangFuse tracing support
├── memory/
│   ├── sql_memory.py    # Conversation memory backed by SQLAlchemy
│   ├── window_memory.py # Sliding window memory
│   └── history/
│       └── sql_history.py  # Message history adapter for SQL storage
├── vectorstores/
│   └── pinecone.py      # Pinecone retriever builder
├── embeddings/
│   └── openai.py        # OpenAI embeddings builder
├── llms/
│   └── chat_openai.py   # ChatOpenAI LLM builder (returns map entry)
├── callbacks/
│   └── stream.py        # Streaming callback handler for SSE
├── tracing/
│   └── langfuse.py      # LangFuse callback + handler setup
├── redis.py             # Redis client (used for rate-limiting / caching)
├── score.py             # Weighted random component selection by A/B score
├── models/__init__.py   # ChatArgs dataclass
└── create_embeddings.py # PDF → embeddings → Pinecone upload pipeline
```

## WHERE TO LOOK

| Task                    | Location                                            |
| ----------------------- | --------------------------------------------------- |
| Chat chain construction | `chat.py` → `build_chat()`                          |
| Chain class definition  | `chains/retrieval.py` — `RetrievalChain`            |
| Add streaming support   | `chains/streamable.py`                              |
| Add LangFuse tracing    | `chains/traceable.py` + `tracing/langfuse.py`       |
| Add new LLM option      | `llms/chat_openai.py` — add to `llm_map`            |
| Add new memory type     | `memory/` — add builder to `memory_map`             |
| Add new retriever       | `vectorstores/pinecone.py` — add to `retriever_map` |
| ChatArgs input shape    | `models/__init__.py`                                |
| A/B scoring logic       | `score.py`                                          |
| PDF embedding pipeline  | `create_embeddings.py`                              |

## CONVENTIONS

- `llm_map`, `memory_map`, `retriever_map` — dicts mapping component name → builder function; `select_component()` picks from these using weighted scoring
- Component names are stored in the `Conversation` DB record; reused on subsequent messages to same conversation
- `ChatArgs` carries `conversation_id`, `pdf_id`, `metadata`, `streaming: bool`
- `TraceableChain` + `StreamableChain` applied as mixins before `ConversationalRetrievalChain` in MRO
- langchain 0.0.352 Python — use `from langchain.chat_models import ChatOpenAI`, NOT `from langchain_openai import ...`

## ANTI-PATTERNS

- Do not import from `langchain_openai`, `langchain_community`, etc. — those packages don't exist at `0.0.352`
- Do not bypass `build_chat()` — component selection + persistence must go through it
- Do not call DB layer directly from chat — use `app.web.api` functions

## NOTES

- `ChatOpenAI(streaming=False)` is used for the condense-question step even when streaming is enabled
- LangFuse tracing is opt-in via env var presence
