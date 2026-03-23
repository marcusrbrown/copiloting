# PDF Dist

Standalone Flask + SvelteKit PDF chat application.

## First-Time Setup

The default Python setup for this app comes from the repo root.

From the repo root:

```sh
mise install
poetry env use 3.11
poetry install
poetry run flask --app app.web init-db
pnpm -C course/pdf-dist/client install --frozen-lockfile
```

## Running the App

There are three backend processes plus the SvelteKit frontend during development.

Use the repo-root `.venv`. Do not run `poetry install` inside `course/pdf-dist/`.

### Python server

From the repo root:

```sh
source .venv/bin/activate
cd course/pdf-dist
inv dev
```

### Worker

From the repo root:

```sh
source .venv/bin/activate
cd course/pdf-dist
inv devworker
```

### Redis

```sh
redis-server
```

### Frontend

From the repo root:

```sh
pnpm -C course/pdf-dist/client run dev
```

### Reset the database

From the repo root:

```sh
poetry run flask --app app.web init-db
```

## Notes

- Flask serves built static assets from `client/build/`
- The root Poetry environment is the boring default for this app and `course/sections`
- The repo root `poetry.toml` keeps the virtualenv in `./.venv`
- `instance/sqlite.db` and `dump.rdb` are local state artifacts
