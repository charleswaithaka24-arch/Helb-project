from fastapi import Depends
from sqlalchemy.orm import Session

from app.apps.users.repository import UserRepository
from app.apps.users.service import UserService
from app.core.database import get_db


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)
