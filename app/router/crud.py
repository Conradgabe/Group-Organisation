from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.utils.utils import get_password_hash, verify_password

from app.schema import UserCreate

crud_router = APIRouter()

# A user gets their record from the  org or database
@crud_router.get("/api/users/{userId}")
async def get_user(db: Session = Depends(get_db)):
    pass

# Get all organisation a user belongs to via the token
@crud_router.get("/api.organisations")
async def get_organisations(db: Session = Depends(get_db)):
    pass

# logged user gets the single organisations details
@crud_router.get("/api/organisations/{orgId}")
async def get_organisation(db: Session = Depends(get_db)):
    pass

# Create an organisation
@crud_router.post("/api/organisations")
async def create_organisation(db: Session = Depends(get_db)):
    pass

# Add a user to an organisation
@crud_router.post("/api/organisations/{orgId}/users")
async def add_user_to_organisation(db: Session = Depends(get_db)):
    pass