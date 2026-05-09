from fastapi import APIRouter, Depends, Path, status

from app.apps.debts.providers import get_debt_service
from app.apps.debts.schemas import DebtCreate, DebtPayRequest, DebtResponse, DebtSummary
from app.apps.debts.service import DebtService
from app.core.security import get_current_user

router = APIRouter(prefix="/debts", tags=["debts"])


@router.post("/", response_model=DebtResponse, status_code=status.HTTP_201_CREATED)
def create_debt(
    debt_in: DebtCreate,
    current_user=Depends(get_current_user),
    service: DebtService = Depends(get_debt_service),
) -> DebtResponse:
    return service.create_debt(current_user.id, debt_in=debt_in)


@router.get("/", response_model=list[DebtResponse])
def list_debts(
    current_user=Depends(get_current_user),
    service: DebtService = Depends(get_debt_service),
) -> list[DebtResponse]:
    return service.list_debts(current_user.id)


@router.post("/{debt_id}/pay", response_model=DebtResponse)
def pay_debt(
    debt_id: int = Path(..., ge=1),
    request: DebtPayRequest = Depends(),
    current_user=Depends(get_current_user),
    service: DebtService = Depends(get_debt_service),
) -> DebtResponse:
    return service.pay_debt(user_id=current_user.id, debt_id=debt_id, pay_request=request)


@router.get("/summary", response_model=DebtSummary)
def debt_summary(
    current_user=Depends(get_current_user),
    service: DebtService = Depends(get_debt_service),
) -> DebtSummary:
    return service.debt_summary(current_user.id)
