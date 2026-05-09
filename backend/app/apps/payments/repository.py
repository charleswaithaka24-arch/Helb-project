from sqlalchemy.orm import Session

from app.apps.payments.models import Payment
from app.apps.payments.schemas import PaymentCreate


class PaymentRepository:
    """Database access layer for payment entities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, payment_id: int) -> Payment | None:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def create(self, payment_in: PaymentCreate) -> Payment:
        payment = Payment(amount=payment_in.amount, status="pending")
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
