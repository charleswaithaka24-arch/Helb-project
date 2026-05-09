from fastapi import APIRouter, Depends

from app.apps.advice.providers import get_advice_service
from app.apps.advice.schemas import AdviceResponse
from app.apps.advice.service import AdviceService
from app.core.security import get_current_user

router = APIRouter(prefix="/advice", tags=["advice"])


@router.get("/", response_model=list[AdviceResponse])
def get_advice(
    current_user=Depends(get_current_user),
    service: AdviceService = Depends(get_advice_service),
) -> list[AdviceResponse]:
    return service.generate_advice(user_id=current_user.id)
