from fastapi import Depends
from sqlalchemy.orm import Session

from app.apps.expenses.repository import ExpenseRepository
from app.apps.expenses.service import ExpenseService
from app.apps.semesters.repository import SemesterRepository
from app.core.database import get_db


def get_expense_repository(db: Session = Depends(get_db)) -> ExpenseRepository:
    return ExpenseRepository(db=db)


def get_semester_repository(db: Session = Depends(get_db)) -> SemesterRepository:
    return SemesterRepository(db=db)


def get_expense_service(
    repository: ExpenseRepository = Depends(get_expense_repository),
    semester_repository: SemesterRepository = Depends(get_semester_repository),
) -> ExpenseService:
    return ExpenseService(repository=repository, semester_repository=semester_repository)
