from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.apps.expenses.providers import get_expense_service
from app.apps.expenses.schemas import ExpenseCreate, ExpenseResponse, ExpenseSummary
from app.apps.expenses.service import ExpenseService
from app.core.security import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_in: ExpenseCreate,
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
) -> ExpenseResponse:
    return service.create_expense(user_id=current_user.id, expense_in=expense_in)


@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(
    semester_id: int | None = Query(None, description="Optional semester filter."),
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
) -> list[ExpenseResponse]:
    return service.list_expenses(user_id=current_user.id, semester_id=semester_id)


@router.get("/summary", response_model=ExpenseSummary)
def get_expense_summary(
    period: str = Query("semester", pattern="^(today|week|month|semester)$"),
    semester_id: int | None = Query(None, description="Optional semester ID for semester summary."),
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
) -> ExpenseSummary:
    return service.get_expense_summary(user_id=current_user.id, period=period, semester_id=semester_id)
