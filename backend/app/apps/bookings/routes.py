from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from app.apps.bookings.providers import get_booking_service
from app.apps.bookings.schemas import BookingCreate, BookingResponse, LoanApprovalRequest
from app.apps.bookings.service import BookingService
from app.core.database import get_db
from app.core.security import get_current_admin
from app.apps.bookings.models import Booking

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    service: BookingService = Depends(get_booking_service),
) -> BookingResponse:
    """Create a new loan application."""
    return service.create_booking(booking_in)


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, service: BookingService = Depends(get_booking_service)) -> BookingResponse:
    """Retrieve booking/loan details by ID."""
    return service.get_booking(booking_id)


@router.post("/approve-loan", response_model=BookingResponse, status_code=status.HTTP_200_OK)
def approve_loan(
    approval_request: LoanApprovalRequest,
    background_tasks: BackgroundTasks,
    service: BookingService = Depends(get_booking_service),
) -> BookingResponse:
    """Approve a loan application and send SMS notification asynchronously."""
    return service.approve_loan(approval_request.booking_id, background_tasks)


@router.get("/admin/all-loans", response_model=list[BookingResponse])
def get_all_loans(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    """Admin only: Get all loan applications."""
    return db.query(Booking).all()
