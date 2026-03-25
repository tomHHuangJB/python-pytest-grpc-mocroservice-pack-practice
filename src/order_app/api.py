from fastapi import Depends, FastAPI, HTTPException, status

from order_app.models import CreateOrderRequest, InvalidOrderError, InventoryServiceError, OutOfStockError
from order_app.repository import InMemoryOrderRepository
from order_app.schemas import OrderCreatePayload, OrderResponsePayload
from order_app.service import OrderService

app = FastAPI(title="Order Practice API")


class LiveInventoryClient:
    def reserve(self, sku: str, quantity: int) -> None:
        if sku == "sku-out":
            raise OutOfStockError("inventory unavailable")
        if sku == "sku-timeout":
            raise TimeoutError("inventory timeout")


repository = InMemoryOrderRepository()
inventory_client = LiveInventoryClient()
service = OrderService(repository=repository, inventory_client=inventory_client)


def get_order_service() -> OrderService:
    return service


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/orders", response_model=OrderResponsePayload, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreatePayload, order_service: OrderService = Depends(get_order_service)) -> OrderResponsePayload:
    request = CreateOrderRequest(**payload.model_dump())
    try:
        order = order_service.create_order(request)
    except InvalidOrderError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except OutOfStockError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except InventoryServiceError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return OrderResponsePayload.model_validate(order.__dict__)
