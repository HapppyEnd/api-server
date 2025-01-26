import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from code_app.main_app import app
from code_app.models import Base, Patient, User, get_db

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Create the test database tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override the dependency for the database session in FastAPI."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create a FastAPI test client
client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """Fixture for managing the database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def create_user(db_session: Session):
    """Create test user."""
    user = User(username="testuser", password="testpassword", role="doctor")
    user.set_password(user.password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    yield user
    db_session.delete(user)
    db_session.commit()


@pytest.fixture
def create_patient(db_session: Session, create_user: User):
    """Create test patient."""
    patient = Patient(date_of_birth=datetime.date(1990, 1, 1),
                      diagnosis=["Flu"], created_at=datetime.datetime.now())
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    yield patient
    db_session.delete(patient)
    db_session.commit()


def test_login(create_user: User):
    """
    Test successful login.

    Check when provided with correct credentials,
    server return status code 200 and includes access token 
    in the response.
    """
    response = client.post(
        "/login", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_read_patients(create_user: User, create_patient: Patient):
    """
    Test reading the list of patients after logging in.

    Verifies that after a successful login using the access token,
    server return status code 200 and a list of patients.
    """
    response = client.post(
        "/login", json={"username": "testuser", "password": "testpassword"})
    token = response.json()["access_token"]

    response = client.get(
        "/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_invalid_login():
    """
    Test login with incorrect credentials.

    Check when provided with incorrect credentials, server return status
    code 401 and an error message "Invalid credentials".
    """
    response = client.post(
        "/login", json={"username": "wronguser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_access_patients_without_token():
    """
    Test access to the list of patients without an authentication token.

    Verifies when attempting to access the "/patients" endpoint without
    token, server return status code 401 and the message
    "Not authenticated".
    """
    response = client.get("/patients")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
