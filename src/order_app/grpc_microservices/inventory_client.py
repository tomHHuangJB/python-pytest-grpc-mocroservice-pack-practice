import grpc

from order_app.grpc_contracts import inventory_pb2, inventory_pb2_grpc
from order_app.models import InventoryServiceError, OutOfStockError


class InventoryGrpcClient:
    def __init__(self, target: str, timeout_seconds: float = 1.0) -> None:
        self.target = target
        self.timeout_seconds = timeout_seconds
        self.channel = grpc.insecure_channel(target)
        self.stub = inventory_pb2_grpc.InventoryServiceStub(self.channel)

    def reserve(self, sku: str, quantity: int) -> None:
        try:
            response = self.stub.Reserve(
                inventory_pb2.ReserveRequest(sku=sku, quantity=quantity),
                timeout=self.timeout_seconds,
            )
        except grpc.RpcError as exc:
            raise InventoryServiceError("inventory dependency failed") from exc

        if not response.reserved:
            raise OutOfStockError(response.reason or "inventory unavailable")

    def close(self) -> None:
        self.channel.close()

    def __enter__(self) -> "InventoryGrpcClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()
