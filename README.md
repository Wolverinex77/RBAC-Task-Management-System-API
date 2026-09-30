# Task Management System

A FastAPI-based task management API for organizing users, teams, projects, and project tasks. The application uses SQLAlchemy for persistence, JWT bearer tokens for authentication, and role-based access control for administrative operations.

## Features

- User registration and login
- JWT access-token authentication
- Argon2 password hashing through Passlib
- Admin-protected operations
- Team creation and team-member management
- Project creation, viewing, and archiving
- Task creation and assignment to project members
- Task state transitions from `in-progress` to `done`
- Task archiving
- Task audit-history endpoints
- Automatic database-table creation on application startup
- Interactive OpenAPI documentation through FastAPI

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy 2.x
- Pydantic
- Passlib with Argon2
- `python-jose` for JWT tokens
- PostgreSQL-compatible SQLAlchemy database configuration

## Project Structure

```text
TaskManagementSystem/
├── auth.py                 # JWT authentication and password helpers
├── database.py             # SQLAlchemy engine, Base, and session dependency
├── exceptions.py           # Domain-specific exceptions
├── main.py                 # FastAPI application and router registration
├── models/                 # SQLAlchemy ORM models
├── routers/                # HTTP API routes
├── schemas/                # Pydantic request and response schemas
├── services/               # Application and business logic
├── config.py               # Environment-backed application settings
├── .env.example            # Environment variable template
├── .gitignore
└── README.md
```

## API Routes

| Area | Prefix | Examples |
| --- | --- | --- |
| Authentication | `/auth` | `POST /auth/register`, `POST /auth/login` |
| Teams | `/teams` | `POST /teams/`, `POST /teams/{id}/add-user` |
| Projects | `/projects` | `POST /projects/`, `GET /projects/{project_id}` |
| Project tasks | `/projects` | `GET /projects/{id}/tasks` |
| Tasks | `/tasks` | `POST /tasks/`, `POST /tasks/{id}/change-state` |
| Task administration | `/tasks` | `POST /tasks/{id}/archive-task`, `GET /tasks/{id}/audit` |

Use the generated Swagger documentation for the complete request and response schemas.

## Prerequisites

- Python 3.10 or later
- A PostgreSQL database, or another SQLAlchemy-supported database with a compatible connection URL

## Local Setup

### 1. Clone or copy the project

```bash
git clone <repository-url>
cd TaskManagementSystem
```

### 2. Create a virtual environment

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database and secrets

Copy the environment template:

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bash
# macOS/Linux
cp .env.example .env
```

Set the following values in `.env`:

- `DATABASE_URL`: PostgreSQL connection URL.
- `SECRET_KEY`: a unique, long, randomly generated JWT signing key.
- `JWT_ALGORITHM`: JWT signing algorithm, normally `HS256`.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: access-token lifetime.

The application loads these values in [`config.py`](config.py). Missing required values cause startup to fail with a clear configuration error. The `.env` file is ignored by Git; commit only [`.env.example`](.env.example).

If the old JWT secret was used outside local development, rotate it immediately. Existing tokens signed with the previous secret will no longer be valid after rotation.

### 5. Start the API

From the project directory:

```bash
uvicorn main:app --reload
```

The API is available at:

- Base URL: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- OpenAPI schema: <http://localhost:8000/openapi.json>

Tables are created through `Base.metadata.create_all(engine)` when the application starts. For production, use a migration tool such as Alembic instead of relying on startup table creation.

## Authentication

1. Register a user with `POST /auth/register`.
2. Log in with `POST /auth/login`.
3. Copy the returned bearer token.
4. Select **Authorize** in Swagger UI and enter:

```text
Bearer <access-token>
```

Some routes require an administrator role. The role is checked by the `require_admin` dependency.

## Task Workflow

Tasks are assigned to users who belong to the relevant project team. The supported state values are:

- `in-progress`
- `done`

Task state changes are exposed through `POST /tasks/{id}/change-state`. Administrative users can archive tasks and inspect their audit history.

## Development Notes

- The API uses synchronous SQLAlchemy sessions.
- Business logic is kept in the `services/` package, while route handlers translate domain exceptions into HTTP responses.
- Keep validation and authorization in the backend; clients must not be trusted to enforce project membership or task permissions.
- Never commit `.env`; use `.env.example` to document required configuration.
- Add automated tests before making production changes.

## License

No license has been specified yet. This project is currently not licensed for reuse or redistribution.
