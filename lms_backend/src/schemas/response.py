from typing import Any, Optional

from pydantic import BaseModel, Field


class ResponseEnvelope(BaseModel):
    """Standard response envelope for successful responses."""
    status: str = Field(default="ok", description="Status indicator")
    message: str = Field(default="success", description="Status message")
    data: Optional[Any] = Field(default=None, description="Payload")
    timestamp: Optional[str] = Field(default=None, description="Server timestamp (ISO8601)")
