from fastapi import APIRouter, Depends

from app.apps.alerts.providers import get_alert_service
from app.apps.alerts.schemas import AlertResponse
from app.apps.alerts.service import AlertService
from app.core.security import get_current_user

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=list[AlertResponse])
def get_alerts(
    current_user=Depends(get_current_user),
    service: AlertService = Depends(get_alert_service),
) -> list[AlertResponse]:
    return service.list_alerts(user_id=current_user.id)
