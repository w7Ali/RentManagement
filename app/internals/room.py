# app/internals/room.py

from sqlalchemy.orm import Session
from app.models.room import RoomModel
from app.schemas.room import RoomCreate

def create_room(db: Session, room: RoomCreate, user_id: int):
    db_room = RoomModel(**room.dict(), user_id=user_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_rooms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RoomModel).offset(skip).limit(limit).all()

def get_room(db: Session, room_id: int):
    return db.query(RoomModel).filter(RoomModel.id == room_id).first()
