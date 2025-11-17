from datetime import datetime

from fastapi import APIRouter

from src.core.errors import api_envelope
from src.core.config import get_settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Returns service health, environment, and version information.",
    responses={200: {"description": "Service healthy"}},
)
# PUBLIC_INTERFACE
async def health():
    """Health endpoint providing status and basic service info.

    Returns:
        dict: response envelope with status and service info.
    """
    settings = get_settings()
    return api_envelope(
        {
            "service": "TechLearn LMS API",
            "env": settings.APP_ENV,
            "version": "0.1.0",
            "time": datetime.utcnow().isoformat(),
        }
    )
