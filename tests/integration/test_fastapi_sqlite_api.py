import pytest
from fastapi.testclient import TestClient

from order_app.api import create_app
from order_app.repository import SqliteOrderRepository
from order_app.service import OrderService
from tests.helpers.inventory import ApiInventoryStub


@pytest.mark.integration
def test_fastapi_with_sqlite_repository_persists_between_requests(tmp_path) -> None:
    repository = SqliteOrderRepository(str(tmp_path / "orders.db"))
    inventory = ApiInventoryStub(mode="ok")
    service = OrderService(repository=repository, inventory_client=inventory)
    client = TestClient(create_app(order_service=service))

    create_response = client.post(
        "/orders",
        json={"customer_id": "cust-123", "sku": "sku-001", "quantity": 2, "unit_price": 19.99},
    )

    order_id = create_response.json()["order_id"]
    get_response = client.get(f"/orders/{order_id}")

    assert create_response.status_code == 201
    assert get_response.status_code == 200
    assert repository.count() == 1


@pytest.mark.integration
def test_fastapi_with_sqlite_repository_keeps_clean_state_after_failure(tmp_path) -> None:
    repository = SqliteOrderRepository(str(tmp_path / "orders.db"))
    inventory = ApiInventoryStub(mode="timeout")
    service = OrderService(repository=repository, inventory_client=inventory)
    client = TestClient(create_app(order_service=service))

    response = client.post(
        "/orders",
        json={"customer_id": "cust-123", "sku": "sku-timeout", "quantity": 2, "unit_price": 19.99},
    )

    assert response.status_code == 502
    assert repository.count() == 0
