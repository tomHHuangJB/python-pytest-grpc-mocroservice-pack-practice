from uuid import uuid4

from order_app.models import (
    CreateOrderRequest,
    InvalidOrderError,
    InventoryServiceError,
    Order,
    OutOfStockError,
)
from order_app.pricing import calculate_total
from order_app.repository import InMemoryOrderRepository


class OrderService:
    def __init__(self, repository: InMemoryOrderRepository, inventory_client) -> None:
        self.repository = repository
        self.inventory_client = inventory_client

    def create_order(self, request: CreateOrderRequest) -> Order:
        self._validate_request(request)
        total_price = calculate_total(request.unit_price, request.quantity)

        try:
            self.inventory_client.reserve(request.sku, request.quantity)
        except OutOfStockError:
            raise
        except Exception as exc:
            raise InventoryServiceError("inventory dependency failed") from exc

        order = Order(
            order_id=str(uuid4()),
            customer_id=request.customer_id,
            sku=request.sku,
            quantity=request.quantity,
            unit_price=request.unit_price,
            total_price=total_price,
        )
        self.repository.save(order)
        return order

    def _validate_request(self, request: CreateOrderRequest) -> None:
        if not request.customer_id.strip():
            raise InvalidOrderError("customer_id is required")
        if not request.sku.strip():
            raise InvalidOrderError("sku is required")
        if request.quantity <= 0:
            raise InvalidOrderError("quantity must be positive")
        if request.unit_price <= 0:
            raise InvalidOrderError("unit_price must be positive")
