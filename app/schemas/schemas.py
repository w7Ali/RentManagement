from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class RoomBase(BaseModel):
    type: str
    member_size: int
    work_name: Optional[str] = None
    work_count: Optional[int] = None

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

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

class PaymentBase(BaseModel):
    date: date
    amount: int
    status: str
    balance: int
    electricity_usage: int

class PaymentCreate(PaymentBase):
    user_id: int

class Payment(PaymentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
