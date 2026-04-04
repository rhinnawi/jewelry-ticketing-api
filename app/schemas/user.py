"""
User request/response schemas.

Defines Pydantic models for user-related API operations.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.utils import UserRole


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username: Unique username.
        email: Unique email address.
        password: User password (will be hashed).
        role: User role (defaults to SALES).
    """

    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.SALES


class UserResponse(BaseModel):
    """
    Schema for user API responses.

    Attributes:
        id: User identifier.
        username: Username.
        email: Email address.
        role: User role.
        created_at: Timestamp of creation.
    """

    id: str
    username: str
    email: str
    role: UserRole
    created_at: datetime

    model_config = {"from_attributes": True}
