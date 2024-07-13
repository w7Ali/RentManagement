from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.internals.crud import user as crud_user
from app.schemas import UserCreate, User, UserBase
from app.database.db import get_db
router = APIRouter()



@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (UserCreate): User details to create.

    Returns:
        UserBase: Created user details.
    """
    return crud_user.create_user(db=db, user=user)

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of users with optional pagination.

    Args:
        skip (int, optional): Number of records to skip (default is 0).
        limit (int, optional): Maximum number of records to retrieve (default is 10).

    Returns:
        List[UserBase]: List of users.
    """
    return crud_user.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by ID.

    Args:
        user_id (int): ID of the user to retrieve.

    Returns:
        UserBase: Retrieved user details.

    Raises:
        HTTPException: 404 if user with the given ID does not exist.
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
