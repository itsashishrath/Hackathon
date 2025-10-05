from fastapi.testclient import TestClient
from server import app, products
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_product_stock():
    """Resets product stock before each test."""
    for p in products:
        if p["id"] == 1: p["stock"] = 5
        if p["id"] == 2: p["stock"] = 2
        if p["id"] == 3: p["stock"] = 0
        if p["id"] == 4: p["stock"] = 10
        if p["id"] == 5: p["stock"] = 1

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


def test_checkout_out_of_stock():
    """Should fail when product is out of stock (stock == 0)."""
    # Product C in backend has stock = 0
    order = [{"id": 3, "quantity": 1}]
    response = client.post("/checkout", json=order)
    data = response.json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "out of stock" in data["message"]


def test_checkout_exceeds_stock():
    """Should fail when requested quantity > available stock."""
    # Product E has stock = 1, try buying 5
    order = [{"id": 5, "quantity": 5}]
    response = client.post("/checkout", json=order)
    data = response.json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "exceeds available stock" in data["message"]


def test_checkout_invalid_payload_structure():
    """Should fail when JSON structure is invalid (not a list)."""
    order = {"id": 1, "quantity": 2}  # should be a list
    response = client.post("/checkout", json=order)
    data = response.json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "Invalid data format" in data["message"]
