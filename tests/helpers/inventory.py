from order_app.models import OutOfStockError


class ApiInventoryStub:
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
