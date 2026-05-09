from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.apps.expenses.models import Expense
from app.apps.expenses.schemas import ExpenseCreate


class ExpenseRepository:
    """Data access for expense records."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, expense_in: ExpenseCreate, user_id: int, semester_id: int) -> Expense:
        expense = Expense(
            user_id=user_id,
            semester_id=semester_id,
            amount=expense_in.amount,
            category=expense_in.category.value,
            note=expense_in.note,
            timestamp=expense_in.timestamp or datetime.utcnow(),
            location=expense_in.location,
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def list_by_user(self, user_id: int, semester_id: int | None = None):
        query = self.db.query(Expense).filter(Expense.user_id == user_id)
        if semester_id is not None:
            query = query.filter(Expense.semester_id == semester_id)
        return query.order_by(Expense.timestamp.desc()).all()

    def list_by_date_range(self, user_id: int, start_date: date, end_date: date):
        return (
            self.db.query(Expense)
            .filter(
                Expense.user_id == user_id,
                func.date(Expense.timestamp) >= start_date,
                func.date(Expense.timestamp) <= end_date,
            )
            .order_by(Expense.timestamp.desc())
            .all()
        )

    def summary_by_range(self, user_id: int, start_date: date, end_date: date):
        expenses = self.list_by_date_range(user_id=user_id, start_date=start_date, end_date=end_date)
        total = sum(expense.amount for expense in expenses)
        categories: dict[str, float] = {}
        for expense in expenses:
            categories[expense.category] = categories.get(expense.category, 0.0) + expense.amount
        breakdown = {category: round((amount / total) * 100, 1) if total else 0.0 for category, amount in categories.items()}
        return {
            "total": round(total, 2),
            "categories": categories,
            "breakdown": breakdown,
            "expense_count": len(expenses),
        }

    def total_spent_for_semester(self, user_id: int, semester_id: int):
        total = self.db.query(func.coalesce(func.sum(Expense.amount), 0.0)).filter(
            Expense.user_id == user_id,
            Expense.semester_id == semester_id,
        ).scalar()
        return float(total or 0.0)

    def daily_spending_rate(self, user_id: int, semester_id: int, start_date: date, today: date):
        total = self.total_spent_for_semester(user_id=user_id, semester_id=semester_id)
        elapsed_days = max((today - start_date).days + 1, 1)
        return total / elapsed_days
