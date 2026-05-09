from datetime import datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    customer_name: str
    phone_number: str
    loan_amount: float


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoanApprovalRequest(BaseModel):
    booking_id: int
