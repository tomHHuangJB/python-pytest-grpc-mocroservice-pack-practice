import pytest
from fastapi.testclient import TestClient

from order_app.api import create_app
from order_app.repository import InMemoryOrderRepository
from order_app.service import OrderService
from tests.helpers.inventory import ApiInventoryStub


def build_test_client(mode: str = "ok") -> tuple[TestClient, InMemoryOrderRepository, ApiInventoryStub]:
    repository = InMemoryOrderRepository()
    inventory = ApiInventoryStub(mode=mode)
    service = OrderService(repository=repository, inventory_client=inventory)
    app = create_app(order_service=service)
    client = TestClient(app)
    return client, repository, inventory


@pytest.mark.api
def test_fastapi_healthcheck() -> None:
    client, _, _ = build_test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.api
def test_fastapi_create_order_returns_201_and_persists_state() -> None:
    client, repository, inventory = build_test_client()

    response = client.post(
        "/orders",
        json={"customer_id": "cust-123", "sku": "sku-001", "quantity": 2, "unit_price": 19.99},
    )

    body = response.json()
    assert response.status_code == 201
    assert body["customer_id"] == "cust-123"
    assert body["total_price"] == 39.98
    assert inventory.calls == [("sku-001", 2)]
    assert repository.count() == 1


@pytest.mark.api
def test_fastapi_create_order_returns_422_for_invalid_payload() -> None:
    client, repository, _ = build_test_client()

    response = client.post(
        "/orders",
        json={"customer_id": "cust-123", "sku": "sku-001", "quantity": 0, "unit_price": 19.99},
    )

    assert response.status_code == 422
    assert repository.count() == 0


@pytest.mark.api
def test_fastapi_create_order_returns_409_for_out_of_stock() -> None:
    client, repository, _ = build_test_client(mode="out_of_stock")

    response = client.post(
        "/orders",
        json={"customer_id": "cust-123", "sku": "sku-out", "quantity": 2, "unit_price": 19.99},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "inventory unavailable"}
    assert repository.count() == 0


@pytest.mark.api
def test_fastapi_create_order_returns_502_for_dependency_failure() -> None:
    client, repository, _ = build_test_client(mode="timeout")

    response = client.post(
        "/orders",
        json={"customer_id": "cust-123", "sku": "sku-timeout", "quantity": 2, "unit_price": 19.99},
    )

    assert response.status_code == 502
    assert response.json() == {"detail": "inventory dependency failed"}
    assert repository.count() == 0


@pytest.mark.api
def test_fastapi_get_order_returns_existing_record() -> None:
    client, _, _ = build_test_client()

    create_response = client.post(
        "/orders",
        json={"customer_id": "cust-123", "sku": "sku-001", "quantity": 2, "unit_price": 19.99},
    )
    order_id = create_response.json()["order_id"]

    get_response = client.get(f"/orders/{order_id}")

    assert get_response.status_code == 200
    assert get_response.json()["order_id"] == order_id


@pytest.mark.api
def test_fastapi_get_order_returns_404_for_missing_record() -> None:
    client, _, _ = build_test_client()

    response = client.get("/orders/missing-order")

    assert response.status_code == 404
    assert response.json() == {"detail": "order missing-order not found"}
