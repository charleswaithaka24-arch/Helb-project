from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class ExpenseCategory(str, Enum):
    food = "food"
    transport = "transport"
    airtime = "airtime"
    shopping = "shopping"
    entertainment = "entertainment"
    academics = "academics"
    rent = "rent"
    medical = "medical"
    other = "other"


class Expense(Base):
    """Database model for expense records."""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    note = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default="now()")

    semester = relationship("Semester", backref="expenses")
