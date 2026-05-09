from fastapi import Depends
from sqlalchemy.orm import Session

from app.apps.payments.repository import PaymentRepository
from app.apps.payments.service import PaymentService
from app.core.database import get_db


def get_payment_repository(db: Session = Depends(get_db)) -> PaymentRepository:
    return PaymentRepository(db=db)


def get_payment_service(repository: PaymentRepository = Depends(get_payment_repository)) -> PaymentService:
    return PaymentService(repository=repository)
