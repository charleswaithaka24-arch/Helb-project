from fastapi import APIRouter, Depends, Path, status

from app.apps.pockets.providers import get_pocket_service
from app.apps.pockets.schemas import (
    PocketAllocateRequest,
    PocketCreate,
    PocketLockResponse,
    PocketResponse,
    PocketWithdrawRequest,
)
from app.apps.pockets.service import PocketService
from app.core.security import get_current_user

router = APIRouter(prefix="/pockets", tags=["pockets"])


@router.post("/", response_model=PocketResponse, status_code=status.HTTP_201_CREATED)
def create_pocket(
    pocket_in: PocketCreate,
    semester_id: int,
    current_user=Depends(get_current_user),
    service: PocketService = Depends(get_pocket_service),
) -> PocketResponse:
    return service.create_pocket(current_user.id, semester_id=semester_id, pocket_in=pocket_in)


@router.get("/", response_model=list[PocketResponse])
def list_pockets(
    semester_id: int | None = None,
    current_user=Depends(get_current_user),
    service: PocketService = Depends(get_pocket_service),
) -> list[PocketResponse]:
    return service.list_pockets(current_user.id, semester_id=semester_id)


@router.post("/{pocket_id}/allocate", response_model=PocketResponse)
def allocate_to_pocket(
    request: PocketAllocateRequest,
    pocket_id: int = Path(..., ge=1),
    current_user=Depends(get_current_user),
    service: PocketService = Depends(get_pocket_service),
) -> PocketResponse:
    return service.allocate(current_user.id, pocket_id=pocket_id, allocation=request)


@router.post("/{pocket_id}/withdraw", response_model=PocketResponse)
def withdraw_from_pocket(
    request: PocketWithdrawRequest,
    pocket_id: int = Path(..., ge=1),
    current_user=Depends(get_current_user),
    service: PocketService = Depends(get_pocket_service),
) -> PocketResponse:
    return service.withdraw(current_user.id, pocket_id=pocket_id, withdrawal=request)


@router.post("/{pocket_id}/lock", response_model=PocketLockResponse)
def lock_pocket(
    pocket_id: int = Path(..., ge=1),
    current_user=Depends(get_current_user),
    service: PocketService = Depends(get_pocket_service),
) -> PocketLockResponse:
    return service.lock_pocket(current_user.id, pocket_id=pocket_id)
