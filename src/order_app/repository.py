import sqlite3

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

    def get_by_id(self, order_id: str) -> Order | None:
        for order in self._orders:
            if order.order_id == order_id:
                return order
        return None

    def clear(self) -> None:
        self._orders.clear()


class SqliteOrderRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._initialize_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    sku TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total_price REAL NOT NULL
                )
                """
            )

    def save(self, order: Order) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO orders (
                    order_id, customer_id, sku, quantity, unit_price, total_price
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    order.order_id,
                    order.customer_id,
                    order.sku,
                    order.quantity,
                    order.unit_price,
                    order.total_price,
                ),
            )

    def list_all(self) -> list[Order]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT order_id, customer_id, sku, quantity, unit_price, total_price
                FROM orders
                ORDER BY rowid
                """
            ).fetchall()
        return [self._row_to_order(row) for row in rows]

    def count(self) -> int:
        with self._connect() as connection:
            row = connection.execute("SELECT COUNT(*) FROM orders").fetchone()
        return int(row[0])

    def get_by_id(self, order_id: str) -> Order | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT order_id, customer_id, sku, quantity, unit_price, total_price
                FROM orders
                WHERE order_id = ?
                """,
                (order_id,),
            ).fetchone()
        return self._row_to_order(row) if row else None

    def clear(self) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM orders")

    def _row_to_order(self, row: tuple) -> Order:
        return Order(
            order_id=row[0],
            customer_id=row[1],
            sku=row[2],
            quantity=row[3],
            unit_price=row[4],
            total_price=row[5],
        )
