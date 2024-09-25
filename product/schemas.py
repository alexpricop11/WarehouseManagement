from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity_in_stock: int


class CreateProduct(ProductBase):
    pass


class UpdateProduct(ProductBase):
    name: str = None
    description: str = None
    price: float = None
    quantity_in_stock: int = None


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
