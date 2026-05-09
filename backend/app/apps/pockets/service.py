from app.apps.debts.repository import DebtRepository
from app.apps.expenses.repository import ExpenseRepository
from app.apps.pockets.repository import PocketRepository
from app.apps.pockets.schemas import PocketAllocateRequest, PocketCreate, PocketWithdrawRequest
from app.apps.semesters.repository import SemesterRepository
from app.shared.exceptions import raise_conflict, raise_not_found


class PocketService:
    """Business logic for pocket allocations, withdrawals and protected funds."""

    def __init__(
        self,
        repository: PocketRepository,
        semester_repository: SemesterRepository,
        expense_repository: ExpenseRepository,
        debt_repository: DebtRepository,
    ) -> None:
        self.repository = repository
        self.semester_repository = semester_repository
        self.expense_repository = expense_repository
        self.debt_repository = debt_repository

    def create_pocket(self, user_id: int, semester_id: int, pocket_in: PocketCreate):
        semester = self.semester_repository.get_by_id(semester_id)
        if not semester or semester.user_id != user_id:
            raise_not_found("Semester not found for pocket creation.")
        return self.repository.create(user_id=user_id, semester_id=semester_id, pocket_in=pocket_in)

    def list_pockets(self, user_id: int, semester_id: int | None = None):
        return self.repository.list_by_user(user_id=user_id, semester_id=semester_id)

    def allocate(self, user_id: int, pocket_id: int, allocation: PocketAllocateRequest):
        pocket = self.repository.get_by_id(pocket_id)
        if not pocket or pocket.user_id != user_id:
            raise_not_found("Pocket not found.")

        semester = self.semester_repository.get_by_id(pocket.semester_id)
        if not semester:
            raise_not_found("Associated semester not found.")

        protected_balance = sum(
            p.current_balance
            for p in self.repository.list_by_user(user_id=user_id, semester_id=semester.id)
        )
        total_spent = self.expense_repository.total_spent_for_semester(user_id=user_id, semester_id=semester.id)
        total_debt = self.debt_repository.remaining_debt(user_id=user_id)
        available_balance = max(semester.expected_helb_amount - protected_balance - total_spent - total_debt, 0.0)

        if allocation.amount > available_balance:
            raise_conflict("Allocation exceeds available spendable balance.")

        new_balance = pocket.current_balance + allocation.amount
        pocket = self.repository.update_balance(pocket, new_balance)
        self.repository.create_transaction(
            pocket_id=pocket.id,
            user_id=user_id,
            amount=allocation.amount,
            transaction_type="allocation",
            note=allocation.note,
        )
        return pocket

    def withdraw(self, user_id: int, pocket_id: int, withdrawal: PocketWithdrawRequest):
        pocket = self.repository.get_by_id(pocket_id)
        if not pocket or pocket.user_id != user_id:
            raise_not_found("Pocket not found.")
        if pocket.locked and not withdrawal.emergency_override:
            raise_conflict("Pocket is locked. Use emergency override to withdraw funds.")
        if withdrawal.amount > pocket.current_balance:
            raise_conflict("Cannot withdraw more than pocket balance.")
        new_balance = pocket.current_balance - withdrawal.amount
        pocket = self.repository.update_balance(pocket, new_balance)
        transaction_type = "emergency_withdrawal" if pocket.type == "emergency" else "withdrawal"
        self.repository.create_transaction(
            pocket_id=pocket.id,
            user_id=user_id,
            amount=withdrawal.amount,
            transaction_type=transaction_type,
            note=withdrawal.note,
        )
        return pocket

    def lock_pocket(self, user_id: int, pocket_id: int):
        pocket = self.repository.get_by_id(pocket_id)
        if not pocket or pocket.user_id != user_id:
            raise_not_found("Pocket not found.")
        return self.repository.lock(pocket)
