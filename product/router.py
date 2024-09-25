from fastapi import APIRouter, Depends
from database import AsyncSession, get_db
from product.schemas import ProductResponse, CreateProduct, UpdateProduct
from product.services import ProductServices

product_router = APIRouter(prefix='/products', tags=['products'])


@product_router.post('/products', response_model=ProductResponse)
async def create_product(product: CreateProduct, db: AsyncSession = Depends(get_db)) -> ProductResponse:
    """Create Product"""
    product_service = ProductServices(db)
    return await product_service.create_product(product)


@product_router.get('/products')
async def get_products(db: AsyncSession = Depends(get_db)):
    """Get all the products just the name"""
    product_service = ProductServices(db)
    return await product_service.get_products()


@product_router.get('/products/{id}')
async def get_product_info(id: int, db: AsyncSession = Depends(get_db)):
    """Get info product by id"""
    product_service = ProductServices(db)
    return await product_service.get_product_by_id(id)


@product_router.put('/products/{id}', response_model=ProductResponse)
async def update_product(id: int, product_update: UpdateProduct, db: AsyncSession = Depends(get_db)):
    """Update product"""
    product_service = ProductServices(db)
    return await product_service.update_product(id, product_update)


@product_router.delete('/products/{id}')
async def delete_product(id: int, db: AsyncSession = Depends(get_db)):
    """Delete product by id"""
    product_service = ProductServices(db)
    return await product_service.delete_product(id)
