from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import config
from app.core.database import Base, engine
from app.core.logging import logger
from app.shared.middleware import register_middleware
from app.apps.users.routes import router as users_router
from app.apps.payments.routes import router as payments_router
from app.apps.bookings.routes import router as bookings_router
from app.apps.semesters.routes import router as semesters_router
from app.apps.expenses.routes import router as expenses_router
from app.apps.pockets.routes import router as pockets_router
from app.apps.debts.routes import router as debts_router
from app.apps.alerts.routes import router as alerts_router
from app.apps.advice.routes import router as advice_router
from app.apps.dashboard.routes import router as dashboard_router
from app.apps.budget.routes import router as budget_router

# Initialize FastAPI application with metadata and version information.
app = FastAPI(title=config.project_name, version=config.project_version)
register_middleware(app)

# Register feature routers.
app.include_router(users_router)
app.include_router(payments_router)
app.include_router(bookings_router)
app.include_router(semesters_router)
app.include_router(expenses_router)
app.include_router(pockets_router)
app.include_router(debts_router)
app.include_router(alerts_router)
app.include_router(advice_router)
app.include_router(dashboard_router)
app.include_router(budget_router)

# Ensure DB tables are created when the application starts.
@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception("Database exception occurred while handling request.")
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred. Please try again later."},
    )


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        if exc.status_code == 500:
            logger.exception("HTTP 500 error occurred.")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
        return await http_exception_handler(exc, request)

    logger.exception("Unhandled exception occurred.")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


@app.get("/", response_class=JSONResponse)
def health_check() -> JSONResponse:
    """Simple health check endpoint."""
    return JSONResponse({"status": "ok", "project": config.project_name})
