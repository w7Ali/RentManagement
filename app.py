from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel
import enum

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class RoomType(enum.Enum):
    family_only = "family_only"
    boys_only = "boys_only"
    girls_only = "girls_only"
    work = "work"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=date.today)
    name = Column(String, index=True)
    phone = Column(String)
    old_address = Column(String)
    adharcard = Column(String)


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(RoomType))
    member_size = Column(Integer)
    work_name = Column(String, nullable=True)
    user = relationship("User", back_populates="rooms")


User.rooms = relationship("Room", order_by=Room.id, back_populates="user")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    month = Column(String)
    amount = Column(Float)
    status = Column(String)
    balance = Column(Float)
    electricity_usage = Column(Float)
    user = relationship("User", back_populates="payments")


User.payments = relationship("Payment", order_by=Payment.id, back_populates="user")


Base.metadata.create_all(bind=engine)

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    phone: str
    old_address: str
    adharcard: str


class RoomCreate(BaseModel):
    user_id: int
    type: RoomType
    member_size: int
    work_name: str = None


class PaymentCreate(BaseModel):
    user_id: int
    month: str
    amount: float
    status: str
    balance: float
    electricity_usage: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/rooms/", response_model=RoomCreate)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@app.post("/payments/", response_model=PaymentCreate)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


@app.get("/users/{user_id}/payments/")
def get_user_payments(user_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.user_id == user_id).all()
    return payments


@app.get("/monthly-summary/{month}/")
def get_monthly_summary(month: str, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.month == month).all()
    summary = []
    total_amount_due = 0
    total_amount_paid = 0

    for payment in payments:
        user = db.query(User).filter(User.id == payment.user_id).first()
        summary.append({
            "user": user.name,
            "amount": payment.amount,
            "status": payment.status,
            "balance": payment.balance,
            "electricity_usage": payment.electricity_usage
        })
        total_amount_due += payment.amount
        total_amount_paid += (payment.amount - payment.balance)

    return {
        "summary": summary,
        "total_amount_due": total_amount_due,
        "total_amount_paid": total_amount_paid,
        "total_balance": total_amount_due - total_amount_paid
    }
