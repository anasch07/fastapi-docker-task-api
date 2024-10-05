import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app, get_db
from app.database import Base

# use a test database, e.g., an SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# create a configured "Session" class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create the test database tables
Base.metadata.create_all(bind=engine)


# dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# fixture to clean up the database after tests
@pytest.fixture(scope="module", autouse=True)
def teardown():
    yield
    # drop the test database tables after tests
    Base.metadata.drop_all(bind=engine)
    # remove the test database file
    os.remove("./test.db")


def test_create_task():
    response = client.post(
        "/tasks",
        json={"name": "Test Task", "completion_status": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Task"
    assert data["completion_status"] == False
    assert "id" in data
    assert data["id"] == 1


def test_read_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == "Test Task"
    assert data[0]["completion_status"] == False
