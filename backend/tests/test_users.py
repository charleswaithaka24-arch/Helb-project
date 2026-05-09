from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user() -> None:
    response = client.post("/users/", json={"email": "user@example.com", "password": "secret123"})
    assert response.status_code == 201
    assert response.json()["email"] == "user@example.com"
    assert "id" in response.json()


def test_get_user() -> None:
    create_response = client.post("/users/", json={"email": "other@example.com", "password": "secret123"})
    user_id = create_response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
