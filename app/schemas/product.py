from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str | None = None

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy