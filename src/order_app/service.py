from uuid import uuid4

from order_app.eventing import OrderCreatedEvent
from order_app.models import (
    CreateOrderRequest,
    InvalidOrderError,
    InventoryServiceError,
    Order,
    OrderNotFoundError,
    OutOfStockError,
)
from order_app.pricing import calculate_total
from order_app.repository import InMemoryOrderRepository


class OrderService:
    def __init__(self, repository: InMemoryOrderRepository, inventory_client, id_factory=None, event_bus=None) -> None:
        self.repository = repository
        self.inventory_client = inventory_client
        self.id_factory = id_factory or (lambda: str(uuid4()))
        self.event_bus = event_bus

    def create_order(self, request: CreateOrderRequest, idempotency_key: str | None = None) -> Order:
        self._validate_request(request)
        if idempotency_key:
            existing_order = self.repository.get_by_idempotency_key(idempotency_key)
            if existing_order is not None:
                return existing_order
        total_price = calculate_total(request.unit_price, request.quantity)

        try:
            self.inventory_client.reserve(request.sku, request.quantity)
        except OutOfStockError:
            raise
        except Exception as exc:
            raise InventoryServiceError("inventory dependency failed") from exc

        order = Order(
            order_id=self.id_factory(),
            customer_id=request.customer_id,
            sku=request.sku,
            quantity=request.quantity,
            unit_price=request.unit_price,
            total_price=total_price,
        )
        self.repository.save(order, idempotency_key=idempotency_key)
<<<<<<< HEAD
        if self.event_bus is not None:
            self.event_bus.publish(
                "order.created",
                OrderCreatedEvent(
                    order_id=order.order_id,
                    customer_id=order.customer_id,
                    sku=order.sku,
                    quantity=order.quantity,
                    total_price=order.total_price,
                ),
            )
=======
>>>>>>> 69e7893 (Add idempotency coverage and clean POC wording)
        return order

    def get_order(self, order_id: str) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(f"order {order_id} not found")
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
