from app.apps.payments.repository import PaymentRepository
from app.apps.payments.schemas import PaymentCreate
from app.shared.exceptions import raise_not_found


class PaymentService:
    """Business logic layer for payment operations."""

    def __init__(self, repository: PaymentRepository) -> None:
        self.repository = repository

    def create_payment(self, payment_in: PaymentCreate):
        return self.repository.create(payment_in=payment_in)

    def get_payment(self, payment_id: int):
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            raise_not_found("Payment not found.")
        return payment
