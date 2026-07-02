from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database import engine
from app.models import Patient
from sqlmodel import Session, delete

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_database():
    with Session(engine) as session:
        session.exec(delete(Patient))
        session.commit()

def test_get_patients():
    response = client.get("/patients/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_patient():
    response = client.post(
        "/patients/",
        json={
            "id": 1,
            "name": "Ayesha",
            "age": 22,
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Ayesha"


def test_create_patient_missing_field():
    response = client.post(
        "/patients/",
        json={
            "id": 2,
            "name": "Ali",
        },
    )

    assert response.status_code == 422


def test_get_single_patient():
    client.post(
        "/patients/",
        json={
            "id": 10,
            "name": "Ali",
            "age": 25,
        },
    )

    response = client.get("/patients/10")

    assert response.status_code == 200
    assert response.json()["name"] == "Ali"


def test_get_missing_patient():
    response = client.get("/patients/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Patient not found"
    }


def test_delete_patient():
    client.post(
        "/patients/",
        json={
            "id": 20,
            "name": "Sara",
            "age": 30,
        },
    )

    response = client.delete("/patients/20")

    assert response.status_code == 204


def test_delete_missing_patient():
    response = client.delete("/patients/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Patient not found"
    }


def test_update_patient():
    client.post(
        "/patients/",
        json={
            "id": 1,
            "name": "Ali",
            "age": 20,
        },
    )

    response = client.put(
        "/patients/1",
        json={
            "id": 1,
            "name": "Ali",
            "age": 21,
        },
    )

    assert response.status_code == 200
    assert response.json()["age"] == 21


def test_update_missing_patient():
    response = client.put(
        "/patients/999",
        json={
            "id": 999,
            "name": "Unknown",
            "age": 30,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Patient not found"
    }


def test_patch_patient():
    client.post(
        "/patients/",
        json={
            "id": 1,
            "name": "Ali",
            "age": 20,
            "active": True,
        },
    )

    response = client.patch(
        "/patients/1",
        json={
            "age": 25,
        },
    )

    assert response.status_code == 200
    assert response.json()["age"] == 25


def test_patch_missing_patient():
    response = client.patch(
        "/patients/999",
        json={
            "age": 25,
        },
    )

    assert response.status_code == 404


def test_get_active_patients():
    client.post(
        "/patients/",
        json={
            "id": 1,
            "name": "Ali",
            "age": 20,
            "active": True,
        },
    )

    client.post(
        "/patients/",
        json={
            "id": 2,
            "name": "Sara",
            "age": 22,
            "active": False,
        },
    )

    response = client.get("/patients/?active=true")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Ali"


def test_limit_patients():
    client.post(
        "/patients/",
        json={
            "id": 1,
            "name": "Ali",
            "age": 20,
            "active": True,
        },
    )

    client.post(
        "/patients/",
        json={
            "id": 2,
            "name": "Sara",
            "age": 22,
            "active": False,
        },
    )

    response = client.get("/patients/?limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1