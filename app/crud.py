from sqlalchemy.orm import Session
from app.models import User, Organisation, user_organisations
from app.schema import UserCreate
from uuid import uuid4
from app.auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        user_id=str(uuid4()),
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=hashed_password,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    create_organisation(db, db_user, f"{user.firstName}'s Organisation")
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_organisation(db: Session, user: User, org_name: str):
    db_org = Organisation(
        org_id=str(uuid4()),
        name=org_name,
        description=f"Organisation created by {user.firstName}"
    )
    db_org.user.append(user)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def get_user_organisations(db: Session, user_id: str):
    return db.query(Organisation).filter(Organisation.user.any(user_id=user_id)).all()

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def create_organisation(db: Session, user: User, org_name: str, description: str = None):
    db_org = Organisation(
        org_id=str(uuid4()),
        name=org_name,
        description=description
    )
    db_org.user.append(user)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def get_organisation_by_id(db: Session, org_id: str):
    return db.query(Organisation).filter(Organisation.org_id == org_id).first()

def add_user_to_organisation(db: Session, org_id: str, user_id: str):
    organisation = db.query(Organisation).filter(Organisation.org_id == org_id).first()
    user = db.query(User).filter(User.user_id == user_id).first()
    if organisation and user:
        organisation.user.append(user)
        db.commit()
        return True
    return False