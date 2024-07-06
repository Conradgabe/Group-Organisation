from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: Optional[str]

class OrgCreate(BaseModel):
    name: str
    description: str