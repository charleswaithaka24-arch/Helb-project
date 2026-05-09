from sqlalchemy import Column, Float, Integer, String

from app.core.database import Base


class Payment(Base):
    """Database model for payment records."""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="pending")
