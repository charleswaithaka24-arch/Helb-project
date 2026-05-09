from fastapi import Depends
from sqlalchemy.orm import Session

from app.apps.debts.repository import DebtRepository
from app.apps.debts.service import DebtService
from app.apps.semesters.repository import SemesterRepository
from app.core.database import get_db


def get_debt_repository(db: Session = Depends(get_db)) -> DebtRepository:
    return DebtRepository(db=db)


def get_semester_repository(db: Session = Depends(get_db)) -> SemesterRepository:
    return SemesterRepository(db=db)


def get_debt_service(
    repository: DebtRepository = Depends(get_debt_repository),
    semester_repository: SemesterRepository = Depends(get_semester_repository),
) -> DebtService:
    return DebtService(repository=repository, semester_repository=semester_repository)
