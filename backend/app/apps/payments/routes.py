from fastapi import APIRouter, Depends, status

from app.apps.payments.providers import get_payment_service
from app.apps.payments.schemas import PaymentCreate, PaymentResponse
from app.apps.payments.service import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment_in: PaymentCreate,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    """Create a new payment record."""
    return service.create_payment(payment_in)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, service: PaymentService = Depends(get_payment_service)) -> PaymentResponse:
    """Retrieve payment information by ID."""
    return service.get_payment(payment_id)
