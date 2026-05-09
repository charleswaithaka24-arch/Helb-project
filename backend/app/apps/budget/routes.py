from fastapi import APIRouter, Depends

from app.apps.budget.providers import get_budget_service
from app.apps.budget.schemas import DailyLimitResponse
from app.apps.budget.service import BudgetService
from app.core.security import get_current_user

router = APIRouter(prefix="/budget", tags=["budget"])


@router.get("/daily-limit", response_model=DailyLimitResponse)
def get_daily_limit(
    current_user=Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
) -> DailyLimitResponse:
    return service.get_daily_limit(user_id=current_user.id)
