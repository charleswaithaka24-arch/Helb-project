import json
from typing import Optional

from fastapi import Header, Request, HTTPException
from app.core.limiter import redis_client, get_user_id

class IdempotencyHitException(Exception):
    """Raised when an idempotency key is hit and a cached response exists."""
    def __init__(self, cached_data: dict):
        self.cached_data = cached_data

async def verify_idempotency(
    request: Request,
    x_idempotency_key: Optional[str] = Header(None)
):
    """
    Dependency to check for an idempotency key.
    If the key is found and processing, returns 409 Conflict.
    If the key is found and completed, raises IdempotencyHitException to return cached result.
    If not found, marks it as processing and returns the redis_key to be used by the endpoint to save the result.
    """
    if not x_idempotency_key:
        return None
        
    user_id = get_user_id(request)
    redis_key = f"idempotency:{user_id}:{x_idempotency_key}"
    
    cached_response = await redis_client.get(redis_key)
    
    if cached_response:
        if cached_response == b"processing":
            raise HTTPException(status_code=409, detail="Request is already being processed")
        
        # If it's not processing, it's a cached JSON response
        data = json.loads(cached_response.decode("utf-8"))
        raise IdempotencyHitException(cached_data=data)

    # Mark as processing (valid for 24 hours to prevent stuck states if something crashes, though usually shorter is better for 'processing')
    # Let's set processing to 60 seconds.
    await redis_client.setex(redis_key, 60, "processing")
    
    return redis_key

async def save_idempotency_response(redis_key: Optional[str], response_data: dict):
    """
    Save the final response data to Redis for the given idempotency key.
    Valid for 24 hours.
    """
    if redis_key:
        await redis_client.setex(redis_key, 86400, json.dumps(response_data))
