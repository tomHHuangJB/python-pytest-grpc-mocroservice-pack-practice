import pytest
from fastapi.testclient import TestClient

from order_app.api import app, get_order_service
from order_app.models import CreateOrderRequest, InventoryServiceError, OutOfStockError
from order_app.repository import InMemoryOrderRepository
from order_app.service import OrderService


class ApiInventoryStub:
    def __init__(self, mode: str = "ok") -> None:
        self.mode = mode
        self.calls: list[tuple[str, int]] = []

    def reserve(self, sku: str, quantity: int) -> None:
        self.calls.append((sku, quantity))
        if self.mode == "ok":
            return
        if self.mode == "out_of_stock":
            raise OutOfStockError("inventory unavailable")
        if self.mode == "timeout":
            raise TimeoutError("inventory timeout")
        raise RuntimeError(f"unknown mode: {self.mode}")


def build_test_client(mode: str = "ok") -> tuple[TestClient, InMemoryOrderRepository, ApiInventoryStub]:
    repository = InMemoryOrderRepository()
    inventory = ApiInventoryStub(mode=mode)
    service = OrderService(repository=repository, inventory_client=inventory)

    app.dependency_overrides[get_order_service] = lambda: service
    client = TestClient(app)
    return client, repository, inventory


@pytest.mark.api
def test_fastapi_healthcheck() -> None:
    client, _, _ = build_test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    app.dependency_overrides.clear()


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
    app.dependency_overrides.clear()


@pytest.mark.api
def test_fastapi_create_order_returns_422_for_invalid_payload() -> None:
    client, repository, _ = build_test_client()

    response = client.post(
        "/orders",
        json={"customer_id": "cust-123", "sku": "sku-001", "quantity": 0, "unit_price": 19.99},
    )

    assert response.status_code == 422
    assert repository.count() == 0
    app.dependency_overrides.clear()


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
    app.dependency_overrides.clear()


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
    app.dependency_overrides.clear()
