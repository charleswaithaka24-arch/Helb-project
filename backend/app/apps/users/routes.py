from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.apps.users.providers import get_user_service
from app.apps.users.schemas import LoginRequest, UserCreate, UserResponse
from app.apps.users.service import UserService
from app.core.database import get_db
from app.core.security import create_access_token, get_current_user, verify_password
from app.apps.users.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Create a new user using thin routing and injected services."""
    return service.create_user(user_in)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> UserResponse:
    """Retrieve a user by ID using business logic from the service layer."""
    return service.get_user(user_id)


@router.post("/token")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
