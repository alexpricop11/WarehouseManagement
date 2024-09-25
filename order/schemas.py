from pydantic import BaseModel
from datetime import datetime
from models import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class CreateOrder(BaseModel):
    items: list[OrderItemBase]


class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: list[OrderItemBase]

    class Config:
        from_attributes = True


class UpdateOrderStatus(BaseModel):
    status: OrderStatus
