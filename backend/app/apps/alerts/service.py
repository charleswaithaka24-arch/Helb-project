from datetime import date

from app.apps.alerts.repository import AlertRepository
from app.apps.debts.repository import DebtRepository
from app.apps.expenses.repository import ExpenseRepository
from app.apps.pockets.repository import PocketRepository
from app.apps.semesters.repository import SemesterRepository


class AlertService:
    """Generate predictive spending alerts based on user behavior."""

    def __init__(
        self,
        repository: AlertRepository,
        expense_repository: ExpenseRepository,
        semester_repository: SemesterRepository,
        pocket_repository: PocketRepository,
        debt_repository: DebtRepository,
    ) -> None:
        self.repository = repository
        self.expense_repository = expense_repository
        self.semester_repository = semester_repository
        self.pocket_repository = pocket_repository
        self.debt_repository = debt_repository

    def list_alerts(self, user_id: int):
        return self.repository.list_by_user(user_id=user_id)

    def evaluate_spending(self, user_id: int, today: date | None = None):
        today = today or date.today()
        semester = self.semester_repository.get_active_by_user(user_id=user_id)
        if not semester:
            return []

        spent = self.expense_repository.total_spent_for_semester(user_id=user_id, semester_id=semester.id)
        protected_balance = sum(
            pocket.current_balance
            for pocket in self.pocket_repository.list_by_user(user_id=user_id, semester_id=semester.id)
        )
        days_elapsed = max((today - semester.start_date).days + 1, 1)
        projected_daily_spend = spent / days_elapsed
        remaining_budget = semester.expected_helb_amount - protected_balance - spent - self.debt_repository.remaining_debt(user_id=user_id)
        remaining_days = max((semester.end_date - today).days + 1, 0)

        if remaining_days == 0:
            return []

        if projected_daily_spend <= 0 or remaining_budget <= 0:
            message = "Your funds are at risk. Review your semester budget immediately."
            return [self.repository.create(user_id, "danger", message, "runout")]  # type: ignore[arg-type]

        projected_runout_days = remaining_budget / projected_daily_spend
        runout_gap = remaining_days - projected_runout_days
        if runout_gap <= 0:
            message = f"Your current spending pace is safe for the semester. Keep tracking expenses."
            return [self.repository.create(user_id, "info", message, "safe")]

        if runout_gap < 7:
            message = f"If spending continues at this rate, your money may run out {int(runout_gap)} days early."
            return [self.repository.create(user_id, "warning", message, "warning")]

        message = f"Your money may run out {int(runout_gap)} days before semester end if spending pace doesn't slow."
        return [self.repository.create(user_id, "danger", message, "danger")]  # type: ignore[arg-type]
