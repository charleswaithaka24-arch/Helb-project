from sqlalchemy.orm import Session

from app.apps.alerts.models import Alert


class AlertRepository:
    """Data access layer for alert entities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_user(self, user_id: int) -> list[Alert]:
        return self.db.query(Alert).filter(Alert.user_id == user_id).order_by(Alert.created_at.desc()).all()

    def create(self, user_id: int, level: str, message: str, context: str | None = None) -> Alert:
        alert = Alert(user_id=user_id, level=level, message=message, context=context)
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert
