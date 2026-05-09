from app.apps.semesters.repository import SemesterRepository
from app.apps.semesters.schemas import SemesterCreate
from app.shared.exceptions import raise_not_found, raise_conflict


class SemesterService:
    """Business logic for semester lifecycle management."""

    def __init__(self, repository: SemesterRepository) -> None:
        self.repository = repository

    def create_semester(self, user_id: int, semester_in: SemesterCreate):
        if semester_in.end_date <= semester_in.start_date:
            raise_conflict("Semester end date must be after the start date.")

        return self.repository.create(user_id=user_id, semester_in=semester_in)

    def list_semesters(self, user_id: int):
        return self.repository.list_by_user(user_id=user_id)

    def get_semester(self, semester_id: int, user_id: int):
        semester = self.repository.get_by_id(semester_id)
        if not semester or semester.user_id != user_id:
            raise_not_found("Semester not found.")
        return semester

    def activate_semester(self, semester_id: int, user_id: int):
        semester = self.get_semester(semester_id=semester_id, user_id=user_id)
        self.repository.deactivate_all_for_user(user_id=user_id)
        return self.repository.activate(semester)

    def get_active_semester(self, user_id: int):
        semester = self.repository.get_active_by_user(user_id=user_id)
        if not semester:
            raise_not_found("No active semester found. Create and activate a semester first.")
        return semester
