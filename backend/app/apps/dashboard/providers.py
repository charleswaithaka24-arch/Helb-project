from fastapi import Depends
from sqlalchemy.orm import Session

from app.apps.dashboard.service import DashboardService
from app.apps.debts.repository import DebtRepository
from app.apps.expenses.repository import ExpenseRepository
from app.apps.pockets.repository import PocketRepository
from app.apps.semesters.repository import SemesterRepository
from app.core.database import get_db


def get_semester_repository(db: Session = Depends(get_db)) -> SemesterRepository:
    return SemesterRepository(db=db)


def get_expense_repository(db: Session = Depends(get_db)) -> ExpenseRepository:
    return ExpenseRepository(db=db)


def get_pocket_repository(db: Session = Depends(get_db)) -> PocketRepository:
    return PocketRepository(db=db)


def get_debt_repository(db: Session = Depends(get_db)) -> DebtRepository:
    return DebtRepository(db=db)


def get_dashboard_service(
    semester_repository: SemesterRepository = Depends(get_semester_repository),
    expense_repository: ExpenseRepository = Depends(get_expense_repository),
    pocket_repository: PocketRepository = Depends(get_pocket_repository),
    debt_repository: DebtRepository = Depends(get_debt_repository),
) -> DashboardService:
    return DashboardService(
        semester_repository=semester_repository,
        expense_repository=expense_repository,
        pocket_repository=pocket_repository,
        debt_repository=debt_repository,
    )
