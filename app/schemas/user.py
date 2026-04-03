from pydantic import BaseModel, EmailStr
from app.utils import UserRole
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.SALES

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True