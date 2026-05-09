# pyrefly: ignore [missing-import]
from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
# pyrefly: ignore [missing-import]
from sqlalchemy.sql import func

from app.core.database import Base


class Booking(Base):
    """Database model for booking/loan records."""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    loan_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="loans")
