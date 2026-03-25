from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from order_app.models import (
    CreateOrderRequest,
    InvalidOrderError,
    InventoryServiceError,
    OrderNotFoundError,
    OutOfStockError,
)
from order_app.repository import InMemoryOrderRepository
from order_app.schemas import OrderCreatePayload, OrderResponsePayload
from order_app.service import OrderService


class LiveInventoryClient:
    def reserve(self, sku: str, quantity: int) -> None:
        if sku == "sku-out":
            raise OutOfStockError("inventory unavailable")
        if sku == "sku-timeout":
            raise TimeoutError("inventory timeout")


def create_default_service() -> OrderService:
    repository = InMemoryOrderRepository()
    inventory_client = LiveInventoryClient()
    return OrderService(repository=repository, inventory_client=inventory_client)


def get_order_service(request: Request) -> OrderService:
    return request.app.state.order_service


def _order_to_payload(order) -> OrderResponsePayload:
    return OrderResponsePayload.model_validate(order.__dict__)


def create_app(order_service: OrderService | None = None) -> FastAPI:
    app = FastAPI(title="Order Practice API")
    app.state.order_service = order_service or create_default_service()

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    def order_demo_page() -> str:
        return """
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8" />
            <title>Order Practice UI</title>
            <style>
              body { font-family: Helvetica, Arial, sans-serif; margin: 2rem; background: #f4f6fb; color: #162238; }
              main { max-width: 52rem; margin: 0 auto; background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 12px 30px rgba(25, 45, 90, 0.10); }
              h1 { margin-top: 0; }
              form { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
              label { display: flex; flex-direction: column; font-weight: 600; gap: 0.4rem; }
              input { padding: 0.7rem; border: 1px solid #bcc8dd; border-radius: 8px; font-size: 1rem; }
              button { margin-top: 1rem; padding: 0.85rem 1.2rem; border: none; border-radius: 999px; background: #1355d3; color: white; font-weight: 700; cursor: pointer; }
              .result { margin-top: 1.5rem; padding: 1rem; border-radius: 12px; background: #edf3ff; }
              .error { background: #ffe9e8; color: #822727; }
              ul { padding-left: 1.25rem; }
            </style>
          </head>
          <body>
            <main>
              <h1>Order Practice UI</h1>
              <p>Use this page to practice UI plus API validation with Playwright.</p>
              <form id="order-form">
                <label>Customer ID <input id="customer_id" value="cust-123" /></label>
                <label>SKU <input id="sku" value="sku-001" /></label>
                <label>Quantity <input id="quantity" type="number" value="2" /></label>
                <label>Unit Price <input id="unit_price" type="number" step="0.01" value="19.99" /></label>
              </form>
              <button id="submit-order" type="button">Create Order</button>
              <section id="result" class="result" aria-live="polite">No order submitted yet.</section>
              <h2>What To Validate</h2>
              <ul>
                <li>Happy-path order creation</li>
                <li>Error messaging for downstream failures</li>
                <li>Cross-check UI output with API behavior</li>
              </ul>
            </main>
            <script>
              const result = document.getElementById("result");
              document.getElementById("submit-order").addEventListener("click", async () => {
                const payload = {
                  customer_id: document.getElementById("customer_id").value,
                  sku: document.getElementById("sku").value,
                  quantity: Number(document.getElementById("quantity").value),
                  unit_price: Number(document.getElementById("unit_price").value)
                };
                const response = await fetch("/orders", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(payload)
                });
                const body = await response.json();
                if (!response.ok) {
                  result.className = "result error";
                  result.textContent = `Error ${response.status}: ${body.detail}`;
                  return;
                }
                result.className = "result";
                result.textContent = `Order ${body.order_id} created for ${body.customer_id}. Total ${body.total_price}`;
              });
            </script>
          </body>
        </html>
        """

    @app.post("/orders", response_model=OrderResponsePayload, status_code=status.HTTP_201_CREATED)
    def create_order(
        payload: OrderCreatePayload, order_service: OrderService = Depends(get_order_service)
    ) -> OrderResponsePayload:
        request = CreateOrderRequest(**payload.model_dump())
        try:
            order = order_service.create_order(request)
        except InvalidOrderError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
        except OutOfStockError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
        except InventoryServiceError as exc:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

        return _order_to_payload(order)

    @app.get("/orders/{order_id}", response_model=OrderResponsePayload)
    def get_order(order_id: str, order_service: OrderService = Depends(get_order_service)) -> OrderResponsePayload:
        try:
            order = order_service.get_order(order_id)
        except OrderNotFoundError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
        return _order_to_payload(order)

    return app


app = create_app()
