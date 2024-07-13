# app/routers/rooms.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.internals import room as crud_room
from app.schemas.room import RoomCreate, Room

router = APIRouter()


@router.post("/", response_model=Room)
def create_room(room: RoomCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Create a new room associated with a user.

    Args:
        room (RoomCreate): Room details.
        user_id (int): ID of the user associated with the room.

    Returns:
        Room: Created room details.
    """
    return crud_room.create_room(db=db, room=room, user_id=user_id)

@router.get("/", response_model=List[Room])
def read_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of rooms with optional pagination.

    Args:
        skip (int, optional): Number of records to skip (default is 0).
        limit (int, optional): Maximum number of records to retrieve (default is 10).

    Returns:
        List[Room]: List of rooms.
    """
    return crud_room.get_rooms(db, skip=skip, limit=limit)

@router.get("/{room_id}", response_model=Room)
def read_room(room_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific room by ID.

    Args:
        room_id (int): ID of the room to retrieve.

    Returns:
        Room: Retrieved room details.

    Raises:
        HTTPException: 404 if room with the given ID does not exist.
    """
    db_room = crud_room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room
