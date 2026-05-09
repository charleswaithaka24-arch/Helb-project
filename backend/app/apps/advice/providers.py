from fastapi import Depends
from sqlalchemy.orm import Session

from app.apps.advice.repository import AdviceRepository
from app.apps.advice.service import AdviceService
from app.apps.expenses.repository import ExpenseRepository
from app.apps.semesters.repository import SemesterRepository
from app.core.database import get_db


def get_advice_repository(db: Session = Depends(get_db)) -> AdviceRepository:
    return AdviceRepository(db=db)


def get_expense_repository(db: Session = Depends(get_db)) -> ExpenseRepository:
    return ExpenseRepository(db=db)


def get_semester_repository(db: Session = Depends(get_db)) -> SemesterRepository:
    return SemesterRepository(db=db)


def get_advice_service(
    repository: AdviceRepository = Depends(get_advice_repository),
    expense_repository: ExpenseRepository = Depends(get_expense_repository),
    semester_repository: SemesterRepository = Depends(get_semester_repository),
) -> AdviceService:
    return AdviceService(
        repository=repository,
        expense_repository=expense_repository,
        semester_repository=semester_repository,
    )
