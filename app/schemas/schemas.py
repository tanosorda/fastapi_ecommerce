from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None

class Category(CategoryBase):
    id: int
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True

class CategoryWithChildren(Category):
    children: List['CategoryWithChildren'] = []

    class Config:
        orm_mode = True

CategoryWithChildren.update_forward_refs()

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    user_id: int

class Cart(CartBase):
    id: int
    created_at: datetime
    items: List[CartItem] = []

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItem(OrderItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    status: str

class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        orm_mode = True

class SupportTicketBase(BaseModel):
    question: str

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicket(SupportTicketBase):
    id: int
    user_id: int
    answer: Optional[str] = None
    created_at: datetime
    answered_at: Optional[datetime] = None

    class Config:
        orm_mode = True
