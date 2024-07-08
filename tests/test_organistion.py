from app.schema import UserCreate
from app import crud
from app.auth import create_access_token
from tests.conftest import db_session

def test_organisation_access(client, db_session):
    # create a user and organisation
    user = crud.create_user(db_session, UserCreate(
        firstName="Test",
        lastName="User",
        email="test3@example.com",
        password="password",
        phone="123456789"
    ))
    org = crud.create_organisation(db_session, user, "TestOrg", "Test Description")

    # create another user
    another_user = crud.create_user(db_session, UserCreate(
        firstName="Another",
        lastName="User",
        email="another3@example.com",
        password="password",
        phone="123456789"
    ))

    # try to access the organisation with another user
    access_token = create_access_token(data={"sub": another_user.user_id})
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/api/organisations/{org.org_id}", headers=headers)
    assert response.status_code == 401
