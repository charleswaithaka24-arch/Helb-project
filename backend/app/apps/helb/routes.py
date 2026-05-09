from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import Dict, Any

from app.core.limiter import limiter
from app.core.idempotency import verify_idempotency, save_idempotency_response

router = APIRouter(prefix="/helb", tags=["HELB"])

@router.get("/status")
@limiter.limit("5/minute")
async def get_status(request: Request) -> Dict[str, Any]:
    """
    Get the student's HELB loan status.
    Rate limited to 5 requests per minute per student.
    """
    return {"status": "success", "data": {"loan_status": "approved", "amount_due": 15000}}


class DisburseRequest(BaseModel):
    amount: float
    semester_id: str

@router.post("/disburse")
async def disburse_funds(
    request: Request,
    payload: DisburseRequest,
    idempotency_key: str = Depends(verify_idempotency)
) -> Dict[str, Any]:
    """
    Disburse funds to a student for a specific semester.
    Idempotent operation based on X-Idempotency-Key.
    """
    # Simulate processing logic
    response_data = {
        "status": "success", 
        "message": f"Successfully disbursed {payload.amount} for semester {payload.semester_id}"
    }
    
    # Save the response if an idempotency key was provided
    if idempotency_key:
        await save_idempotency_response(idempotency_key, response_data)
        
    return response_data
