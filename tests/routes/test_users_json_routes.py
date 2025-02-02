import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from models.User import User

client = TestClient(app)

json_headers = {"Accept": "application/json"}


# ----- FIXTURES -----
@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    # Mock the return value of db.query(User).all()
    mock_db.query.return_value.all.return_value = [
        {"name": "Michael", "email": "michael@dundermifflin.com"},
        {"name": "Dwight", "email": "dwight@dundermifflin.com"},
    ]
    return mock_db


@pytest.fixture
def client(mock_db):
    from DB.session import get_db

    app.dependency_overrides[get_db] = lambda: mock_db
    with TestClient(app) as client:
        yield client


def test_get_all_users(client):
    response = client.get("/users", headers=json_headers)
    json_data = response.json()
    assert response.status_code == 200
    assert len(json_data) == 2
    assert json_data[0]["name"] == "Michael"
