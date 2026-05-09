from sqlalchemy import Column, Integer, String

from app.core.database import Base


class User(Base):
    """Database model for application users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="student")
