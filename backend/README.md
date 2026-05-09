# Backend

A production-ready FastAPI backend starter using clean architecture and modular feature-based structure.

## Project structure

- `app/`: application package and entrypoint
- `app/core/`: core configuration, settings, database, and security utilities
- `app/apps/`: feature modules grouped by domain (`users`, `payments`, `bookings`)
- `app/shared/`: shared utilities, middleware, and exception helpers
- `tests/`: integration-style tests for feature APIs
- `alembic/`: migration configuration and version scripts

## Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment

The application uses environment variables for configuration. Copy the provided `.env` file and update the values:

```bash
# Application Configuration
PROJECT_NAME=backend
PROJECT_VERSION=0.1.0

# Database Configuration
DATABASE_URL=sqlite:///./backend.db

# Security Configuration
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# Africa's Talking SMS Configuration
AFRICASTALKING_USERNAME=your_africastalking_username
AFRICASTALKING_API_KEY=your_africastalking_api_key
```

**Security Note:** Never commit the `.env` file to version control. Add it to `.gitignore`.

## Run the server

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

## Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "initial"
```

Apply migrations:

```bash
alembic upgrade head
```

## Tests

```bash
pytest
```
