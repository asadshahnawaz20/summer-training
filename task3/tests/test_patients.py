from fastapi.testclient import TestClient
from sqlmodel import Session, delete, SQLModel
import pytest
from app.main import app
from app.database import engine
from app.models import Patient, User

client = TestClient(app)


@pytest.fixture
def token():
    username = "testuser"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/token",
        data={
            "username": username,
            "password": "123456",
        },
    )

    access_token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {access_token}"
    }

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine)


@pytest.fixture(autouse=True)
def clear_database():
    with Session(engine) as session:
        session.exec(delete(Patient))
        session.exec(delete(User))
        session.commit()


def get_token():
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "123456",
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_sample_patient(headers):
    return client.post(
        "/patients/",
        headers=headers,
        json={
            "name": "Ali",
            "age": 25,
            "condition": "Diabetes",
            "risk_score": 80,
            "active": True,
        },
    )


# ===========================
# GET ENDPOINTS
# ===========================

def test_get_patients():
    response = client.get("/patients/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_single_patient():
    headers = get_token()
    patient = create_sample_patient(headers)

    patient_id = patient.json()["id"]

    response = client.get(f"/patients/{patient_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Ali"


def test_get_missing_patient():
    response = client.get("/patients/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Patient not found"
    }


# ===========================
# CREATE
# ===========================

def test_create_patient():
    headers = get_token()

    response = client.post(
        "/patients/",
        headers=headers,
        json={
            "name": "Ayesha",
            "age": 22,
            "condition": "Asthma",
            "risk_score": 60,
            "active": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Ayesha"


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


def test_create_patient_missing_field():
    headers = get_token()

    response = client.post(
        "/patients/",
        headers=headers,
        json={
            "name": "Ali",
            "age": 25,
        },
    )

    assert response.status_code == 422


def test_invalid_age():
    headers = get_token()

    response = client.post(
        "/patients/",
        headers=headers,
        json={
            "name": "Ali",
            "age": 150,
            "condition": "Diabetes",
            "risk_score": 80,
            "active": True,
        },
    )

    assert response.status_code == 422


def test_invalid_risk_score():
    headers = get_token()

    response = client.post(
        "/patients/",
        headers=headers,
        json={
            "name": "Ali",
            "age": 25,
            "condition": "Diabetes",
            "risk_score": 150,
            "active": True,
        },
    )

    assert response.status_code == 422


# ===========================
# UPDATE
# ===========================

def test_update_patient():
    headers = get_token()

    patient = create_sample_patient(headers)
    patient_id = patient.json()["id"]

    response = client.put(
        f"/patients/{patient_id}",
        headers=headers,
        json={
            "name": "Ali Updated",
            "age": 30,
            "condition": "Cancer",
            "risk_score": 90,
            "active": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["age"] == 30
    assert response.json()["condition"] == "Cancer"


def test_update_missing_patient():
    headers = get_token()

    response = client.put(
        "/patients/999",
        headers=headers,
        json={
            "name": "Unknown",
            "age": 30,
            "condition": "Cancer",
            "risk_score": 90,
            "active": True,
        },
    )

    assert response.status_code == 404


# ===========================
# PATCH
# ===========================

def test_patch_patient():
    headers = get_token()

    patient = create_sample_patient(headers)
    patient_id = patient.json()["id"]

    response = client.patch(
        f"/patients/{patient_id}",
        headers=headers,
        json={
            "age": 40
        },
    )

    assert response.status_code == 200
    assert response.json()["age"] == 40


def test_patch_missing_patient():
    headers = get_token()

    response = client.patch(
        "/patients/999",
        headers=headers,
        json={
            "age": 40
        },
    )

    assert response.status_code == 404


# ===========================
# DELETE
# ===========================

def test_delete_patient():
    headers = get_token()

    patient = create_sample_patient(headers)
    patient_id = patient.json()["id"]

    response = client.delete(
        f"/patients/{patient_id}",
        headers=headers,
    )

    assert response.status_code == 204


def test_delete_missing_patient():
    headers = get_token()

    response = client.delete(
        "/patients/999",
        headers=headers,
    )

    assert response.status_code == 404


# ===========================
# FILTERS
# ===========================

def test_get_active_patients():
    headers = get_token()

    client.post(
        "/patients/",
        headers=headers,
        json={
            "name": "Ali",
            "age": 20,
            "condition": "Diabetes",
            "risk_score": 80,
            "active": True,
        },
    )

    client.post(
        "/patients/",
        headers=headers,
        json={
            "name": "Sara",
            "age": 22,
            "condition": "Asthma",
            "risk_score": 50,
            "active": False,
        },
    )

    response = client.get(
        "/patients/?active=true"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_limit_patients():
    headers = get_token()

    create_sample_patient(headers)

    client.post(
        "/patients/",
        headers=headers,
        json={
            "name": "Sara",
            "age": 22,
            "condition": "Asthma",
            "risk_score": 50,
            "active": False,
        },
    )

    response = client.get(
        "/patients/?limit=1"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_by_condition(token):
    client.post(
        "/patients/",
        headers=token,
        json={
            "name": "Ali",
            "age": 25,
            "condition": "Diabetes",
            "risk_score": 80,
            "active": True,
        },
    )

    client.post(
        "/patients/",
        headers=token,
        json={
            "name": "Sara",
            "age": 30,
            "condition": "Cancer",
            "risk_score": 70,
            "active": True,
        },
    )

    response = client.get(
        "/patients/?condition=Diabetes"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["condition"] == "Diabetes"


def test_offset_patients(token):
    for i in range(5):
        client.post(
            "/patients/",
            headers=token,
            json={
                "name": f"Patient{i}",
                "age": 30,
                "condition": "Flu",
                "risk_score": 50,
                "active": True,
            },
        )

    response = client.get(
        "/patients/?offset=2"
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_invalid_age(token):
    response = client.post(
        "/patients/",
        headers=token,
        json={
            "name": "Ali",
            "age": 200,
            "condition": "Flu",
            "risk_score": 50,
            "active": True,
        },
    )

    assert response.status_code == 422


def test_invalid_risk_score(token):
    response = client.post(
        "/patients/",
        headers=token,
        json={
            "name": "Ali",
            "age": 25,
            "condition": "Flu",
            "risk_score": 200,
            "active": True,
        },
    )

    assert response.status_code == 422