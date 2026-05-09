from sqlalchemy.orm import Session

from app.apps.semesters.models import Semester
from app.apps.semesters.schemas import SemesterCreate


class SemesterRepository:
    """Database access layer for semester entities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, semester_id: int) -> Semester | None:
        return self.db.query(Semester).filter(Semester.id == semester_id).first()

    def get_active_by_user(self, user_id: int) -> Semester | None:
        return self.db.query(Semester).filter(Semester.user_id == user_id, Semester.active.is_(True)).first()

    def list_by_user(self, user_id: int) -> list[Semester]:
        return self.db.query(Semester).filter(Semester.user_id == user_id).order_by(Semester.start_date.desc()).all()

    def create(self, user_id: int, semester_in: SemesterCreate) -> Semester:
        semester = Semester(
            user_id=user_id,
            name=semester_in.name,
            start_date=semester_in.start_date,
            end_date=semester_in.end_date,
            expected_helb_amount=semester_in.expected_helb_amount,
            active=False,
        )
        self.db.add(semester)
        self.db.commit()
        self.db.refresh(semester)
        return semester

    def deactivate_all_for_user(self, user_id: int) -> None:
        self.db.query(Semester).filter(Semester.user_id == user_id, Semester.active.is_(True)).update({"active": False})
        self.db.commit()

    def activate(self, semester: Semester) -> Semester:
        semester.active = True
        self.db.commit()
        self.db.refresh(semester)
        return semester
