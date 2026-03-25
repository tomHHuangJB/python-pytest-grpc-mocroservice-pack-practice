from concurrent import futures

import grpc

from order_app.grpc_contracts import inventory_pb2, inventory_pb2_grpc


class InventoryGrpcService(inventory_pb2_grpc.InventoryServiceServicer):
    def __init__(
        self,
        stock_by_sku: dict[str, int] | None = None,
        out_of_stock_skus: set[str] | None = None,
        timeout_skus: set[str] | None = None,
    ) -> None:
        self.stock_by_sku = stock_by_sku or {"sku-001": 10, "sku-002": 5}
        self.out_of_stock_skus = out_of_stock_skus or set()
        self.timeout_skus = timeout_skus or set()
        self.calls: list[tuple[str, int]] = []

    def Reserve(self, request, context):
        self.calls.append((request.sku, request.quantity))

        if request.sku in self.timeout_skus:
            context.abort(grpc.StatusCode.DEADLINE_EXCEEDED, "inventory timeout")

        if request.sku in self.out_of_stock_skus:
            return inventory_pb2.ReserveResponse(reserved=False, reason="inventory unavailable")

        available_quantity = self.stock_by_sku.get(request.sku, 0)
        if available_quantity < request.quantity:
            return inventory_pb2.ReserveResponse(reserved=False, reason="inventory unavailable")

        self.stock_by_sku[request.sku] = available_quantity - request.quantity
        return inventory_pb2.ReserveResponse(reserved=True, reason="")


def start_inventory_grpc_server(servicer: InventoryGrpcService) -> tuple[grpc.Server, str]:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(servicer, server)
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    return server, f"127.0.0.1:{port}"
