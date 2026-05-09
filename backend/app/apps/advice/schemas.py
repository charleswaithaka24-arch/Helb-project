from datetime import datetime

from pydantic import BaseModel


class AdviceResponse(BaseModel):
    message: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
