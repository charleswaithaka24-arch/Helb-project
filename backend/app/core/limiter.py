from slowapi import Limiter
from slowapi.util import get_remote_address
import redis.asyncio as redis
from jose import jwt, JWTError

from app.core.config import config

# Initialize Redis client
redis_client = redis.from_url(config.redis_url)

def get_user_id(request):
    """
    Extract user ID from request to identify the student.
    Uses the JWT sub (email) if available, otherwise falls back to IP address.
    """
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        try:
            payload = jwt.decode(token.split(" ")[1], config.secret_key, algorithms=["HS256"])
            sub = payload.get("sub")
            if sub:
                return sub
        except JWTError:
            pass
    return get_remote_address(request)

# Configure the SlowAPI Limiter to use Redis
limiter = Limiter(
    key_func=get_user_id,
    storage_uri=config.redis_url
)
