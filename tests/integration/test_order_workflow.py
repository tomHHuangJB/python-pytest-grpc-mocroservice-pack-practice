import pytest

from order_app.models import InventoryServiceError, OutOfStockError


@pytest.mark.integration
def test_order_workflow_happy_path(order_service, repository, inventory_client, order_request) -> None:
    order = order_service.create_order(order_request)

    assert order.order_id
    assert order.total_price == 39.98
    assert repository.list_all()[0].sku == "sku-001"
    assert inventory_client.calls == [("sku-001", 2)]


@pytest.mark.integration
def test_order_workflow_out_of_stock_keeps_repository_clean(repository, order_request, inventory_client_factory) -> None:
    from order_app.service import OrderService

    service = OrderService(repository=repository, inventory_client=inventory_client_factory(mode="out_of_stock"))

    with pytest.raises(OutOfStockError):
        service.create_order(order_request)

    assert repository.list_all() == []


@pytest.mark.integration
def test_order_workflow_timeout_maps_to_dependency_error(repository, order_request, inventory_client_factory) -> None:
    from order_app.service import OrderService

    service = OrderService(repository=repository, inventory_client=inventory_client_factory(mode="timeout"))

    with pytest.raises(InventoryServiceError):
        service.create_order(order_request)

    assert repository.count() == 0
