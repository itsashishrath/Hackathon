from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_get_products_status_code():
    """Should return 200 OK when fetching products."""
    response = client.get("/products")
    assert response.status_code == 200


def test_get_products_returns_list():
    """Should return a JSON list."""
    response = client.get("/products")
    data = response.json()
    assert isinstance(data, list), "Expected list of products"
    assert len(data) > 0, "Expected at least one product"


def test_product_fields_and_types():
    """Each product should have required fields with correct types."""
    response = client.get("/products")
    products = response.json()

    required_fields = {"id": int, "name": str, "price": (float, int), "imageUrl": str}

    for product in products:
        for field, field_type in required_fields.items():
            assert field in product, f"Missing field: {field}"
            assert isinstance(product[field], field_type), f"Field '{field}' has wrong type"
            if field == "price":
                assert product["price"] >= 0, "Price should be non-negative"


def test_image_url_format():
    """Image URLs should be valid placeholder URLs."""
    response = client.get("/products")
    products = response.json()

    for product in products:
        assert product["imageUrl"].startswith("http"), "Image URL should start with http"
