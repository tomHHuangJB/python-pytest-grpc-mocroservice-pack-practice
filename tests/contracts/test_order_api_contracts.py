from pathlib import Path
from typing import Any, Literal

import pytest
from pact import Pact, Verifier

from order_app.api import create_app
from order_app.api_client import OrderApiClient
from order_app.models import Order
from order_app.repository import SqliteOrderRepository
from order_app.schemas import OrderCreatePayload
from order_app.service import OrderService
from tests.helpers.inventory import ApiInventoryStub
from tests.helpers.server import run_app_server


PACT_CONSUMER = "order-api-consumer"
PACT_PROVIDER = "OrderPracticeApi"


def _write_consumer_pact(output_dir: Path) -> Path:
    pact = Pact(PACT_CONSUMER, PACT_PROVIDER)

    (
        pact.upon_receiving("a request to fetch an existing order")
        .given("an order exists", order_id="order-123")
        .with_request("GET", "/orders/order-123")
        .will_respond_with(200)
        .with_body(
            {
                "order_id": "order-123",
                "customer_id": "cust-123",
                "sku": "sku-001",
                "quantity": 2,
                "unit_price": 19.99,
                "total_price": 39.98,
            },
            content_type="application/json",
        )
    )
    (
        pact.upon_receiving("a request to create a new order")
        .given("inventory is available for a new order")
        .with_request("POST", "/orders")
        .with_header("Content-Type", "application/json")
        .with_body({"customer_id": "cust-555", "sku": "sku-002", "quantity": 1, "unit_price": 12.5})
        .will_respond_with(201)
        .with_body(
            {
                "order_id": "order-456",
                "customer_id": "cust-555",
                "sku": "sku-002",
                "quantity": 1,
                "unit_price": 12.5,
                "total_price": 12.5,
            },
            content_type="application/json",
        )
    )

    with pact.serve() as srv:
        with OrderApiClient(str(srv.url)) as client:
            existing = client.get_order("order-123")
            created = client.create_order(
                OrderCreatePayload(customer_id="cust-555", sku="sku-002", quantity=1, unit_price=12.5)
            )
            assert existing.order_id == "order-123"
            assert created.order_id == "order-456"

    pact.write_file(output_dir)
    pact_files = sorted(output_dir.glob("*.json"))
    if not pact_files:
        raise AssertionError("No pact file was written")
    return pact_files[0]


@pytest.mark.contract
def test_consumer_contract_generates_pact_file(tmp_path: Path) -> None:
    pact_file = _write_consumer_pact(tmp_path)

    assert pact_file.exists()
    assert pact_file.read_text()


@pytest.mark.contract
def test_provider_verifies_generated_contract(tmp_path: Path) -> None:
    pact_dir = tmp_path / "pacts"
    pact_dir.mkdir()
    _write_consumer_pact(pact_dir)

    repository = SqliteOrderRepository(str(tmp_path / "provider.db"))
    inventory = ApiInventoryStub(mode="ok")
    service = OrderService(repository=repository, inventory_client=inventory, id_factory=lambda: "order-456")
    app = create_app(order_service=service)

    def handle_state(
        state: str,
        action: Literal["setup", "teardown"],
        parameters: dict[str, Any] | None,
    ) -> None:
        if action == "teardown":
            repository.clear()
            return

        repository.clear()
        if state == "an order exists":
            repository.save(
                Order(
                    order_id="order-123",
                    customer_id="cust-123",
                    sku="sku-001",
                    quantity=2,
                    unit_price=19.99,
                    total_price=39.98,
                )
            )
        elif state == "inventory is available for a new order":
            return
        else:
            raise ValueError(f"Unknown provider state: {state}")

    with run_app_server(app) as base_url:
        result = (
            Verifier(PACT_PROVIDER, host="127.0.0.1")
            .add_source(str(pact_dir))
            .add_transport(url=base_url)
            .state_handler(handle_state, teardown=True)
            .verify()
        )
    assert result
