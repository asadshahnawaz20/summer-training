# Present so pytest adds this project directory to sys.path, which lets the
# tests import the application package with `from app.main import app`
# regardless of how pytest is invoked.
import pytest
from sqlmodel import SQLModel, Session, delete

from app.database import engine
from app.models import Patient, User


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine)
    yield


@pytest.fixture(autouse=True)
def clear_database():
    with Session(engine) as session:
        session.exec(delete(Patient))
        session.exec(delete(User))
        session.commit()