# from fastapi import FastAPI
# from app.routers import users, room, payment
# from app.database import engine, Base

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(room.router, prefix="/rooms", tags=["rooms"])
# app.include_router(payment.router, prefix="/payments", tags=["payments"])

from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
