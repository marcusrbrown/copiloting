# tutorials/AGENTS.md

## OVERVIEW

TypeScript LangChain tutorial — single script demonstrating LLM agent with web search + calculator. pnpm workspace package.

## STRUCTURE

```
tutorials/
├── quickstart-llms.ts   # Only tutorial: OpenAI LLM + SerpAPI + Calculator agent
├── tsconfig.json        # Extends root tsconfig (ES2022, nodenext, strictest)
├── package.json         # @copiloting/tutorials — build: rimraf + tsc
└── dist/                # Compiled output (generated, don't edit)
```

## WHERE TO LOOK

| Task        | Location                                                    |
| ----------- | ----------------------------------------------------------- |
| Agent setup | `quickstart-llms.ts` — `initializeAgentExecutorWithOptions` |
| Tool config | `quickstart-llms.ts` — SerpAPI + Calculator instantiation   |
| Run script  | `package.json` → `start:quickstart-llms`                    |

## CONVENTIONS

- Imports use `.js` extensions on runtime paths (nodenext module resolution)
- langchain version pinned at `0.0.212` at root — do **not** use modern langchain APIs
- `dotenv` loaded via `node -r dotenv/config` at runtime, not imported in code
- Top-level `await` works because `"type": "module"` in package.json

## ANTI-PATTERNS

- Do not upgrade langchain imports without checking root `package.json` — old API
- Do not add `import 'dotenv/config'` — injected at runtime via node flag

## COMMANDS

```bash
# From repo root
pnpm -C tutorials run start:quickstart-llms    # build + run tutorial

# From tutorials/
pnpm run build                                  # compile TS → dist/
```

## NOTES

- Requires `SERPAPI_API_KEY` + `OPENAI_API_KEY` in root `.env`
- Only one tutorial script exists — codebase is exploratory, not a library
