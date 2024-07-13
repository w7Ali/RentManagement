from fastapi import FastAPI
from app.database import Base, engine, SessionLocal, get_db
# app/routers/__init__.py
from app.routers.user import router as user_router
from app.routers.room import router as room_router
from app.routers.payment import router as payment_router


app = FastAPI()
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(room_router, prefix="/rooms", tags=["rooms"])
app.include_router(payment_router, prefix="/payments", tags=["payments"])

# Additional app configurations can go here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
