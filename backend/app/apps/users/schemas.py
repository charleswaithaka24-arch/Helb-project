from pydantic import BaseModel, EmailStr


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
