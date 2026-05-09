from sqlalchemy.orm import Session

from app.apps.users.models import User
from app.apps.users.schemas import UserCreate


class UserRepository:
    """Database access layer for user entities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user_in: UserCreate, hashed_password: str) -> User:
        user = User(email=user_in.email, password=hashed_password, role=user_in.role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
