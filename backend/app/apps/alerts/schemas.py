from datetime import datetime

from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: int
    level: str
    message: str
    context: str | None
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True
