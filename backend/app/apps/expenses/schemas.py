from datetime import datetime, date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


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


class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0)
    category: ExpenseCategory
    note: Optional[str] = None
    timestamp: Optional[datetime] = None
    location: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    semester_id: Optional[int] = None


class ExpenseResponse(ExpenseBase):
    id: int
    semester_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseSummary(BaseModel):
    period: str
    total: float
    categories: dict[str, float]
    breakdown: dict[str, float]
    expense_count: int


class ExpenseTrendPoint(BaseModel):
    period: str
    total: float
