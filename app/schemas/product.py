from pydantic import BaseModel

class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    image_url: str
    category_id: int

    class Config:
        orm_mode = True