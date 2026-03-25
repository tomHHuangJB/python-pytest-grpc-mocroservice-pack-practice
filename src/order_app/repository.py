from order_app.models import Order


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: list[Order] = []

    def save(self, order: Order) -> None:
        self._orders.append(order)

    def list_all(self) -> list[Order]:
        return list(self._orders)

    def count(self) -> int:
        return len(self._orders)
