import httpx
import pytest

from order_app.api_client import OrderApiClient
from order_app.schemas import OrderCreatePayload


@pytest.mark.api
def test_api_client_create_order_validates_success_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/orders"
        body = {
            "order_id": "ord-123",
            "customer_id": "cust-123",
            "sku": "sku-001",
            "quantity": 2,
            "unit_price": 19.99,
            "total_price": 39.98,
        }
        return httpx.Response(status_code=201, json=body)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(base_url="https://practice.local", transport=transport)

    api_client = OrderApiClient(base_url="https://practice.local", client=client)
    response = api_client.create_order(
        OrderCreatePayload(customer_id="cust-123", sku="sku-001", quantity=2, unit_price=19.99)
    )

    assert response.order_id == "ord-123"
    assert response.total_price == 39.98
    api_client.close()


@pytest.mark.api
def test_api_client_raises_with_error_detail_from_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=409, json={"detail": "inventory unavailable"})

    transport = httpx.MockTransport(handler)
    client = httpx.Client(base_url="https://practice.local", transport=transport)

    api_client = OrderApiClient(base_url="https://practice.local", client=client)

    with pytest.raises(RuntimeError, match="409: inventory unavailable"):
        api_client.create_order(
            OrderCreatePayload(customer_id="cust-123", sku="sku-out", quantity=2, unit_price=19.99)
        )

    api_client.close()


@pytest.mark.api
def test_api_client_fails_when_success_response_schema_is_wrong() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=201,
            json={
                "order_id": "ord-123",
                "customer_id": "cust-123",
                "sku": "sku-001",
                "quantity": 2,
                "unit_price": 19.99,
            },
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(base_url="https://practice.local", transport=transport)

    api_client = OrderApiClient(base_url="https://practice.local", client=client)

    with pytest.raises(Exception):
        api_client.create_order(
            OrderCreatePayload(customer_id="cust-123", sku="sku-001", quantity=2, unit_price=19.99)
        )

    api_client.close()
