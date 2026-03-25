# Copilot Instructions

Read `AGENTS.md` at the repository root first — it has the full project map, structure, conventions, commands, and anti-patterns. Everything below supplements it.

## Verification (run before every commit)

```bash
pnpm lint            # ESLint + Prettier — must pass
pnpm build           # all workspaces — must pass
poetry install       # Python deps — must pass
```

If you change Python dependency versions in any `pyproject.toml`, also run `poetry lock` to regenerate the lock file.

## Hard rules

### TypeScript

- `@bfra.me/tsconfig` (strict) is active — no `any`, no `@ts-ignore`, no `@ts-expect-error`
- ESM only: use `.js` extensions in all import paths (`import {foo} from './bar.js'`)
- Module system is `nodenext` — no CommonJS, no `require()`

### Python

- Python `^3.14` via Poetry — each subdirectory has its own `pyproject.toml`
- Application code imports are **stale** — deps were upgraded to pydantic v2, openai v1, langchain 0.3, chromadb 1.x but the code still uses old APIs. Check actual import paths against current package versions before writing new code.

### Package managers

- **pnpm 10 only** for JS/TS — never use npm or yarn
- **Poetry only** for Python — never use pip directly
- pnpm settings live in `pnpm-workspace.yaml`, not `.npmrc`

### Formatting & linting

- `@bfra.me/eslint-config` handles both ESLint rules and Prettier formatting
- Run `pnpm fix` to auto-fix lint + format issues before committing
- Prettier rules: `semi: false`, `singleQuote: true`, `bracketSpacing: false`, `printWidth: 100`
- `.svelte` files use the `svelte` parser (configured in `prettier.config.js`)

### Security

- **Never** commit API keys, tokens, or credentials
- `.env` files are gitignored — use `.env.template` as reference
- Pin GitHub Actions by full SHA hash, not version tag

## Tool versions

All tool versions are managed by `mise.toml` — do not install Python, Node, pnpm, or Poetry through other means. Run `mise install` to get the correct versions.

## What CI checks

| Job           | Checks                                                    |
| ------------- | --------------------------------------------------------- |
| Build Node.js | `pnpm install` → `pnpm lint` → `pnpm build` → `pnpm test` |
| Build Python  | `poetry install` → `poetry run pytest`                    |
