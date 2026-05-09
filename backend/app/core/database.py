from typing import Generator

# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import config

# Create the SQLAlchemy engine and declarative base for ORM models.
connect_args = {"check_same_thread": False} if config.database_url.startswith("sqlite") else {}
engine = create_engine(config.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
