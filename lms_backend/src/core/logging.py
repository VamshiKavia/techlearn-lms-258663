import logging
import sys
from typing import Optional

from src.core.config import Settings


def configure_logging(settings: Optional[Settings] = None) -> None:
    """Configure application logging, integrating with uvicorn loggers.

    Args:
        settings: Optional settings to include environment context.
    """
    log_level = logging.INFO
    # Root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )
    # Align uvicorn access/error with our formatting
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(logger_name).setLevel(log_level)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger by name.

    Args:
        name: Logger name (usually __name__).

    Returns:
        logging.Logger: logger instance.
    """
    return logging.getLogger(name)
