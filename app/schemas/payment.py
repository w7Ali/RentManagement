# app/schemas/payment.py

from pydantic import BaseModel
from datetime import date

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
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "date": "2024-07-10",
                "amount": 5000,
                "status": "paid",
                "balance": 0,
                "electricity_usage": 150
            }
        }
