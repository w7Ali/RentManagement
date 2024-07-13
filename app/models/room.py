from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.schemas.CONSTANT import ROOM_TYPES


class RoomModel(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    member_size = Column(Integer)
    work_name = Column(String, nullable=True)
    work_count = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="rooms")

