from fastapi import Depends
from sqlalchemy.orm import Session

from app.apps.semesters.repository import SemesterRepository
from app.apps.semesters.service import SemesterService
from app.core.database import get_db


def get_semester_repository(db: Session = Depends(get_db)) -> SemesterRepository:
    return SemesterRepository(db=db)


def get_semester_service(repository: SemesterRepository = Depends(get_semester_repository)) -> SemesterService:
    return SemesterService(repository=repository)
