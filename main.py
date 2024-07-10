from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schema, crud
from app.database import SessionLocal, engine, get_db
from app.utils.utils import verify_password
from app.auth import oauth2_scheme, create_access_token, get_current_user
from app.schema import RegistrationResponse, LoginResponse, OrganisationListResponse
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/test"):
async def():
    return {"Message", "Success"}

@app.post("/auth/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = crud.create_user(db, user)
    access_token = create_access_token(data={"sub": new_user.user_id})
    return RegistrationResponse(
        status="success",
        message="Registration successful",
        data={"accessToken": access_token, "user": new_user}
    )

@app.post("/auth/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.user_id})
    return LoginResponse(
        status="success",
        message="Login successful",
        data={"accessToken": access_token, "user": user}
    )

@app.get("/api/users/{id}", response_model=schema.UserResponse, status_code=status.HTTP_200_OK)
async def get_user(id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.user_id != current_user.user_id and user not in current_user.organisations:
        raise HTTPException(status_code=403, detail="Not authorized to view this user")
    return user

@app.get("/api/organisations", response_model=OrganisationListResponse, status_code=status.HTTP_200_OK)
async def get_organisations(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    organisations = crud.get_user_organisations(db, current_user.user_id)
    return OrganisationListResponse(
        status="success",
        message="Organisations retrieved successfully",
        data={"organisations": organisations}
    )

@app.get("/api/organisations/{org_id}", response_model=schema.OrganisationDetailResponse, status_code=status.HTTP_200_OK)
async def get_organisation(org_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    organisation = crud.get_organisation_by_id(db, org_id)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    if current_user not in organisation.user:
        raise HTTPException(status_code=403, detail="Not authorized to view this organisation")
    return schema.OrganisationDetailResponse(
        status="success",
        message="Organisation retrieved successfully",
        data=organisation
    )

@app.post("/api/organisations", response_model=schema.OrganisationDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_organisation(org: schema.OrganisationCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        new_org = crud.create_organisation(db, current_user, org.name, org.description)
        return schema.OrganisationDetailResponse(
            status="success",
            message="Organisation created successfully",
            data=new_org
        )
    except Exception:
        return schema.OrganisationDetailResponse(
            status="Bad Request",
            message="client error",
            statusCode=status.HTTP_400_BAD_REQUEST
        )
    
@app.post("/api/organisations/{org_id}/users", response_model=schema.OrganisationDetailResponse)
async def add_user_to_organisation(org_id: str, user_data: schema.AddUserToOrganisation, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    success = crud.add_user_to_organisation(db, org_id, user_data.userId)
    if not success:
        raise HTTPException(status_code=400, detail="User or Organisation not found")
    return schema.OrganisationDetailResponse(
        status="success",
        message="User added to organisation successfully",
        data={}
    )
