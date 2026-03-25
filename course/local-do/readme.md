Use this to run a local file-upload server.

# Setup

This is a separate optional Poetry project. It is not part of the default repo-root Python setup.

From `course/local-do/`:

```bash
mise install
poetry env use 3.11
poetry install
poetry run python app.py
```

## Notes

- In the PDF app `.env`, set `UPLOAD_URL=http://localhost:8050`
- Restart the PDF app after changing `UPLOAD_URL`
