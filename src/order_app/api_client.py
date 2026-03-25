from typing import Any

import httpx

from order_app.schemas import ErrorResponsePayload, OrderCreatePayload, OrderResponsePayload


class OrderApiClient:
    def __init__(self, base_url: str, client: httpx.Client | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.Client(base_url=self.base_url, timeout=5.0)

    def create_order(self, payload: OrderCreatePayload) -> OrderResponsePayload:
        response = self.client.post("/orders", json=payload.model_dump())
        self._raise_for_error_response(response)
        return OrderResponsePayload.model_validate(response.json())

    def get_order(self, order_id: str) -> OrderResponsePayload:
        response = self.client.get(f"/orders/{order_id}")
        self._raise_for_error_response(response)
        return OrderResponsePayload.model_validate(response.json())

    def _raise_for_error_response(self, response: httpx.Response) -> None:
        if response.is_success:
            return

        detail = "request failed"
        try:
            detail = ErrorResponsePayload.model_validate(response.json()).detail
        except Exception:
            pass
        raise RuntimeError(f"{response.status_code}: {detail}")

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "OrderApiClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
