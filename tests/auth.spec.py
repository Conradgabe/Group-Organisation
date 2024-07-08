from app import crud
from app.schema import UserCreate

def test_register_success(client):
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123456789"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["user"]["firstName"] == "John"
    assert data["data"]["user"]["lastName"] == "Doe"
    assert data["data"]["user"]["email"] == "john.doe@example.com"
    assert "accessToken" in data["data"]

def test_register_missing_fields(client):
    response = client.post("/auth/register", json={
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123456789"
    })
    assert response.status_code == 422
    data = response.json()
    assert "errors" in data

def test_register_duplicate_email(client, db_session):
    crud.create_user(db_session, UserCreate(
        firstName="John",
        lastName="Doe",
        email="john.doe@example.com",
        password="password",
        phone="123456789"
    ))
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123456789"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "Bad request"
    assert data["message"] == "Registration unsuccessful"

def test_login_success(client):
    client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123456789"
    })
    response = client.post("/auth/login", data={
        "username": "john.doe@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["user"]["email"] == "john.doe@example.com"
    assert "accessToken" in data["data"]

def test_login_invalid_credentials(client):
    response = client.post("/auth/login", data={
        "username": "john.doe@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.json()
    assert data["status"] == "Bad request"
    assert data["message"] == "Authentication failed"
