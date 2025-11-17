from pydantic import BaseModel, Field


class IDModel(BaseModel):
    """Standard ID model."""
    id: str = Field(..., description="Resource identifier")
