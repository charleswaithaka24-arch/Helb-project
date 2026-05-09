from sqlalchemy.orm import Session

from app.apps.advice.models import AdviceLog


class AdviceRepository:
    """Data access layer for advice logging."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user_id: int, message: str, source: str) -> AdviceLog:
        advice = AdviceLog(user_id=user_id, message=message, source=source)
        self.db.add(advice)
        self.db.commit()
        self.db.refresh(advice)
        return advice

    def list_by_user(self, user_id: int) -> list[AdviceLog]:
        return self.db.query(AdviceLog).filter(AdviceLog.user_id == user_id).order_by(AdviceLog.created_at.desc()).all()
