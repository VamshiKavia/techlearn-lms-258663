from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    """Shared course fields."""
    title: str = Field(..., description="Course title", min_length=1, max_length=200)
    description: str = Field(..., description="Course description", min_length=1)
    category: str = Field(..., description="Course category", min_length=1, max_length=100)
    published: bool = Field(default=False, description="Published flag")


class CourseCreate(CourseBase):
    """Course creation payload."""
    # TODO: enforce role-based permissions (instructor/admin)
    pass


class CourseOut(CourseBase):
    """Course response model."""
    id: str = Field(..., description="Course ID")
    created_by: Optional[str] = Field(None, description="Creator user id (placeholder)")
    created_at: datetime = Field(..., description="Creation timestamp")
