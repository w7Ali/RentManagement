# app/internals/payment.py

from sqlalchemy.orm import Session
from app.models.payment import PaymentModel
from app.schemas.payment import PaymentCreate

def create_payment(db: Session, payment: PaymentCreate):
    db_payment = PaymentModel(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(PaymentModel).offset(skip).limit(limit).all()

def get_payment(db: Session, payment_id: int):
    return db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
