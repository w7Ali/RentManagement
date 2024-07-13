from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class PaymentModel(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    amount = Column(Integer)
    status = Column(String)  # paid, unpaid, partial
    balance = Column(Integer)
    electricity_usage = Column(Integer)

    user = relationship("UserModel")
