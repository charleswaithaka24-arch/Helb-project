from datetime import date

from pydantic import BaseModel


class CategoryBreakdownItem(BaseModel):
    category: str
    amount: float
    percentage: float


class WeeklyTrendPoint(BaseModel):
    date: date
    total: float


class DashboardResponse(BaseModel):
    total_balance: float
    protected_funds: float
    total_expenses: float
    daily_safe_limit: float
    projected_survival_date: date
    debt_status: dict[str, float]
    category_breakdown: list[CategoryBreakdownItem]
    weekly_spending_trend: list[WeeklyTrendPoint]
