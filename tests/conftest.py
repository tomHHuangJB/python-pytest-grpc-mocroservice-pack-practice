import pytest

from order_app.models import CreateOrderRequest, OutOfStockError
from order_app.repository import InMemoryOrderRepository
from order_app.service import OrderService


class StubInventoryClient:
    def __init__(self, mode: str = "ok") -> None:
        self.mode = mode
        self.calls: list[tuple[str, int]] = []

    def reserve(self, sku: str, quantity: int) -> None:
        self.calls.append((sku, quantity))
        if self.mode == "ok":
            return
        if self.mode == "out_of_stock":
            raise OutOfStockError("inventory unavailable")
        if self.mode == "timeout":
            raise TimeoutError("inventory timeout")
        raise RuntimeError(f"unknown mode: {self.mode}")


@pytest.fixture
def order_request() -> CreateOrderRequest:
    return CreateOrderRequest(
        customer_id="cust-123",
        sku="sku-001",
        quantity=2,
        unit_price=19.99,
    )


@pytest.fixture
def repository() -> InMemoryOrderRepository:
    return InMemoryOrderRepository()


@pytest.fixture
def inventory_client() -> StubInventoryClient:
    return StubInventoryClient()


@pytest.fixture
def inventory_client_factory():
    def _create(mode: str = "ok") -> StubInventoryClient:
        return StubInventoryClient(mode=mode)

    return _create


@pytest.fixture
def order_service(repository: InMemoryOrderRepository, inventory_client: StubInventoryClient) -> OrderService:
    return OrderService(repository=repository, inventory_client=inventory_client)
