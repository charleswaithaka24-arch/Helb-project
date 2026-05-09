from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PocketType(str, Enum):
    rent = "rent"
    school_fees = "school_fees"
    emergency = "emergency"
    custom = "custom"


class PocketBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    type: PocketType
    initial_balance: float = Field(0.0, ge=0.0)


class PocketCreate(PocketBase):
    pass


class PocketResponse(BaseModel):
    id: int
    name: str
    type: PocketType
    current_balance: float
    locked: bool
    semester_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PocketTransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    note: Optional[str] = None


class PocketAllocateRequest(PocketTransactionBase):
    pass


class PocketWithdrawRequest(PocketTransactionBase):
    emergency_override: bool = False


class PocketLockResponse(BaseModel):
    id: int
    locked: bool

    class Config:
        from_attributes = True
