# Copiloting

Polyglot AI/LLM experimentation monorepo with:

- TypeScript LangChain tutorials in `tutorials/`
- Python LangChain demos in `course/sections/`
- A Flask + SvelteKit PDF chat app in `course/pdf-dist/`

## Prerequisites

- [mise](https://mise.jdx.dev/) for local tool versions

`mise.toml` installs and pins the repo's Python, Poetry, pnpm, and Node versions.

## Local Setup

Open the repo root in VS Code. The default Python workflow is repo-root based.

```bash
# Install pinned tool versions from mise.toml
mise install

# Create/use the repo Python 3.11 environment
poetry env use 3.11

# Install Python dependencies for the root project plus editable path deps
poetry install

# Install JS workspace dependencies
pnpm install --frozen-lockfile
```

## VS Code

- Open the repository root, not a nested Python directory
- Install the recommended extensions (`ms-python.python`, `ms-python.vscode-pylance`)
- VS Code is configured to use the repo `.venv`
- Pylance is configured to resolve `course/pdf-dist` imports like `from app.web import ...`

If VS Code does not pick up the interpreter automatically, select `.venv` from the Python interpreter picker.

## Python Commands

```bash
# Root Poetry scripts
poetry run agents
poetry run course
poetry run facts
poetry run facts-create-embeddings
poetry run tchat

# Flask DB init for the PDF app
poetry run flask --app app.web init-db
```

## JavaScript Commands

```bash
pnpm build
pnpm check-format
pnpm -C tutorials run start:quickstart-llms
pnpm -C course/pdf-dist/client run dev
```

## Notes

- Root Poetry setup covers the main Python work in `course/sections` and `course/pdf-dist`
- `poetry.toml` pins Poetry to an in-project virtualenv at `./.venv`
- `course/local-do` is a separate optional Poetry project with its own setup
- This repo pins Python `3.11.7`; your system `python3` version does not matter if `mise` and Poetry are used correctly
