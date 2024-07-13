from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    old_address = Column(String)
    adharcard = Column(String)

    rooms = relationship("Room", back_populates="owner")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    member_size = Column(Integer)
    work_name = Column(String, nullable=True)
    work_count = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="rooms")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    amount = Column(Integer)
    status = Column(String)  # paid, unpaid, partial
    balance = Column(Integer)
    electricity_usage = Column(Integer)

    user = relationship("User")
