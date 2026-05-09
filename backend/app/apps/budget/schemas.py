from datetime import date

from pydantic import BaseModel


class DailyLimitResponse(BaseModel):
    remaining_balance: float
    remaining_days: int
    recommended_daily_limit: float
    projected_runout_date: date
    budget_health_status: str
