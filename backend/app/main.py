from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import config
from app.core.database import Base, engine
from app.core.logging import logger
from app.core.limiter import limiter
from app.core.idempotency import IdempotencyHitException
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
from app.apps.helb.routes import router as helb_router

# Initialize FastAPI application with metadata and version information.
app = FastAPI(title=config.project_name, version=config.project_version)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
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
app.include_router(helb_router)

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

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(IdempotencyHitException)
async def idempotency_hit_handler(request: Request, exc: IdempotencyHitException) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=exc.cached_data,
        headers={"X-Idempotency-Replayed": "true"}
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
