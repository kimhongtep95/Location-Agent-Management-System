# Location Agent Management System (LAMS)

A full-stack system for managing field agents, physical locations, and the assignments that put an
agent at a location — with a check-in / check-out workflow and an operations dashboard.

## Domain

- **User** — `id`, `email` (unique), `password_hash`, `full_name`, `role` (`admin` | `manager` |
  `agent`), `created_at`.
- **Agent** — `id`, `full_name`, `email`, `phone`, `region`, `status` (`active` | `inactive` |
  `on_leave`), `created_at`.
- **Location** — `id`, `name`, `address`, `city`, `latitude`, `longitude`, `is_active`,
  `created_at`.
- **Assignment** — `id`, `agent_id`, `location_id`, `status` (`assigned` | `checked_in` |
  `checked_out` | `completed`), `assigned_at`, `check_in_at`, `check_out_at`, `notes`.

## Tech stack

**Backend** — FastAPI, async SQLAlchemy 2.0, Pydantic v2 / pydantic-settings, PyJWT, PBKDF2
password hashing, pytest. Layered into `domain` / `application` / `infrastructure` / `presentation`.
The database is **SQLite via aiosqlite** by default, so there is no external Postgres/Redis to run.
Tables are created on startup and a demo dataset is seeded automatically.

**Frontend** — React 18 + TypeScript + Vite, MUI v6, react-router-dom v6,
@tanstack/react-query v5, zustand v5, react-hook-form v7, chart.js + react-chartjs-2.

## Project layout

```
location-agent-management-system/
  backend/    # FastAPI application + pytest tests
  frontend/   # React + Vite single-page app
  docker-compose.yml
```

## Running the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The API runs at http://localhost:8000. Interactive Swagger docs are at http://localhost:8000/docs.
On first startup the app creates `lams.db` and seeds a demo admin, agents, locations, and
assignments.

Run the tests:

```bash
cd backend
pytest -q
```

## Running the frontend

```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_BASE_URL defaults to http://localhost:8000/api/v1
npm run dev
```

The app runs at http://localhost:5173.

## Running with Docker

```bash
docker compose up --build
```

- API: http://localhost:8000
- Web: http://localhost:5173

## Seeded demo login

```
email:    admin@lams.local
password: Password123!
```

## API surface (prefix `/api/v1`)

- `POST /auth/register`, `POST /auth/login`, `GET /auth/me`
- `GET/POST /agents`, `GET/PATCH/DELETE /agents/{id}`
- `GET/POST /locations`, `GET/PATCH/DELETE /locations/{id}`
- `GET/POST /assignments`, `POST /assignments/{id}/check-in`,
  `POST /assignments/{id}/check-out`
- `GET /dashboard/stats`

## Frontend areas

All screens are behind authentication. After logging in at `/login`, the app shell provides:

- **Dashboard** — headline stats (agents, locations, active assignments, checked-in now) and
  charts (agents by status, assignments by location).
- **Agents** — searchable table with create/edit/delete and a status filter.
- **Locations** — table with create/edit/delete (coordinates + active toggle).
- **Assignments** — assign an agent to a location, then check in / check out with live status.

The JWT is held in a zustand store and persisted to localStorage; the API client attaches it as a
Bearer token.
