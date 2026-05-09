from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_booking() -> None:
    response = client.post("/bookings/", json={"customer_name": "Alice", "phone_number": "1234567890", "loan_amount": 100.0})
    assert response.status_code == 201
    assert response.json()["customer_name"] == "Alice"
    assert response.json()["status"] == "pending"


def test_get_booking() -> None:
    create_response = client.post("/bookings/", json={"customer_name": "Bob", "phone_number": "0987654321", "loan_amount": 200.0})
    booking_id = create_response.json()["id"]
    response = client.get(f"/bookings/{booking_id}")
    assert response.status_code == 200
    assert response.json()["id"] == booking_id
