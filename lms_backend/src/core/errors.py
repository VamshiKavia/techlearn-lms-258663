from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


class ErrorCode(str, Enum):
    """Standardized error codes for the API."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    BAD_REQUEST = "BAD_REQUEST"


class ApplicationError(Exception):
    """Base exception class for application errors."""

    def __init__(self, message: str, code: ErrorCode, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()


def api_envelope(data: Any = None, message: str = "success") -> Dict[str, Any]:
    """Create a standard API response envelope."""
    return {
        "status": "ok",
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app."""

    @app.exception_handler(ApplicationError)
    async def handle_application_error(_: Request, exc: ApplicationError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "error": {
                    "code": exc.code.value,
                    "message": exc.message,
                    "details": exc.details,
                    "timestamp": exc.timestamp,
                },
            },
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "error": {
                    "code": ErrorCode.BAD_REQUEST.value if exc.status_code < 500 else ErrorCode.INTERNAL_ERROR.value,
                    "message": exc.detail,
                    "timestamp": datetime.utcnow().isoformat(),
                },
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception):
        # Avoid leaking internal details
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": {
                    "code": ErrorCode.INTERNAL_ERROR.value,
                    "message": "An unexpected error occurred.",
                    "timestamp": datetime.utcnow().isoformat(),
                },
            },
        )
