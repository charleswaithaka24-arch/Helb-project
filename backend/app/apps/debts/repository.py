from sqlalchemy import func
from sqlalchemy.orm import Session

from app.apps.debts.models import Debt
from app.apps.debts.schemas import DebtCreate


class DebtRepository:
    """Database access layer for debt entities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, debt_id: int) -> Debt | None:
        return self.db.query(Debt).filter(Debt.id == debt_id).first()

    def list_by_user(self, user_id: int) -> list[Debt]:
        return self.db.query(Debt).filter(Debt.user_id == user_id).order_by(Debt.due_date).all()

    def create(self, user_id: int, debt_in: DebtCreate) -> Debt:
        debt = Debt(
            user_id=user_id,
            creditor_name=debt_in.creditor_name,
            original_amount=debt_in.original_amount,
            remaining_amount=debt_in.original_amount,
            interest_rate=debt_in.interest_rate,
            due_date=debt_in.due_date,
        )
        self.db.add(debt)
        self.db.commit()
        self.db.refresh(debt)
        return debt

    def pay(self, debt: Debt, amount: float) -> Debt:
        debt.remaining_amount -= amount
        if debt.remaining_amount <= 0:
            debt.remaining_amount = 0.0
            debt.status = "paid"
        self.db.commit()
        self.db.refresh(debt)
        return debt

    def total_debt(self, user_id: int) -> float:
        total = self.db.query(func.coalesce(func.sum(Debt.original_amount), 0.0)).filter(Debt.user_id == user_id).scalar()
        return float(total or 0.0)

    def remaining_debt(self, user_id: int) -> float:
        total = self.db.query(func.coalesce(func.sum(Debt.remaining_amount), 0.0)).filter(Debt.user_id == user_id).scalar()
        return float(total or 0.0)
