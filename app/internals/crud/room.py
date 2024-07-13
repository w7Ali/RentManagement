from sqlalchemy.orm import Session
from app.models import Room
from app.schemas import RoomCreate

def create_room(db: Session, room: RoomCreate, user_id: int):
    db_room = Room(**room.dict(), user_id=user_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_rooms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Room).offset(skip).limit(limit).all()

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()
