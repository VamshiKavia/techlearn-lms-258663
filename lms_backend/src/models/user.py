from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration."""
    admin = "admin"
    instructor = "instructor"
    student = "student"


class UserBase(BaseModel):
    """Shared properties for user entities."""
    email: EmailStr = Field(..., description="User email")
    role: UserRole = Field(..., description="User role")


class UserCreate(UserBase):
    """Payload to create a user (placeholder for future)."""
    pass


class UserOut(UserBase):
    """User response model."""
    id: str = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")
