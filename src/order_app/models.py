from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrderRequest:
    customer_id: str
    sku: str
    quantity: int
    unit_price: float


@dataclass(frozen=True)
class Order:
    order_id: str
    customer_id: str
    sku: str
    quantity: int
    unit_price: float
    total_price: float


class OrderError(Exception):
    """Base class for domain-specific order errors."""


class InvalidOrderError(OrderError):
    """Raised when the request is invalid."""


class OutOfStockError(OrderError):
    """Raised when inventory cannot fulfill the request."""


class InventoryServiceError(OrderError):
    """Raised when the inventory dependency fails."""
