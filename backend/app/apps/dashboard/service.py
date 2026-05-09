from datetime import date, datetime, timedelta

from app.apps.dashboard.schemas import DashboardResponse, CategoryBreakdownItem, WeeklyTrendPoint
from app.apps.debts.repository import DebtRepository
from app.apps.expenses.repository import ExpenseRepository
from app.apps.pockets.repository import PocketRepository
from app.apps.semesters.repository import SemesterRepository


class DashboardService:
    """Business logic for dashboard aggregation."""

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

    def get_dashboard(self, user_id: int):
        semester = self.semester_repository.get_active_by_user(user_id=user_id)
        if not semester:
            raise ValueError("No active semester found. Activate a semester to view the dashboard.")

        today = date.today()
        total_expenses = self.expense_repository.total_spent_for_semester(user_id=user_id, semester_id=semester.id)
        protected_funds = sum(pocket.current_balance for pocket in self.pocket_repository.list_by_user(user_id=user_id, semester_id=semester.id))
        remaining_budget = max(semester.expected_helb_amount - protected_funds - total_expenses - self.debt_repository.remaining_debt(user_id=user_id), 0.0)
        remaining_days = max((semester.end_date - today).days + 1, 1)
        daily_safe_limit = round(remaining_budget / remaining_days, 2)
        projected_survival_date = today + timedelta(days=(remaining_budget / (total_expenses / max((today - semester.start_date).days + 1, 1))) if total_expenses > 0 else remaining_days)

        category_summary = self.expense_repository.summary_by_range(
            user_id=user_id,
            start_date=semester.start_date,
            end_date=min(semester.end_date, today),
        )
        breakdown = [
            CategoryBreakdownItem(category=category, amount=amount, percentage=percentage)
            for category, amount in category_summary["categories"].items()
            for percentage in [category_summary["breakdown"][category]]
        ]

        weekly_trend = []
        for offset in range(6, -1, -1):
            point_date = today - timedelta(days=offset)
            day_total = sum(
                expense.amount
                for expense in self.expense_repository.list_by_date_range(user_id=user_id, start_date=point_date, end_date=point_date)
            )
            weekly_trend.append(WeeklyTrendPoint(date=point_date, total=round(day_total, 2)))

        return DashboardResponse(
            total_balance=round(semester.expected_helb_amount, 2),
            protected_funds=round(protected_funds, 2),
            total_expenses=round(total_expenses, 2),
            daily_safe_limit=daily_safe_limit,
            projected_survival_date=projected_survival_date,
            debt_status={
                "remaining_debt": round(self.debt_repository.remaining_debt(user_id=user_id), 2),
                "debt_to_income_ratio": round(
                    self.debt_repository.remaining_debt(user_id=user_id) / semester.expected_helb_amount
                    if semester.expected_helb_amount else 0.0,
                    2,
                ),
            },
            category_breakdown=breakdown,
            weekly_spending_trend=weekly_trend,
        )
