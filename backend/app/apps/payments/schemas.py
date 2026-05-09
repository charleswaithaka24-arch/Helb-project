from pydantic import BaseModel


class PaymentBase(BaseModel):
    amount: float


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    status: str

    class Config:
        from_attributes = True
