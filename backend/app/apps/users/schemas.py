from typing import List
from pydantic import BaseModel, EmailStr
from app.apps.bookings.schemas import BookingResponse


class UserBase(BaseModel):
    email: EmailStr
    role: str = "student"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class StudentWithLoansResponse(UserResponse):
    loans: List[BookingResponse] = []
