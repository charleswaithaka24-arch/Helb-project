from fastapi import BackgroundTasks

from app.apps.bookings.repository import BookingRepository
from app.apps.bookings.schemas import BookingCreate
from app.core.sms import sms_service
from app.shared.exceptions import raise_not_found


class BookingService:
    """Business logic layer for booking/loan operations."""

    def __init__(self, repository: BookingRepository) -> None:
        self.repository = repository

    def create_booking(self, booking_in: BookingCreate):
        return self.repository.create(booking_in=booking_in)

    def get_booking(self, booking_id: int):
        booking = self.repository.get_by_id(booking_id)
        if not booking:
            raise_not_found("Booking not found.")
        return booking

    def approve_loan(self, booking_id: int, background_tasks: BackgroundTasks):
        booking = self.repository.approve_loan(booking_id)
        if not booking:
            raise_not_found("Booking not found or already approved.")

        # Send SMS notification asynchronously
        background_tasks.add_task(
            sms_service.send_loan_approval_sms,
            booking.phone_number,
            booking.customer_name
        )

        return booking
