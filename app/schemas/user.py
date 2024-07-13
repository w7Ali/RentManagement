from pydantic import BaseModel
from typing import List
from .room import Room

class UserBase(BaseModel):
    name: str
    phone: str
    old_address: str
    adharcard: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    rooms: List[Room] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "phone": "1234567890",
                "old_address": "123 Old St, Old City",
                "adharcard": "123456789012",
                "rooms": [
                    {
                        "id": 1,
                        "owner_id": 1,
                        "type": "family_only",
                        "member_size": 4,
                        "work_name": "Software Development",
                        "work_count": 3
                    }
                ]
            }
        }
