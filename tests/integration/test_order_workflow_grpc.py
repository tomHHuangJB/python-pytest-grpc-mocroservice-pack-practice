import pytest

from order_app.grpc_microservices.inventory_client import InventoryGrpcClient
from order_app.grpc_microservices.inventory_service import InventoryGrpcService, start_inventory_grpc_server
from order_app.models import InventoryServiceError, OutOfStockError
from order_app.repository import InMemoryOrderRepository
from order_app.service import OrderService


@pytest.mark.grpc
def test_order_service_creates_order_through_grpc_inventory(order_request) -> None:
    repository = InMemoryOrderRepository()
    servicer = InventoryGrpcService(stock_by_sku={"sku-001": 5})
    server, target = start_inventory_grpc_server(servicer)

    try:
        with InventoryGrpcClient(target=target) as inventory_client:
            service = OrderService(repository=repository, inventory_client=inventory_client)
            order = service.create_order(order_request)

        assert order.order_id
        assert repository.count() == 1
        assert servicer.calls == [("sku-001", 2)]
        assert servicer.stock_by_sku["sku-001"] == 3
    finally:
        server.stop(None)


@pytest.mark.grpc
def test_order_service_keeps_repository_clean_when_grpc_reports_out_of_stock(order_request) -> None:
    repository = InMemoryOrderRepository()
    servicer = InventoryGrpcService(out_of_stock_skus={"sku-001"})
    server, target = start_inventory_grpc_server(servicer)

    try:
        with InventoryGrpcClient(target=target) as inventory_client:
            service = OrderService(repository=repository, inventory_client=inventory_client)
            with pytest.raises(OutOfStockError):
                service.create_order(order_request)

        assert repository.count() == 0
    finally:
        server.stop(None)


@pytest.mark.grpc
def test_order_service_keeps_repository_clean_when_grpc_dependency_fails(order_request) -> None:
    repository = InMemoryOrderRepository()
    servicer = InventoryGrpcService(timeout_skus={"sku-001"})
    server, target = start_inventory_grpc_server(servicer)

    try:
        with InventoryGrpcClient(target=target, timeout_seconds=0.2) as inventory_client:
            service = OrderService(repository=repository, inventory_client=inventory_client)
            with pytest.raises(InventoryServiceError):
                service.create_order(order_request)

        assert repository.list_all() == []
    finally:
        server.stop(None)
