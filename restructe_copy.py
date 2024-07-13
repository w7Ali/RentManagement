# models/payment.py
# from sqlalchemy import Column, Integer, String, Date, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base


# class PaymentModel(Base):
#     __tablename__ = "payments"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     date = Column(Date)
#     amount = Column(Integer)
#     status = Column(String)  # paid, unpaid, partial
#     balance = Column(Integer)
#     electricity_usage = Column(Integer)

#     user = relationship("UserModel")
# models/user.py
# from sqlalchemy import Column, Integer, String, Date, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base
# from app.schemas.CONSTANT import ROOM_TYPES

# class UserModel(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     phone = Column(String, index=True)
#     old_address = Column(String)
#     adharcard = Column(Integer)

#     rooms = relationship("RoomModel", back_populates="owner")

# model/room.py
# from sqlalchemy import Column, Integer, String, Date, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base
# from app.schemas.CONSTANT import ROOM_TYPES


# class RoomModel(Base):
#     __tablename__ = "rooms"
#     id = Column(Integer, primary_key=True, index=True)
#     type = Column(String, nullable=False)
#     member_size = Column(Integer)
#     work_name = Column(String, nullable=True)
#     work_count = Column(Integer, nullable=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("UserModel", back_populates="rooms")

# schemas/payment.py
# from pydantic import BaseModel
# from datetime import date

# class PaymentBase(BaseModel):
#     date: date
#     amount: int
#     status: str
#     balance: int
#     electricity_usage: int

# class PaymentCreate(PaymentBase):
#     user_id: int

# class Payment(PaymentBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True
#         schema_extra = {
#             "example": {
#                 "id": 1,
#                 "user_id": 1,
#                 "date": "2024-07-10",
#                 "amount": 5000,
#                 "status": "paid",
#                 "balance": 0,
#                 "electricity_usage": 150
#             }
#         }
# shcemas/user.py
# from pydantic import BaseModel
# from typing import List
# from .room import Room

# class UserBase(BaseModel):
#     name: str
#     phone: str
#     old_address: str
#     adharcard: str

# class UserCreate(UserBase):
#     pass

# class User(UserBase):
#     id: int
#     rooms: List[Room] = []

#     class Config:
#         orm_mode = True
#         schema_extra = {
#             "example": {
#                 "id": 1,
#                 "name": "John Doe",
#                 "phone": "1234567890",
#                 "old_address": "123 Old St, Old City",
#                 "adharcard": "123456789012",
#                 "rooms": [
#                     {
#                         "id": 1,
#                         "owner_id": 1,
#                         "type": "family_only",
#                         "member_size": 4,
#                         "work_name": "Software Development",
#                         "work_count": 3
#                     }
#                 ]
#             }
#         }
# Schemas/room.py
# from pydantic import BaseModel, validator
# from typing import Literal, Optional
# from app.schemas.CONSTANT import ROOM_TYPES

# class RoomBase(BaseModel):
#     type: Literal["family_only", "boys_only", "girls_only", "work"]
#     member_size: int
#     work_name: Optional[str] = None
#     work_count: Optional[int] = None

#     @validator("type")
#     def check_room_type(cls, value):
#         if value not in ROOM_TYPES:
#             raise ValueError(f"Invalid room type: {value}")
#         return value

# class RoomCreate(RoomBase):
#     pass

# class Room(RoomBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True
#         schema_extra = {
#             "example": {
#                 "id": 1,
#                 "owner_id": 1,
#                 "type": "family_only",
#                 "member_size": 4,
#                 "work_name": "Software Development",
#                 "work_count": 3
#             }
#         }
# database/database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
# database/db.py
# from app.database import SessionLocal

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# internals/payment.py
# from sqlalchemy.orm import Session
# from app.models import PaymentModel
# from app.schemas import PaymentCreate

# def create_payment(db: Session, payment: PaymentCreate):
#     db_payment = PaymentModel(**payment.dict())
#     db.add(db_payment)
#     db.commit()
#     db.refresh(db_payment)
#     return db_payment

# def get_payments(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(PaymentModel).offset(skip).limit(limit).all()

# def get_payment(db: Session, payment_id: int):
#     return db.query(PaymentModel).filter(Payment.id == payment_id).first()
# internals/user.py
# from sqlalchemy.orm import Session
# from app.schemas.models import User
# from app.schemas import UserCreate

# def create_user(db: Session, user: UserCreate):
#     db_user = User(**user.dict())
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def get_users(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(User).offset(skip).limit(limit).all()

# def get_user(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()


# internals/room.py
# from sqlalchemy.orm import Session
# from app.schemas.models import Room
# from app.schemas import RoomCreate

# def create_room(db: Session, room: RoomCreate, user_id: int):
#     db_room = Room(**room.dict(), user_id=user_id)
#     db.add(db_room)
#     db.commit()
#     db.refresh(db_room)
#     return db_room

# def get_rooms(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Room).offset(skip).limit(limit).all()

# def get_room(db: Session, room_id: int):
#     return db.query(Room).filter(Room.id == room_id).first()

# database.__init__.py
# from .database import (
#     Base,
#     engine,
#     SessionLocal,
# )

# from .db import get_db
# model.__init__.py
# # app/schemas/__init__.py
# from .user import UserModel
# from .room import RoomModel
# from .payment import PaymentModel


# shcemas.__init__.py
# # app/schemas/__init__.py

# from .room import (
#     RoomBase,
#     RoomCreate,
#     Room
# )
# from .user import (
#     UserBase,
#     UserCreate,
#     User
# )
# from .payment import (
#     PaymentBase,
#     PaymentCreate,
#     Payment
# )

# from .CONSTANT import (
#     ROOM_TYPES,
# )
# schemas.CONSTANT.py
# FAMILY_ONLY = "family_only"
# BOYS_ONLY = "boys_only"
# GIRLS_ONLY = "girls_only"
# WORK = "work"

# ROOM_TYPES = [FAMILY_ONLY, BOYS_ONLY, GIRLS_ONLY, WORK]

# routers.__init__.py
# from .payment import (
#     create_payment,
#     read_payments,
#     read_payment,
#     monthly_summary,
#     user_balance,
# )

# from room import (
#     create_user,
#     read_user,
#     read_users,

# )

# from .users import (
#     create_user,
#     read_user,
#     read_users,
# )

# routers.pyaments.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from app.database import SessionLocal
# from app.internals import payment as crud_payment
# from app.schemas import PaymentCreate, Payment
# # from app.
# from app.database.db import get_db

# router = APIRouter()



# @router.post("/", response_model=Payment)
# def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
#     """
#     Create a new payment record.

#     Args:
#         payment (PaymentCreate): Payment details.

#     Returns:
#         Payment: Created payment details.
#     """
#     return crud_payment.create_payment(db=db, payment=payment)

# @router.get("/", response_model=List[Payment])
# def read_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     """
#     Retrieve a list of payments with optional pagination.

#     Args:
#         skip (int, optional): Number of records to skip (default is 0).
#         limit (int, optional): Maximum number of records to retrieve (default is 10).

#     Returns:
#         List[Payment]: List of payments.
#     """
#     return crud_payment.get_payments(db, skip=skip, limit=limit)

# @router.get("/{payment_id}", response_model=Payment)
# def read_payment(payment_id: int, db: Session = Depends(get_db)):
#     """
#     Retrieve a specific payment record by ID.

#     Args:
#         payment_id (int): ID of the payment record to retrieve.

#     Returns:
#         Payment: Retrieved payment details.

#     Raises:
#         HTTPException: 404 if payment with the given ID does not exist.
#     """
#     db_payment = crud_payment.get_payment(db, payment_id=payment_id)
#     if db_payment is None:
#         raise HTTPException(status_code=404, detail="Payment not found")
#     return db_payment

# @router.get("/monthly_summary/", response_model=List[Payment])
# def monthly_summary(month: int, year: int, db: Session = Depends(get_db)):
#     """
#     Retrieve a monthly summary of payments.

#     Args:
#         month (int): Month number (1-12).
#         year (int): Year.

#     Returns:
#         List[Payment]: List of payments for the specified month and year.
#     """
#     return crud_payment.get_monthly_summary(db, month=month, year=year)

# @router.get("/user_balance/{user_id}", response_model=List[Payment])
# def user_balance(user_id: int, db: Session = Depends(get_db)):
#     """
#     Retrieve a list of payments related to a specific user for balance tracking.

#     Args:
#         user_id (int): ID of the user.

#     Returns:
#         List[Payment]: List of payments associated with the user.
#     """
#     return crud_payment.get_user_balance(db, user_id=user_id)

# routers.user.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from app.database import SessionLocal
# from app.internals.crud import user as crud_user
# from app.schemas import UserCreate, User, UserBase
# from app.database.db import get_db
# router = APIRouter()



# @router.post("/", response_model=User)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     """
#     Create a new user.

#     Args:
#         user (UserCreate): User details to create.

#     Returns:
#         UserBase: Created user details.
#     """
#     return crud_user.create_user(db=db, user=user)

# @router.get("/", response_model=List[User])
# def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     """
#     Retrieve a list of users with optional pagination.

#     Args:
#         skip (int, optional): Number of records to skip (default is 0).
#         limit (int, optional): Maximum number of records to retrieve (default is 10).

#     Returns:
#         List[UserBase]: List of users.
#     """
#     return crud_user.get_users(db, skip=skip, limit=limit)

# @router.get("/{user_id}", response_model=User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     """
#     Retrieve a specific user by ID.

#     Args:
#         user_id (int): ID of the user to retrieve.

#     Returns:
#         UserBase: Retrieved user details.

#     Raises:
#         HTTPException: 404 if user with the given ID does not exist.
#     """
#     db_user = crud_user.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
# router.room.py
# from fastapi import APIRouter, Depends, HTTPException
# from typing import List
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.internals.crud import room as crud_room
# from app.schemas.schemas import RoomCreate, Room
# from app.database.db import get_db


# router = APIRouter()


# @router.post("/", response_model=Room)
# def create_room(room: RoomCreate, user_id: int, db: Session = Depends(get_db)):
#     """
#     Create a new room associated with a user.

#     Args:
#         room (RoomCreate): Room details.
#         user_id (int): ID of the user associated with the room.

#     Returns:
#         Room: Created room details.
#     """
#     return crud_room.create_room(db=db, room=room, user_id=user_id)

# @router.get("/", response_model=List[Room])
# def read_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     """
#     Retrieve a list of rooms with optional pagination.

#     Args:
#         skip (int, optional): Number of records to skip (default is 0).
#         limit (int, optional): Maximum number of records to retrieve (default is 10).

#     Returns:
#         List[Room]: List of rooms.
#     """
#     return crud_room.get_rooms(db, skip=skip, limit=limit)

# @router.get("/{room_id}", response_model=Room)
# def read_room(room_id: int, db: Session = Depends(get_db)):
#     """
#     Retrieve a specific room by ID.

#     Args:
#         room_id (int): ID of the room to retrieve.

#     Returns:
#         Room: Retrieved room details.

#     Raises:
#         HTTPException: 404 if room with the given ID does not exist.
#     """
#     db_room = crud_room.get_room(db, room_id=room_id)
#     if db_room is None:
#         raise HTTPException(status_code=404, detail="Room not found")
#     return db_room

          