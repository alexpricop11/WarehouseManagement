from fastapi import FastAPI
from order.router import order_router
from product.router import product_router

app = FastAPI(title="Warehouse Management", description="API for managing warehouse orders and products")

app.include_router(product_router)
app.include_router(order_router)
