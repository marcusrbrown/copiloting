# course/local-do/AGENTS.md

## OVERVIEW

Minimal standalone Flask server for PDF upload only. No LLM integration — just a file receiver with UUID-named storage. Independent Poetry project.

## STRUCTURE

```
local-do/
├── app.py          # Flask app: single upload endpoint, saves to uploads/
├── uploads/        # Uploaded PDFs stored with UUID filenames (gitkeep + real files)
├── dump.rdb        # Redis dump (local dev artifact — ignore)
├── pyproject.toml  # Standalone Poetry project (Flask, blinker, click)
└── readme.md       # Brief description
```

## WHERE TO LOOK

| Task            | Location                              |
| --------------- | ------------------------------------- |
| Upload endpoint | `app.py`                              |
| File storage    | `uploads/` (UUID-named, no extension) |

## CONVENTIONS

- Standalone Poetry project — does NOT share deps with parent `pyproject.toml`
- Uploaded files are stored without extension using UUID4 as filename

## NOTES

- `uploads/` contains real uploaded files committed to the repo (sample data from local dev)
- `dump.rdb` is a Redis snapshot artifact — local dev only, not used in code here
- No routes beyond file upload; no authentication
