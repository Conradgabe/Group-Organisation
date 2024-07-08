from sqlalchemy import Boolean, Column, Table, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from uuid import uuid4

user_organisations = Table(
    "user_organisations",
    Base.metadata,
    Column("user_id", String(64), ForeignKey("users.user_id")),
    Column("org_id", String(64), ForeignKey("organisations.org_id")),
)

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(64), unique=True, primary_key=True, nullable=False, default=lambda: str(uuid4()))
    firstName = Column(String(64), nullable=False)
    lastName = Column(String(64), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    phone = Column(String(64))

    orgs = relationship("Organisation", secondary="user_organisations", back_populates='user')

class Organisation(Base):
    __tablename__ = "organisations"

    org_id = Column(String(64), unique=True, primary_key=True, nullable=False, default=lambda: str(uuid4()))
    name = Column(String(64), nullable=False)
    description = Column(String)

    user = relationship("User", secondary="user_organisations", back_populates="orgs")
