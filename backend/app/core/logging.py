import sys

from loguru import logger  # type: ignore[import]

# Remove the default Loguru handler so we can customize output sinks.
logger.remove()

# Console logging
logger.add(
    sys.stderr,
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
)

# File logging with rotation at 10 MB per file.
logger.add(
    "app_logs.log",
    level="INFO",
    rotation="10 MB",
    retention="10 days",
    backtrace=True,
    diagnose=True,
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
