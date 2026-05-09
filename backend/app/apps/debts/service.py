from app.apps.debts.repository import DebtRepository
from app.apps.debts.schemas import DebtCreate, DebtPayRequest
from app.apps.semesters.repository import SemesterRepository
from app.shared.exceptions import raise_conflict, raise_not_found


class DebtService:
    """Business logic for debt creation, repayment and summary."""

    def __init__(self, repository: DebtRepository, semester_repository: SemesterRepository) -> None:
        self.repository = repository
        self.semester_repository = semester_repository

    def create_debt(self, user_id: int, debt_in: DebtCreate):
        active_semester = self.semester_repository.get_active_by_user(user_id=user_id)
        if not active_semester:
            raise_not_found("Activate a semester before adding debts.")
        return self.repository.create(user_id=user_id, debt_in=debt_in)

    def list_debts(self, user_id: int):
        return self.repository.list_by_user(user_id=user_id)

    def pay_debt(self, user_id: int, debt_id: int, pay_request: DebtPayRequest):
        debt = self.repository.get_by_id(debt_id)
        if not debt or debt.user_id != user_id:
            raise_not_found("Debt not found.")
        if debt.status == "paid":
            raise_conflict("This debt is already paid.")
        if pay_request.amount > debt.remaining_amount:
            raise_conflict("Payment exceeds remaining debt amount.")
        return self.repository.pay(debt=debt, amount=pay_request.amount)

    def debt_summary(self, user_id: int):
        total = self.repository.total_debt(user_id=user_id)
        remaining = self.repository.remaining_debt(user_id=user_id)
        active_debts = len([debt for debt in self.repository.list_by_user(user_id=user_id) if debt.status != "paid"])
        active_semester = self.semester_repository.get_active_by_user(user_id=user_id)
        if not active_semester:
            raise_not_found("Activate a semester before checking debt summary.")
        debt_to_income_ratio = (remaining / active_semester.expected_helb_amount) if active_semester.expected_helb_amount else 0.0
        return {
            "total_debt": round(total, 2),
            "remaining_debt": round(remaining, 2),
            "debt_to_income_ratio": round(debt_to_income_ratio, 2),
            "active_debts": active_debts,
        }
