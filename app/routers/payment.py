from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.internals import payment as crud_payment
from app.schemas import PaymentCreate, Payment
# from app.
from app.database.db import get_db

router = APIRouter()



@router.post("/", response_model=Payment)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """
    Create a new payment record.

    Args:
        payment (PaymentCreate): Payment details.

    Returns:
        Payment: Created payment details.
    """
    return crud_payment.create_payment(db=db, payment=payment)

@router.get("/", response_model=List[Payment])
def read_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of payments with optional pagination.

    Args:
        skip (int, optional): Number of records to skip (default is 0).
        limit (int, optional): Maximum number of records to retrieve (default is 10).

    Returns:
        List[Payment]: List of payments.
    """
    return crud_payment.get_payments(db, skip=skip, limit=limit)

@router.get("/{payment_id}", response_model=Payment)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific payment record by ID.

    Args:
        payment_id (int): ID of the payment record to retrieve.

    Returns:
        Payment: Retrieved payment details.

    Raises:
        HTTPException: 404 if payment with the given ID does not exist.
    """
    db_payment = crud_payment.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/monthly_summary/", response_model=List[Payment])
def monthly_summary(month: int, year: int, db: Session = Depends(get_db)):
    """
    Retrieve a monthly summary of payments.

    Args:
        month (int): Month number (1-12).
        year (int): Year.

    Returns:
        List[Payment]: List of payments for the specified month and year.
    """
    return crud_payment.get_monthly_summary(db, month=month, year=year)

@router.get("/user_balance/{user_id}", response_model=List[Payment])
def user_balance(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a list of payments related to a specific user for balance tracking.

    Args:
        user_id (int): ID of the user.

    Returns:
        List[Payment]: List of payments associated with the user.
    """
    return crud_payment.get_user_balance(db, user_id=user_id)
