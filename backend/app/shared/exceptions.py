from fastapi import HTTPException, status


class ApplicationError(Exception):
    """Base exception for application-specific errors."""
    pass


def raise_conflict(detail: str) -> None:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def raise_not_found(detail: str) -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
