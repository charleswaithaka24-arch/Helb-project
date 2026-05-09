# HELB App

A comprehensive financial management platform designed specifically for university students. The application helps students effectively manage their Higher Education Loans Board (HELB) disbursements alongside other income sources.

## 🌟 Features

- **User Management**: Secure authentication and user profile management.
- **Semester Tracking**: Organize finances and budgets on a per-semester basis.
- **Budgeting**: Plan your finances with robust budgeting tools.
- **Pockets**: Categorize your funds into dedicated "pockets" for better money allocation (e.g., tuition, rent, upkeep).
- **Expense Tracking**: Log and monitor daily expenses against your budget.
- **Debt Management**: Keep track of borrowed money and repayment schedules.
- **Payments**: Process and record payments efficiently.
- **Financial Advice**: Receive insights and tips on managing student finances.
- **Alerts & Notifications**: Get SMS alerts powered by Africa's Talking for critical updates and budget thresholds.
- **Dashboard**: A centralized view of your financial health.

## 🏗️ Architecture

The project is built with a focus on clean, modular architecture. 

Currently, the repository contains:

- **[`backend/`](backend/)**: A production-ready REST API built with FastAPI, using clean architecture principles and a feature-based structure.

A frontend client is currently in development and will be added to this repository.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 13+

### Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost/helb_db
AT_API_KEY=your_africastalking_api_key
AT_USERNAME=your_africastalking_username
SECRET_KEY=your_jwt_secret_key
```

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Ensure you have a `.env` file in the `backend` directory. The application uses environment variables for configuration. Set the appropriate database and API keys (like Africa's Talking).

5. **Apply Database Migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Run the Development Server:**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`. You can view the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Authentication**: JWT with Passlib (bcrypt)
- **Data Validation**: Pydantic
- **External Integrations**: [Africa's Talking](https://africastalking.com/) for SMS alerts

## 🧪 Testing

To run the backend tests, navigate to the `backend` directory and execute:

```bash
pytest
``` 