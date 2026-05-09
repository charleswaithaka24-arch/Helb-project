from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_payment() -> None:
    response = client.post("/payments/", json={"amount": 25.5})
    assert response.status_code == 201
    assert response.json()["amount"] == 25.5
    assert response.json()["status"] == "pending"


def test_get_payment() -> None:
    create_response = client.post("/payments/", json={"amount": 55.0})
    payment_id = create_response.json()["id"]
    response = client.get(f"/payments/{payment_id}")
    assert response.status_code == 200
    assert response.json()["id"] == payment_id
