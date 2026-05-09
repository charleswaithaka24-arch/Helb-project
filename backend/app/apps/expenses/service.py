from datetime import date, datetime, timedelta
from typing import Optional

from app.apps.expenses.repository import ExpenseRepository
from app.apps.expenses.schemas import ExpenseCreate
from app.apps.semesters.repository import SemesterRepository
from app.shared.exceptions import raise_conflict, raise_not_found


class ExpenseService:
    """Business logic around expense creation and analytics."""

    def __init__(self, repository: ExpenseRepository, semester_repository: SemesterRepository) -> None:
        self.repository = repository
        self.semester_repository = semester_repository

    def create_expense(self, user_id: int, expense_in: ExpenseCreate):
        semester = None
        if expense_in.semester_id:
            semester = self.semester_repository.get_by_id(expense_in.semester_id)
            if not semester or semester.user_id != user_id:
                raise_not_found("Semester not found for this expense.")
        else:
            semester = self.semester_repository.get_active_by_user(user_id=user_id)
            if not semester:
                raise_conflict("No active semester available. Activate a semester before logging expenses.")

        expense = self.repository.create(expense_in=expense_in, user_id=user_id, semester_id=semester.id)
        return expense

    def list_expenses(self, user_id: int, semester_id: int | None = None):
        return self.repository.list_by_user(user_id=user_id, semester_id=semester_id)

    def get_expense_summary(
        self,
        user_id: int,
        period: str,
        semester_id: int | None = None,
        today: date | None = None,
    ) -> dict:
        today = today or date.today()
        if period == "today":
            start_date = today
            end_date = today
        elif period == "week":
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif period == "month":
            start_date = today.replace(day=1)
            end_date = today
        elif period == "semester":
            if semester_id is None:
                semester = self.semester_repository.get_active_by_user(user_id=user_id)
                if not semester:
                    raise_not_found("No active semester found.")
                semester_id = semester.id
            semester = self.semester_repository.get_by_id(semester_id)
            if not semester or semester.user_id != user_id:
                raise_not_found("Semester not found.")
            start_date = semester.start_date
            end_date = min(semester.end_date, today)
        else:
            raise_conflict("Invalid summary period. Use today, week, month or semester.")

        return {
            "period": period,
            **self.repository.summary_by_range(user_id=user_id, start_date=start_date, end_date=end_date),
        }

    def get_semester_expense_total(self, user_id: int, semester_id: int):
        semester = self.semester_repository.get_by_id(semester_id)
        if not semester or semester.user_id != user_id:
            raise_not_found("Semester not found.")
        return self.repository.total_spent_for_semester(user_id=user_id, semester_id=semester.id)

    def get_spending_rate(self, user_id: int, semester_id: int, today: date | None = None):
        today = today or date.today()
        semester = self.semester_repository.get_by_id(semester_id)
        if not semester or semester.user_id != user_id:
            raise_not_found("Semester not found.")
        return self.repository.daily_spending_rate(user_id=user_id, semester_id=semester_id, start_date=semester.start_date, today=today)
