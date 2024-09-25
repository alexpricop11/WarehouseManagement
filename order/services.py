from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.future import select

from database import AsyncSession
from models import Order, OrderStatus, OrderItem
from order.schemas import CreateOrder, OrderResponse
from product.services import ProductServices


class OrderServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order: CreateOrder) -> OrderResponse:
        order_items = []
        product_service = ProductServices(self.db)
        for item in order.items:
            product = await product_service.check_stock(item.product_id, item.quantity)
            await product_service.reduce_stock(product, item.quantity)
            order_items.append(OrderItem(product_id=item.product_id, quantity=item.quantity))
        new_order = Order(status=OrderStatus.in_progress)
        new_order.order_items = order_items
        self.db.add(new_order)
        await self.db.commit()
        await self.db.refresh(new_order)
        return OrderResponse(id=new_order.id, created_at=new_order.created_at, status=new_order.status,
                             items=order.items)

    async def get_all_orders(self):
        result = await self.db.execute(select(Order))
        orders = result.scalars().all()
        return orders

    async def get_order_by_id(self, id: int):
        result = await self.db.execute(select(Order).where(id == Order.id))
        order = result.scalars().first()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    async def update_order_status(self, id: int, status: OrderStatus):
        update_status = update(Order).where(id == Order.id).values(status=status)
        result = await self.db.execute(update_status)
        await self.db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return result
