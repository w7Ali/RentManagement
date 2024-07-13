from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.internals.crud import payment as crud_payment
from app.schemas import PaymentCreate, Payment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Payment)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return crud_payment.create_payment(db=db, payment=payment)

@router.get("/", response_model=List[Payment])
def read_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_payment.get_payments(db, skip=skip, limit=limit)

@router.get("/{payment_id}", response_model=Payment)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = crud_payment.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/monthly_summary/", response_model=List[Payment])
def monthly_summary(month: int, year: int, db: Session = Depends(get_db)):
    return crud_payment.get_monthly_summary(db, month=month, year=year)

@router.get("/user_balance/{user_id}", response_model=List[Payment])
def user_balance(user_id: int, db: Session = Depends(get_db)):
    return crud_payment.get_user_balance(db, user_id=user_id)
