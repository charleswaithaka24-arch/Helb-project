from datetime import datetime


def timestamp() -> str:
    """Return a consistent timestamp string for logging and debugging."""
    return datetime.utcnow().isoformat() + "Z"
