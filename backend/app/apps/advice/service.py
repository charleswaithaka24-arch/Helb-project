from datetime import date

from app.apps.advice.repository import AdviceRepository
from app.apps.expenses.repository import ExpenseRepository
from app.apps.semesters.repository import SemesterRepository


class AdviceService:
    """Rule-based advice generator for spending behavior."""

    def __init__(
        self,
        repository: AdviceRepository,
        expense_repository: ExpenseRepository,
        semester_repository: SemesterRepository,
    ) -> None:
        self.repository = repository
        self.expense_repository = expense_repository
        self.semester_repository = semester_repository

    def list_advice(self, user_id: int):
        return self.repository.list_by_user(user_id=user_id)

    def generate_advice(self, user_id: int, today: date | None = None):
        today = today or date.today()
        semester = self.semester_repository.get_active_by_user(user_id=user_id)
        if not semester:
            return []

        must_generate = []
        total_spent = self.expense_repository.total_spent_for_semester(user_id=user_id, semester_id=semester.id)
        categories = self.expense_repository.summary_by_range(
            user_id=user_id,
            start_date=semester.start_date,
            end_date=min(semester.end_date, today),
        )["categories"]

        if total_spent <= 0:
            return []

        if categories.get("entertainment", 0) / total_spent >= 0.2:
            must_generate.append(
                ("Reducing entertainment spending by 20% could extend your budget by several days.", "category")
            )

        if categories.get("food", 0) / total_spent >= 0.25:
            must_generate.append(
                ("Reducing eating out and cooking more at home can lower your food costs.", "food")
            )

        weekend_spend = 0.0
        weekday_spend = 0.0
        expenses = self.expense_repository.list_by_user(user_id=user_id, semester_id=semester.id)
        for expense in expenses:
            if expense.timestamp.weekday() >= 5:
                weekend_spend += expense.amount
            else:
                weekday_spend += expense.amount

        if weekend_spend > weekday_spend:
            must_generate.append(
                ("You spend more over weekends. Planning weekday meals and transport can help you save.", "pattern")
            )

        if not must_generate:
            must_generate.append(
                ("Your spending pattern looks balanced today. Keep tracking expenses to stay on course.", "stable")
            )

        created = []
        for message, source in must_generate:
            created.append(self.repository.create(user_id=user_id, message=message, source=source))
        return created
