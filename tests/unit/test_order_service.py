from unittest.mock import Mock

import pytest

from order_app.models import CreateOrderRequest, InvalidOrderError, InventoryServiceError, OrderNotFoundError, OutOfStockError
from order_app.repository import InMemoryOrderRepository
from order_app.service import OrderService


@pytest.mark.unit
def test_create_order_saves_order_and_calls_inventory(order_service, inventory_client, repository, order_request) -> None:
    order = order_service.create_order(order_request)

    assert order.customer_id == "cust-123"
    assert order.total_price == 39.98
    assert repository.count() == 1
    assert inventory_client.calls == [("sku-001", 2)]


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field", "value", "expected_message"),
    [
        ("customer_id", "", "customer_id is required"),
        ("sku", "", "sku is required"),
        ("quantity", 0, "quantity must be positive"),
        ("unit_price", 0, "unit_price must be positive"),
    ],
)
def test_create_order_rejects_invalid_requests(field: str, value, expected_message: str, repository) -> None:
    inventory_client = Mock()
    service = OrderService(repository=repository, inventory_client=inventory_client)
    request = CreateOrderRequest(customer_id="cust-123", sku="sku-001", quantity=2, unit_price=10.0)
    request = CreateOrderRequest(**{**request.__dict__, field: value})

    with pytest.raises(InvalidOrderError, match=expected_message):
        service.create_order(request)

    inventory_client.reserve.assert_not_called()
    assert repository.count() == 0


@pytest.mark.unit
def test_create_order_propagates_out_of_stock_without_partial_write(repository, order_request) -> None:
    inventory_client = Mock()
    inventory_client.reserve.side_effect = OutOfStockError("inventory unavailable")
    service = OrderService(repository=repository, inventory_client=inventory_client)

    with pytest.raises(OutOfStockError):
        service.create_order(order_request)

    assert repository.count() == 0


@pytest.mark.unit
def test_create_order_wraps_unexpected_inventory_failures(repository, order_request) -> None:
    inventory_client = Mock()
    inventory_client.reserve.side_effect = TimeoutError("dependency timeout")
    service = OrderService(repository=repository, inventory_client=inventory_client)

    with pytest.raises(InventoryServiceError, match="inventory dependency failed"):
        service.create_order(order_request)

    assert repository.count() == 0


@pytest.mark.unit
def test_get_order_returns_saved_order(order_service, order_request) -> None:
    created = order_service.create_order(order_request)

    fetched = order_service.get_order(created.order_id)

    assert fetched == created


@pytest.mark.unit
def test_get_order_raises_for_missing_order(order_service) -> None:
    with pytest.raises(OrderNotFoundError, match="order missing-order not found"):
        order_service.get_order("missing-order")
