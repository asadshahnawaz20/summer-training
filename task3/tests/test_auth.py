from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "sara",
            "password": "123456",
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == "sara"


def test_login():
    client.post(
        "/auth/register",
        json={
            "username": "ali",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/token",
        data={
            "username": "ali",
            "password": "123456",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_register_duplicate_user():
    client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "password": "123456",
        },
    )

    assert response.status_code == 409


def test_invalid_login():
    response = client.post(
        "/auth/token",
        data={
            "username": "wrong",
            "password": "wrong",
        },
    )

    assert response.status_code == 401


def test_create_patient_without_token():
    response = client.post(
        "/patients/",
        json={
            "name": "Ali",
            "age": 25,
            "condition": "Diabetes",
            "risk_score": 80,
            "active": True,
        },
    )

    assert response.status_code == 401


def test_login_wrong_password():
    client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/token",
        data={
            "username": "john",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_invalid_token():
    response = client.post(
        "/patients/",
        headers={
            "Authorization":
            "Bearer invalidtoken"
        },
        json={
            "name": "Ali",
            "age": 25,
            "condition": "Flu",
            "risk_score": 50,
            "active": True,
        },
    )

    assert response.status_code == 401


from jose import jwt
from app.auth import SECRET_KEY, ALGORITHM


def test_token_without_sub():
    token = jwt.encode(
        {"test": "abc"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.post(
        "/patients/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "name": "Ali",
            "age": 25,
            "condition": "Flu",
            "risk_score": 50,
            "active": True,
        },
    )

    assert response.status_code == 401


def test_token_user_not_found():
    token = jwt.encode(
        {"sub": "ghostuser"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.post(
        "/patients/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "name": "Ali",
            "age": 25,
            "condition": "Flu",
            "risk_score": 50,
            "active": True,
        },
    )

    assert response.status_code == 401