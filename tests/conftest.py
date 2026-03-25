from pathlib import Path

import pytest

from order_app.models import CreateOrderRequest, OutOfStockError
from order_app.repository import InMemoryOrderRepository, SqliteOrderRepository
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


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def proto_contract_path(repo_root: Path) -> Path:
    return repo_root / "proto" / "order_app" / "grpc_contracts" / "inventory.proto"


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
def sqlite_repository(tmp_path: Path) -> SqliteOrderRepository:
    return SqliteOrderRepository(str(tmp_path / "orders.db"))


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
