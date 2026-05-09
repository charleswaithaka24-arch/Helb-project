from fastapi import APIRouter, Depends

from app.apps.dashboard.providers import get_dashboard_service
from app.apps.dashboard.schemas import DashboardResponse
from app.apps.dashboard.service import DashboardService
from app.core.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    current_user=Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardResponse:
    return service.get_dashboard(user_id=current_user.id)
