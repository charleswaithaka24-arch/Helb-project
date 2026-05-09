from fastapi import APIRouter, Depends, status

from app.apps.semesters.providers import get_semester_service
from app.apps.semesters.schemas import SemesterCreate, SemesterResponse
from app.apps.semesters.service import SemesterService
from app.core.security import get_current_user

router = APIRouter(prefix="/semesters", tags=["semesters"])


@router.post("/", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED)
def create_semester(
    semester_in: SemesterCreate,
    current_user=Depends(get_current_user),
    service: SemesterService = Depends(get_semester_service),
) -> SemesterResponse:
    return service.create_semester(current_user.id, semester_in)


@router.get("/", response_model=list[SemesterResponse])
def list_semesters(
    current_user=Depends(get_current_user),
    service: SemesterService = Depends(get_semester_service),
) -> list[SemesterResponse]:
    return service.list_semesters(current_user.id)


@router.post("/{semester_id}/activate", response_model=SemesterResponse)
def activate_semester(
    semester_id: int,
    current_user=Depends(get_current_user),
    service: SemesterService = Depends(get_semester_service),
) -> SemesterResponse:
    return service.activate_semester(semester_id=semester_id, user_id=current_user.id)
