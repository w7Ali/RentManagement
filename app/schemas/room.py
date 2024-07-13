from pydantic import BaseModel, validator
from typing import Literal, Optional
from app.schemas.CONSTANT import ROOM_TYPES

class RoomBase(BaseModel):
    type: Literal["family_only", "boys_only", "girls_only", "work"]
    member_size: int
    work_name: Optional[str] = None
    work_count: Optional[int] = None

    @validator("type")
    def check_room_type(cls, value):
        if value not in ROOM_TYPES:
            raise ValueError(f"Invalid room type: {value}")
        return value

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "owner_id": 1,
                "type": "family_only",
                "member_size": 4,
                "work_name": "Software Development",
                "work_count": 3
            }
        }
