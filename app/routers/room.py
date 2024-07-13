from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.internals.crud import user as crud_user
from app.schemas import UserCreate, User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db=db, user=user)

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_user.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
