from fastapi.testclient import TestClient
from server import app
import pytest

client = TestClient(app)


def test_checkout_successful_order():
    """Should succeed with valid product IDs and quantities."""
    order = [{"id": 1, "quantity": 1}]
    response = client.post("/checkout", json=order)
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "total_amount" in data
    assert data["message"] == "Checkout successful"


def test_checkout_invalid_product_id():
    """Should fail when product ID does not exist."""
    order = [{"id": 999, "quantity": 1}]  # nonexistent product
    response = client.post("/checkout", json=order)
    data = response.json()

    assert response.status_code == 404
    assert data["status"] == "error"
    assert "not found" in data["message"]


def test_checkout_invalid_payload_structure():
    """Should fail when JSON structure is invalid (not a list)."""
    order = {"id": 1, "quantity": 2}  # should be a list
    response = client.post("/checkout", json=order)
    data = response.json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "Invalid data format" in data["message"]


def test_checkout_invalid_quantity():
    """Should fail when quantity is zero or negative."""
    order = [{"id": 1, "quantity": 0}]
    response = client.post("/checkout", json=order)
    data = response.json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "Quantity must be at least 1" in data["message"]
