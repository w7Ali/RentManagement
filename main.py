from fastapi import FastAPI
from app.routers import users, room, payment
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(room.router, prefix="/rooms", tags=["rooms"])
app.include_router(payment.router, prefix="/payments", tags=["payments"])
