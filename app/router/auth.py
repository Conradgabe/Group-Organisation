from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.utils.utils import get_password_hash, verify_password

from app.schema import UserCreate

auth_router = APIRouter()

@auth_router.post("auth/register/", tags=['User'])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password before storing it
    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        email=user.email,
        fullname=user.fullname,
        password=hashed_password,  # Store the hashed password
        is_verified=user.is_verified
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@auth_router.get("/users/{user_id}", tags=['User'], response_model=UserCreate)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
