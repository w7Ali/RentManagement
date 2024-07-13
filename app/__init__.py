from fastapi import FastAPI

# app/__init__.py
from .database import Base, engine, SessionLocal
from .db import get_db

from app.routers import room, users, payment

def init_db():
    Base.metadata.create_all(bind=engine)

def get_application() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    def startup_event():
        init_db()

    return app

app = get_application()

# Import and include routers
from app.routers import room, users, payment
app.include_router(room.router, prefix="/rooms", tags=["Rooms"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(payment.router, prefix="/payments", tags=["Payments"])
