# app/internals/user.py

from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()
