"""
User API endpoints.

Defines all routes for user-related operations.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Create a new user.

    Args:
        user: User data to create.
        db: Database session (injected).

    Returns:
        UserResponse: Created user.

    Raises:
        HTTPException: 400 if username already exists.
    """
    existing_user = db.query(User).filter(
        User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    db_user = User(
        id=str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        hashed_password=user.password,  # TODO: Hash this in production!
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Get a specific user by ID.

    Args:
        user_id: ID of the user to retrieve.
        db: Database session (injected).

    Returns:
        UserResponse: User details.

    Raises:
        HTTPException: 404 if user not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
