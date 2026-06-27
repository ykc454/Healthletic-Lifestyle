import json
from app import app

client = app.test_client()

def test_home():
    response = client.get("/")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["message"] == "Healthletic Lifestyle Flask API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["status"] == "healthy"


def test_users():
    response = client.get("/api/users")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 2