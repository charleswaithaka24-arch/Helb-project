from sqlalchemy.orm import Session

from app.apps.bookings.models import Booking
from app.apps.bookings.schemas import BookingCreate


class BookingRepository:
    """Database access layer for booking/loan entities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, booking_id: int) -> Booking | None:
        return self.db.query(Booking).filter(Booking.id == booking_id).first()

    def create(self, booking_in: BookingCreate) -> Booking:
        booking = Booking(
            customer_name=booking_in.customer_name,
            phone_number=booking_in.phone_number,
            loan_amount=booking_in.loan_amount,
            status="pending"
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def approve_loan(self, booking_id: int) -> Booking | None:
        booking = self.get_by_id(booking_id)
        if booking and booking.status == "pending":
            booking.status = "approved"
            self.db.commit()
            self.db.refresh(booking)
            return booking
        return None
