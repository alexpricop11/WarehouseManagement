from fastapi import APIRouter, Depends
from database import AsyncSession, get_db
from order.schemas import OrderResponse, CreateOrder, UpdateOrderStatus
from order.services import OrderServices

order_router = APIRouter(prefix='/orders', tags=['orders'])


@order_router.post("/orders", response_model=OrderResponse)
async def create_order(order: CreateOrder, db: AsyncSession = Depends(get_db)):
    """Create order"""
    return await OrderServices(db).create_order(order)


@order_router.get("/orders")
async def get_orders(db: AsyncSession = Depends(get_db)):
    """Get all orders"""
    return await OrderServices(db).get_all_orders()


@order_router.get("/orders/{id}")
async def get_order_by_id(id: int, db: AsyncSession = Depends(get_db)):
    """Get order by id"""
    return await OrderServices(db).get_order_by_id(id)


@order_router.patch("/orders/{id}/status")
async def update_order_status(id: int, order_status: UpdateOrderStatus, db: AsyncSession = Depends(get_db)):
    """Update status"""
    return await OrderServices(db).update_order_status(id, order_status.status)
