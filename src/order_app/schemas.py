from pydantic import BaseModel, Field


class OrderCreatePayload(BaseModel):
    customer_id: str = Field(min_length=1)
    sku: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderResponsePayload(BaseModel):
    order_id: str
    customer_id: str
    sku: str
    quantity: int
    unit_price: float
    total_price: float


class ErrorResponsePayload(BaseModel):
    detail: str
