# Task 3 — FastAPI: Building Web APIs

## Purpose

This task takes you from Python fundamentals (Task 1) and Git workflow (Task 2)
into building real, production-style web APIs with **FastAPI**.

It is an intensive, hands-on, **self-paced** program — there are no deadlines or
time limits here. Move at the pace that lets you actually understand each step.
You learn a concept, then immediately build it into one growing project — a
**Patient Management API**. By the end you will have a tested, documented,
authenticated REST API backed by a database.

This is build-heavy by design. Every step has something to ship.

> Containerizing this API with Docker and Docker Compose is **Task 4** — keep
> this project clean and runnable locally; you will dockerize it next.

## AI Usage Rule

AI tools are allowed for this task. Use them to learn faster — explain errors,
review your code, suggest tests, draft docs.

You must still **understand every line you commit**. Do not paste code you cannot
explain in review. If a reviewer asks "why does this work?", you should be able to
answer.

## Prerequisites

- Completed Task 1 (Python) and Task 2 (Git/GitHub).
- Python 3.11+ installed (`python --version`).
- Comfortable with the terminal, virtual environments, and Git branches.
- A REST/HTTP client: [HTTPie](https://httpie.io/), `curl`, or the built-in Swagger UI.

If HTTP methods (GET/POST/PUT/PATCH/DELETE), status codes, or JSON are
unfamiliar, skim [MDN: An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
first.

## What You Will Build — Patient Management API

A single project that grows in three parts:

- **Part 1:** A working API with in-memory data — endpoints, validation, docs.
- **Part 2:** A database, full CRUD, authentication, and an automated test suite.
- **Part 3 (optional):** Migrations, pagination, background tasks, and polish.

> Use **fake/sample patient data only** — never real patient data.

## API Specification — What You Must Build

Your finished API must implement **exactly these endpoints and models**. This is
the contract your tests (and any reviewer) will check against.

### Data models

**Patient**

| Field | Type | Rules |
| --- | --- | --- |
| `id` | int | server-generated, read-only |
| `name` | str | required, 1–100 chars |
| `age` | int | required, 0–120 |
| `condition` | str | required, non-empty |
| `risk_score` | int | required, 0–100 |
| `active` | bool | defaults to `true` |

Use separate Pydantic schemas: `PatientCreate` (no `id`), `PatientUpdate` (all
fields optional, for `PATCH`), and `PatientRead` (includes `id`).

**User** (for authentication): `id`, `username` (unique), and a **hashed**
password (never store or return plain text). `UserRead` exposes only `id` and
`username`.

### Endpoints

| Method | Path | Auth | Success | Description |
| --- | --- | --- | --- | --- |
| `GET` | `/health` | — | 200 | `{"status": "ok"}` |
| `POST` | `/auth/register` | — | 201 | Create a user from `{username, password}`; **409** if the username exists |
| `POST` | `/auth/token` | — | 200 | OAuth2 password form → `{access_token, token_type: "bearer"}`; **401** on bad credentials |
| `GET` | `/patients` | — | 200 | List patients; supports `?active=`, `?condition=`, `?limit=`, `?offset=` |
| `GET` | `/patients/{id}` | — | 200 | One patient; **404** if missing |
| `POST` | `/patients` | ✅ | 201 | Create a patient from `PatientCreate`; **422** on invalid data |
| `PUT` | `/patients/{id}` | ✅ | 200 | Full replace; **404** if missing |
| `PATCH` | `/patients/{id}` | ✅ | 200 | Partial update from `PatientUpdate`; **404** if missing |
| `DELETE` | `/patients/{id}` | ✅ | 204 | Delete; **404** if missing |

**Auth ✅** means the request must carry a valid JWT (`Authorization: Bearer
<token>`); without it the API returns **401**.

### Status codes you must use correctly

`200` OK · `201` Created · `204` No Content · `401` Unauthorized ·
`404` Not Found · `409` Conflict · `422` Unprocessable Entity (validation).

## What You Will Learn

- ASGI, `uvicorn`, and how a FastAPI app starts and serves requests
- Path & query parameters, request bodies, and response models
- Data validation and serialization with **Pydantic v2**
- HTTP status codes and structured error handling (`HTTPException`)
- Automatic interactive docs (Swagger UI / ReDoc) and OpenAPI
- Project structure: routers, dependencies, settings
- **Dependency injection** (`Depends`)
- Databases with **SQLModel** (SQLAlchemy + Pydantic) and full **CRUD**
- `async`/`await` request handlers
- Authentication & authorization with **OAuth2 + JWT** and password hashing
- Middleware, CORS, and configuration via environment variables
- **Testing** with `pytest` + `httpx`/`TestClient`
- (Optional) Alembic migrations, background tasks, pagination, logging

## Environment Setup

A runnable starter already lives in this `task3/` folder. Set it up on a branch:

```bash
git switch -c task3/patient-api
cd task3
python -m venv .venv
source .venv/bin/activate        # macOS/Linux  (Windows: .venv\Scripts\activate)
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

## Learning Resources

**Start here**

- [FastAPI — Tutorial / User Guide](https://fastapi.tiangolo.com/tutorial/) — work through it in order; it mirrors this task.
- [FastAPI — First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)

**Video courses (YouTube)**

- [Create an API in 20 minutes with FastAPI](https://www.youtube.com/watch?v=ICnKq9fgLrI) — quick taste of the framework.
- [FastAPI — A Python Framework, Full Course (freeCodeCamp / Bitfumes)](https://www.youtube.com/watch?v=7t2alSnE2-I) — a solid end-to-end beginner course.
- [Python API Development — Comprehensive Course (freeCodeCamp)](https://www.youtube.com/watch?v=Yw4LmMQXXFs) — deep dive (database, auth, tests, deploy).
- [FastAPI Beyond CRUD — Full Course](https://www.youtube.com/watch?v=TO4aQ3ghFOc) — structuring a larger, real-world API.

**By topic**

| Topic | Resource |
| --- | --- |
| Path & query params | [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/) · [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/) |
| Request bodies & models | [Request Body](https://fastapi.tiangolo.com/tutorial/body/) · [Pydantic v2 docs](https://docs.pydantic.dev/latest/) |
| Response models & status | [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/) · [Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/) |
| Error handling | [Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) |
| Project structure | [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) |
| Dependency injection | [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) |
| Databases | [SQLModel docs](https://sqlmodel.tiangolo.com/) · [FastAPI + SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) |
| Async | [Concurrency and async / await](https://fastapi.tiangolo.com/async/) |
| Security (OAuth2 + JWT) | [Security tutorial](https://fastapi.tiangolo.com/tutorial/security/) · [OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) |
| Configuration | [Settings & environment variables](https://fastapi.tiangolo.com/advanced/settings/) |
| Middleware & CORS | [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) · [CORS](https://fastapi.tiangolo.com/tutorial/cors/) |
| Testing | [Testing](https://fastapi.tiangolo.com/tutorial/testing/) · [pytest](https://docs.pytest.org/) · [HTTPX](https://www.python-httpx.org/) |
| Migrations | [Alembic docs](https://alembic.sqlalchemy.org/) |
| Server | [Uvicorn](https://www.uvicorn.org/) |

**Reference & extra practice**

- [FastAPI — Advanced User Guide](https://fastapi.tiangolo.com/advanced/)
- [REST API design best practices (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- [HTTP status codes (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

## Part 1 — FastAPI Fundamentals

Goal: a working, validated, documented API that serves patient data from an
in-memory list.

| Focus | Build |
| --- | --- |
| What is an API, HTTP, ASGI, uvicorn; the project & first `GET /` | A running app with `/` and `/health`; explore `/docs` |
| Path & query parameters; type coercion & validation | `GET /patients` (with `?active=`, `?limit=`) and `GET /patients/{id}` |
| Pydantic v2 models, request bodies, `response_model` | `Patient` / `PatientCreate` models; `POST /patients` |
| Status codes & error handling (`HTTPException`) | 404 for missing patient; 201 on create; validation errors |
| Update & delete; `PUT`/`PATCH` semantics | `PUT /patients/{id}`, `PATCH`, `DELETE /patients/{id}` |
| Project structure: routers & `Depends`; OpenAPI tags & summaries | Split into `app/main.py` and `app/routers/patients.py`; tidy docs |

**Reference — your first endpoint**

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI(title="Patient Management API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

**Part 1 — Checkpoint**

- [ ] App runs with `uvicorn app.main:app --reload`.
- [ ] CRUD endpoints for patients work against an in-memory store.
- [ ] Request/response bodies are validated by Pydantic models.
- [ ] Correct status codes (200, 201, 204, 404, 422) are returned.
- [ ] `/docs` is clean: every endpoint has a tag, summary, and response model.
- [ ] You committed your work in small steps on the `task3/patient-api` branch.

---

## Part 2 — Data, Auth & Testing

Goal: persist data in a real database, secure the API, and prove it works with
automated tests.

| Focus | Build |
| --- | --- |
| SQLModel: engine, `Session`, table models; `Depends(get_session)` | SQLite database; `Patient` table model; DB-backed `get_session` dependency |
| Move CRUD to the database; query patterns | Rewrite all patient endpoints to read/write the database |
| `async` handlers; when async helps and when it doesn't | Make appropriate handlers `async`; understand the trade-offs |
| OAuth2 password flow, JWT, password hashing (`passlib`) | `User` model, `POST /auth/register`, `POST /auth/token`, `get_current_user` |
| Protect routes; config via `pydantic-settings` / env vars | Require auth for write endpoints; load `SECRET_KEY` from env |
| Testing with `pytest` + `httpx`/`TestClient`; test DB fixture | A test suite covering CRUD, validation errors, and auth |

**Reference — a protected endpoint**

```python
from fastapi import Depends
from .auth import get_current_user

@router.post("/patients", status_code=201, response_model=Patient)
def create_patient(
    data: PatientCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),  # require login
):
    ...
```

**Part 2 — Checkpoint**

- [ ] Data persists in SQLite across restarts.
- [ ] All CRUD endpoints use the database via a `get_session` dependency.
- [ ] Users can register and obtain a JWT from `/auth/token`.
- [ ] Write endpoints reject unauthenticated requests with **401**.
- [ ] Secrets come from environment variables, not hard-coded.
- [ ] `pytest` passes with tests for happy paths, validation, and auth.

---

## Part 3 — Going Further (Optional)

Goal: take the API closer to something you could actually deploy.

| Focus | Build |
| --- | --- |
| Alembic migrations | Initialize Alembic; generate and apply the first migration |
| Pagination, filtering, sorting | `GET /patients?limit=&offset=&condition=&sort=` |
| Background tasks & `lifespan` events | A background task (e.g. audit log) and startup/shutdown hooks |
| Middleware, CORS, structured logging, request IDs | Logging middleware; CORS for a frontend origin |
| OpenAPI polish | Descriptions, examples, versioning |

**Part 3 — Checkpoint**

- [ ] Schema changes are managed by Alembic migrations.
- [ ] List endpoints support pagination and at least one filter.
- [ ] Logging and CORS are configured.

> Next up: **Task 4** containerizes this API (Dockerfile + Docker Compose with a
> database and Redis).

---

## Testing & Coverage (required)

**You write the tests.** A starter test for `/health` is included so the suite
runs from day one — every other endpoint in the API specification is yours to
cover. Use `pytest` with FastAPI's `TestClient` (see the
[Testing guide](https://fastapi.tiangolo.com/tutorial/testing/)).

Your test suite must reach **more than 98% line coverage** of the `app/` package.
Measure it with [`pytest-cov`](https://pytest-cov.readthedocs.io/):

```bash
pytest --cov=app --cov-report=term-missing
```

`--cov-report=term-missing` prints the exact lines you have not covered yet —
work through them until you are above 98%. CI enforces this with a hard gate:

```bash
pytest --cov=app --cov-fail-under=98
```

What to test (at least):

- **Happy paths** for every endpoint and the correct success status code.
- **Validation errors** (422) — e.g. `age` out of range, missing `name`, `risk_score > 100`.
- **Not found** (404) for reads/updates/deletes of unknown ids.
- **Auth**: register, log in, and that write endpoints return **401** without a token and succeed with one.
- **Conflict** (409) when registering a duplicate username.
- Query behaviour for `/patients` filters and pagination.

> Coverage is a floor, not the goal. 98% with weak assertions is worse than
> thoughtful tests — make each test actually check behaviour, not just run code.

## Capstone Requirements

Whatever pace you take, the final API must:

1. Implement the full [API specification](#api-specification--what-you-must-build) above.
2. Be backed by a database with full CRUD.
3. Validate all input/output with Pydantic models (separate create/read/update models).
4. Use correct HTTP status codes and return structured errors.
5. Require authentication (JWT) for write operations.
6. Load configuration (secrets, DB URL) from environment variables.
7. Ship with a trainee-written `pytest` suite that passes at **>98% coverage**.
8. Have a `README.md` explaining how to install, run, and test it, and expose clean OpenAPI at `/docs`.

## Suggested Project Structure

The starter gives you `app/main.py`, `tests/`, and `conftest.py`. Grow it into:

```text
task3/
├── README.md
├── requirements.txt
├── .env.example            # documents required env vars (no real secrets)
├── conftest.py             # puts task3/ on the import path for tests
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app, router registration   (provided)
│   ├── config.py           # pydantic-settings
│   ├── database.py         # engine, get_session
│   ├── models.py           # SQLModel tables + Pydantic schemas
│   ├── auth.py             # hashing, JWT, get_current_user
│   └── routers/
│       ├── patients.py
│       └── auth.py
└── tests/
    ├── test_health.py      # provided starter test
    ├── test_patients.py    # you write these
    └── test_auth.py
```

## How to Run

```bash
cd task3
source .venv/bin/activate
uvicorn app.main:app --reload          # http://127.0.0.1:8000/docs
pytest                                 # run the test suite
pytest --cov=app --cov-report=term-missing   # run with coverage
```

## Submission Checklist

- [ ] I worked on a `task3/...` branch and committed in small, meaningful steps.
- [ ] The API implements the full API specification (every endpoint and model).
- [ ] I wrote the tests myself and `pytest` passes locally.
- [ ] `pytest --cov=app` reports **more than 98%** coverage.
- [ ] I used fake/sample patient data only — no real patient data, no secrets committed.
- [ ] I added a `.env.example` and did **not** commit a real `.env`.
- [ ] The `README.md` explains install, run, and test steps.
- [ ] I opened a pull request into `main` with a clear description.

## Reflection

Add your reflection before submitting:

```text
1. What does a path operation (endpoint) actually do when a request arrives?
2. Why use Pydantic response models instead of returning raw dicts?
3. What is dependency injection and where did you use it?
4. How does JWT authentication work in your API, step by step?
5. What was the hardest bug you hit, and how did you debug it?
6. What would you add or change to make this API production-ready?
```




# Running with Docker

## Prerequisites

- Docker Desktop installed
- Docker Compose

## Build and start the application

```bash
docker compose up --build
```

The API will be available at:

http://localhost:8000/docs

## Check running containers

```bash
docker compose ps
```

## View API logs

```bash
docker compose logs api
```

## Stop the containers

```bash
docker compose down
```

Database data is stored in a Docker named volume, so it persists across container restarts.