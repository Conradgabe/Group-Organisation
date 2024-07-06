from fastapi import FastAPI
from app.router import bind_all_routes
from app.database import Base, engine
from app.router.auth import auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)