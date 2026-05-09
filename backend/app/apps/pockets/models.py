from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PocketType(str, Enum):
    rent = "rent"
    school_fees = "school_fees"
    emergency = "emergency"
    custom = "custom"


class Pocket(Base):
    """Database model for protected money pockets."""
    __tablename__ = "pockets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    current_balance = Column(Float, nullable=False, default=0.0)
    locked = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    semester = relationship("Semester", backref="pockets")


class PocketTransaction(Base):
    """Transaction history for pocket allocations and withdrawals."""
    __tablename__ = "pocket_transactions"

    id = Column(Integer, primary_key=True, index=True)
    pocket_id = Column(Integer, ForeignKey("pockets.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pocket = relationship("Pocket", backref="transactions")
