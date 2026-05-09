from datetime import date, datetime

from pydantic import BaseModel, Field


class DebtBase(BaseModel):
    creditor_name: str = Field(..., min_length=2, max_length=100)
    original_amount: float = Field(..., gt=0)
    interest_rate: float = Field(0.0, ge=0.0)
    due_date: date


class DebtCreate(DebtBase):
    pass


class DebtPayRequest(BaseModel):
    amount: float = Field(..., gt=0)


class DebtResponse(DebtBase):
    id: int
    remaining_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DebtSummary(BaseModel):
    total_debt: float
    remaining_debt: float
    debt_to_income_ratio: float
    active_debts: int
