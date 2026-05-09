from app.apps.users.repository import UserRepository
from app.apps.users.schemas import UserCreate
from app.core.security import hash_password
from app.shared.exceptions import raise_conflict, raise_not_found


class UserService:
    """Business logic layer for user operations."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, user_in: UserCreate):
        if self.repository.get_by_email(user_in.email):
            raise_conflict("A user with this email already exists.")

        hashed_password = hash_password(user_in.password)
        return self.repository.create(user_in=user_in, hashed_password=hashed_password)

    def get_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise_not_found("User not found.")
        return user
