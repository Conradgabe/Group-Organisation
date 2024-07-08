from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OrganisationResponse(BaseModel):
    org_id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class OrganisationListResponse(BaseModel):
    status: str
    message: str
    data: dict

    class Config:
        from_attributes = True

class RegistrationResponse(BaseModel):
    status: str
    message: str
    data: dict

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    status: str
    message: str
    data: dict

    class Config:
        from_attributes = True

class OrganisationCreate(BaseModel):
    name: str
    description: Optional[str] = None

class AddUserToOrganisation(BaseModel):
    user_id: str

class OrganisationDetailResponse(BaseModel):
    status: str
    message: str
    data: dict

    class Config:
        from_attributes = True

class OrganisationResponse(BaseModel):
    org_id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True