from fastapi import HTTPException
from sqlalchemy.future import select

from database import AsyncSession
from models import Product
from product.schemas import CreateProduct, UpdateProduct


class ProductServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, product_create: CreateProduct):
        new_product = Product(**product_create.dict())
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def get_products(self):
        result = await self.db.execute(select(Product.name))
        products = result.scalars().all()
        return products

    async def get_product_by_id(self, id: int):
        product = await self.db.execute(select(Product).where(id == Product.id))
        result = product.scalars().first()
        if result is None:
            raise HTTPException(status_code=404, detail='Order not found')
        return result

    async def update_product(self, product_id: int, update_product: UpdateProduct):
        product = await self.db.execute(select(Product).where(product_id == Product.id))
        result = product.scalars().first()
        if result is None:
            raise HTTPException(status_code=404, detail='Product not found')
        for key, value in update_product.dict(exclude_unset=True).items():
            setattr(result, key, value)
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def delete_product(self, product_id: int):
        product = await self.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail='Product not found')
        await self.db.delete(product)
        await self.db.commit()
        return product

    async def check_stock(self, product_id: int, quantity: int):
        product = await self.db.execute(select(Product).where(product_id == Product.id))
        product = product.scalars().first()
        if not product or product.quantity_in_stock < quantity:
            raise HTTPException(status_code=400, detail=f"Not enough items for product ID {product_id}")
        return product

    async def reduce_stock(self, product: Product, quantity: int):
        product.quantity_in_stock -= quantity
        self.db.add(product)
