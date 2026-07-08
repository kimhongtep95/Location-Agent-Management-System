# LAMS API

Backend API for the Location Agent Management System — FastAPI, async SQLAlchemy 2.0 (SQLite via
aiosqlite by default), JWT auth with PBKDF2 password hashing, layered into
`domain` / `application` / `infrastructure` / `presentation`.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Swagger docs at http://localhost:8000/docs. On first startup the app creates `lams.db` and seeds a
demo admin plus sample agents, locations, and assignments.

## Test

```bash
pytest -q
```

## Seeded demo login

```
admin@lams.local / Password123!
```
