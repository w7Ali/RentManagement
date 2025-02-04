# app/models/user.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.schemas.CONSTANT import ROOM_TYPES

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    old_address = Column(String)
    adharcard = Column(String)

    rooms = relationship("RoomModel", back_populates="owner")
