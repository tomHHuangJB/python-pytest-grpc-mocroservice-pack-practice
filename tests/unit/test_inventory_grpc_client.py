import pytest

from order_app.grpc_microservices.inventory_client import InventoryGrpcClient
from order_app.grpc_microservices.inventory_service import InventoryGrpcService, start_inventory_grpc_server
from order_app.models import InventoryServiceError, OutOfStockError


@pytest.mark.grpc
def test_inventory_grpc_client_reserves_stock_successfully() -> None:
    servicer = InventoryGrpcService(stock_by_sku={"sku-001": 3})
    server, target = start_inventory_grpc_server(servicer)

    try:
        with InventoryGrpcClient(target=target) as client:
            client.reserve("sku-001", 2)
        assert servicer.stock_by_sku["sku-001"] == 1
        assert servicer.calls == [("sku-001", 2)]
    finally:
        server.stop(None)


@pytest.mark.grpc
def test_inventory_grpc_client_maps_out_of_stock_response() -> None:
    servicer = InventoryGrpcService(out_of_stock_skus={"sku-out"})
    server, target = start_inventory_grpc_server(servicer)

    try:
        with InventoryGrpcClient(target=target) as client:
            with pytest.raises(OutOfStockError, match="inventory unavailable"):
                client.reserve("sku-out", 1)
    finally:
        server.stop(None)


@pytest.mark.grpc
def test_inventory_grpc_client_maps_rpc_failure_to_dependency_error() -> None:
    servicer = InventoryGrpcService(timeout_skus={"sku-timeout"})
    server, target = start_inventory_grpc_server(servicer)

    try:
        with InventoryGrpcClient(target=target, timeout_seconds=0.2) as client:
            with pytest.raises(InventoryServiceError, match="inventory dependency failed"):
                client.reserve("sku-timeout", 1)
    finally:
        server.stop(None)
