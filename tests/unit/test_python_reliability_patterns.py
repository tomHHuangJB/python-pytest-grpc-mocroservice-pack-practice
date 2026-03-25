import copy
from dataclasses import FrozenInstanceError

import pytest

from order_app.models import CreateOrderRequest
from order_app.repository import InMemoryOrderRepository
from order_app.service import OrderService


class AlwaysAvailableInventoryClient:
    def reserve(self, sku: str, quantity: int) -> None:
        return


def make_api_order_payload() -> dict:
    return {
        "customer": {"id": "cust-123", "tier": "standard"},
        "order": {"sku": "sku-001", "quantity": 2, "unit_price": 19.99},
    }


def build_request_from_payload(payload: dict) -> CreateOrderRequest:
    return CreateOrderRequest(
        customer_id=payload["customer"]["id"],
        sku=payload["order"]["sku"],
        quantity=payload["order"]["quantity"],
        unit_price=payload["order"]["unit_price"],
    )


@pytest.fixture
def order_payload() -> dict:
    # Fresh nested API-style payload per test avoids cross-test mutation leaks.
    return make_api_order_payload()


@pytest.fixture
def service_factory():
    def _create(order_id: str = "order-123") -> OrderService:
        return OrderService(
            repository=InMemoryOrderRepository(),
            inventory_client=AlwaysAvailableInventoryClient(),
            id_factory=lambda: order_id,
        )

    return _create


@pytest.mark.unit
def test_frozen_dataclass_prevents_accidental_mutation_of_request_object() -> None:
    request = CreateOrderRequest(customer_id="cust-123", sku="sku-001", quantity=2, unit_price=19.99)

    with pytest.raises(FrozenInstanceError):
        request.quantity = 10  # type: ignore[misc]


@pytest.mark.unit
def test_object_reference_alias_can_change_real_request_data_before_service_call() -> None:
    original_payload = make_api_order_payload()
    alias = original_payload

    alias["order"]["quantity"] = 99
    request = build_request_from_payload(original_payload)

    assert request.quantity == 99


@pytest.mark.unit
def test_shallow_copy_of_nested_api_payload_can_corrupt_original_request_data() -> None:
    original_payload = make_api_order_payload()
    shallow_copy = original_payload.copy()

    shallow_copy["order"]["quantity"] = 7
    request = build_request_from_payload(original_payload)

    # Dict.copy() only protects the top-level object. Nested order data is still shared.
    assert request.quantity == 7


@pytest.mark.unit
def test_deep_copy_keeps_original_api_payload_safe_for_order_creation(service_factory) -> None:
    original_payload = make_api_order_payload()
    safe_copy = copy.deepcopy(original_payload)
    safe_copy["order"]["quantity"] = 7

    request = build_request_from_payload(original_payload)
    created = service_factory().create_order(request)

    assert request.quantity == 2
    assert created.quantity == 2
    assert created.total_price == 39.98


@pytest.mark.unit
def test_fixture_returns_fresh_payload_that_can_be_modified_safely_per_test(order_payload) -> None:
    order_payload["order"]["quantity"] = 5
    request = build_request_from_payload(order_payload)

    assert request.quantity == 5


@pytest.mark.unit
def test_fixture_isolation_prevents_quantity_leak_from_previous_test(order_payload, service_factory) -> None:
    request = build_request_from_payload(order_payload)
    created = service_factory().create_order(request)

    # If fixture isolation were weak, this could still be 5 from the prior test.
    assert request.quantity == 2
    assert created.total_price == 39.98


@pytest.mark.unit
def test_session_scoped_fixture_is_right_for_immutable_repo_metadata(proto_contract_path) -> None:
    assert proto_contract_path.name == "inventory.proto"
    assert proto_contract_path.exists()


@pytest.mark.unit
def test_scope_problem_with_closure_can_produce_wrong_order_ids() -> None:
    services = []
    for order_id in ["order-001", "order-002", "order-003"]:
        services.append(
            OrderService(
                repository=InMemoryOrderRepository(),
                inventory_client=AlwaysAvailableInventoryClient(),
                id_factory=lambda: order_id,
            )
        )

    request = build_request_from_payload(make_api_order_payload())
    created_ids = [service.create_order(request).order_id for service in services]

    assert created_ids == ["order-003", "order-003", "order-003"]


@pytest.mark.unit
def test_binding_closure_value_correctly_keeps_expected_order_ids() -> None:
    services = []
    for order_id in ["order-001", "order-002", "order-003"]:
        services.append(
            OrderService(
                repository=InMemoryOrderRepository(),
                inventory_client=AlwaysAvailableInventoryClient(),
                id_factory=lambda order_id=order_id: order_id,
            )
        )

    request = build_request_from_payload(make_api_order_payload())
    created_ids = [service.create_order(request).order_id for service in services]

    assert created_ids == ["order-001", "order-002", "order-003"]


@pytest.mark.unit
@pytest.mark.parametrize(
    ("quantity", "expected_total"),
    [
        (1, 19.99),
        (2, 39.98),
        (3, 59.97),
    ],
)
def test_parametrize_expands_real_order_creation_coverage(
    quantity: int, expected_total: float, service_factory
) -> None:
    payload = make_api_order_payload()
    payload["order"]["quantity"] = quantity

    created = service_factory(order_id=f"order-{quantity}").create_order(build_request_from_payload(payload))

    assert created.quantity == quantity
    assert created.total_price == expected_total
