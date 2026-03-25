import pytest

from order_app.models import InventoryServiceError
from order_app.service import OrderService


@pytest.mark.integration
def test_sqlite_repository_persists_and_fetches_orders(sqlite_repository, order_request, inventory_client) -> None:
    service = OrderService(repository=sqlite_repository, inventory_client=inventory_client)

    created = service.create_order(order_request)
    fetched = sqlite_repository.get_by_id(created.order_id)

    assert sqlite_repository.count() == 1
    assert fetched == created


@pytest.mark.integration
def test_sqlite_repository_keeps_no_partial_write_on_dependency_failure(sqlite_repository, order_request, inventory_client_factory) -> None:
    service = OrderService(repository=sqlite_repository, inventory_client=inventory_client_factory(mode="timeout"))

    with pytest.raises(InventoryServiceError):
        service.create_order(order_request)

    assert sqlite_repository.count() == 0
    assert sqlite_repository.list_all() == []
