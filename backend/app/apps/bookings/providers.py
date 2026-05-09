from fastapi import Depends
from sqlalchemy.orm import Session

from app.apps.bookings.repository import BookingRepository
from app.apps.bookings.service import BookingService
from app.core.database import get_db


def get_booking_repository(db: Session = Depends(get_db)) -> BookingRepository:
    return BookingRepository(db=db)


def get_booking_service(repository: BookingRepository = Depends(get_booking_repository)) -> BookingService:
    return BookingService(repository=repository)
