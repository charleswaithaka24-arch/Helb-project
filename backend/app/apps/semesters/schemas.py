from datetime import date, datetime

from pydantic import BaseModel, Field


class SemesterBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=80)
    start_date: date
    end_date: date
    expected_helb_amount: float = Field(..., gt=0)


class SemesterCreate(SemesterBase):
    pass


class SemesterResponse(SemesterBase):
    id: int
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
