from datetime import date, timedelta

from app.apps.budget.schemas import DailyLimitResponse
from app.apps.debts.repository import DebtRepository
from app.apps.expenses.repository import ExpenseRepository
from app.apps.pockets.repository import PocketRepository
from app.apps.semesters.repository import SemesterRepository
from app.shared.exceptions import raise_not_found


class BudgetService:
    """Budget calculations for daily spending guidance."""

    def __init__(
        self,
        semester_repository: SemesterRepository,
        expense_repository: ExpenseRepository,
        pocket_repository: PocketRepository,
        debt_repository: DebtRepository,
    ) -> None:
        self.semester_repository = semester_repository
        self.expense_repository = expense_repository
        self.pocket_repository = pocket_repository
        self.debt_repository = debt_repository

    def get_daily_limit(self, user_id: int) -> DailyLimitResponse:
        semester = self.semester_repository.get_active_by_user(user_id=user_id)
        if not semester:
            raise_not_found("No active semester found. Activate a semester before requesting budget guidance.")

        today = date.today()
        total_available = semester.expected_helb_amount
        protected_balance = sum(
            pocket.current_balance
            for pocket in self.pocket_repository.list_by_user(user_id=user_id, semester_id=semester.id)
        )
        total_debt = self.debt_repository.remaining_debt(user_id=user_id)
        total_spent = self.expense_repository.total_spent_for_semester(user_id=user_id, semester_id=semester.id)

        remaining_balance = max(total_available - protected_balance - total_debt - total_spent, 0.0)
        remaining_days = max((semester.end_date - today).days + 1, 0)
        recommended_daily_limit = round(remaining_balance / remaining_days, 2) if remaining_days else 0.0

        actual_daily_rate = total_spent / max((today - semester.start_date).days + 1, 1)
        if actual_daily_rate > 0:
            projected_runout_days = remaining_balance / actual_daily_rate
            projected_runout_date = today + timedelta(days=int(projected_runout_days))
        else:
            projected_runout_date = semester.end_date

        if projected_runout_date < semester.end_date:
            health_status = "danger" if projected_runout_date <= semester.end_date - timedelta(days=7) else "warning"
        else:
            health_status = "healthy"

        return DailyLimitResponse(
            remaining_balance=round(remaining_balance, 2),
            remaining_days=remaining_days,
            recommended_daily_limit=recommended_daily_limit,
            projected_runout_date=projected_runout_date,
            budget_health_status=health_status,
        )
