from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(64), unique=True, primary_key=True, nullable=False, default=str(uuid4()))
    firstName = Column(String(64), nullable=False)
    lastName = Column(String(64), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    phone = Column(String(64))

    orgs = relationship("Organisation", back_populates='organisations')

class Organisation(Base):
    __tablename__ = "organisations"

    orgId = Column(String(64), unique=True, primary_key=True, nullable=False, default=str(uuid4()))
    name = Column(String(64), nullable=False)
    description = Column(String)

    user = relationship("User", back_populates="orgs")