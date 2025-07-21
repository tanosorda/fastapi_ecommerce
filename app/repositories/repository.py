from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload, joinedload
from app.models import models
from app.schemas import schemas
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

async def get_categories(db: AsyncSession):
    result = await db.execute(
        select(models.Category)
    )
    return result.scalars().all()

async def get_category(db: AsyncSession, category_id: int) -> schemas.Category | None:
    result = await db.execute(
        select(models.Category)
        .where(models.Category.id == category_id)
    )
    return result.scalars().first()

async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_products_by_category(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(models.Product)
        .where(models.Product.category_id == category_id)
    )
    return result.scalars().all()

async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Cart operations
async def get_cart_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Cart)
        .where(models.Cart.user_id == user_id)
        .options(
            selectinload(models.Cart.items)
            .joinedload(models.CartItem.product)
        )
    )
    return result.scalars().first()

async def create_cart(db: AsyncSession, cart: schemas.CartBase):
    db_cart = models.Cart(**cart.dict())
    db.add(db_cart)
    await db.commit()
    await db.refresh(db_cart)
    return db_cart

async def add_cart_item(db: AsyncSession, cart_id: int, item: schemas.CartItemCreate):
    db_item = models.CartItem(cart_id=cart_id, **item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def update_cart_item_quantity(db: AsyncSession, item_id: int, quantity: int):
    await db.execute(
        update(models.CartItem)
        .where(models.CartItem.id == item_id)
        .values(quantity=quantity)
    )
    await db.commit()
    result = await db.execute(
        select(models.CartItem)
        .where(models.CartItem.id == item_id)
        .options(joinedload(models.CartItem.product))
    )
    return result.scalars().first()

async def remove_cart_item(db: AsyncSession, item_id: int):
    await db.execute(
        delete(models.CartItem)
        .where(models.CartItem.id == item_id)
    )
    await db.commit()

# Order operations
async def create_order(db: AsyncSession, user_id: int):
    cart = await get_cart_by_user(db, user_id)
    if not cart or not cart.items:
        return None
    
    db_order = models.Order(user_id=user_id)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    
    for item in cart.items:
        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.add(order_item)
    
    # Clear cart items
    await db.execute(
        delete(models.CartItem)
        .where(models.CartItem.cart_id == cart.id)
    )
    await db.commit()
    return db_order

async def get_orders_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Order)
        .where(models.Order.user_id == user_id)
        .options(
            selectinload(models.Order.items)
            .joinedload(models.OrderItem.product)
        )
    )
    return result.scalars().all()

async def get_order_by_id(db: AsyncSession, order_id: int, user_id: int):
    result = await db.execute(
        select(models.Order)
        .where(
            (models.Order.id == order_id) &
            (models.Order.user_id == user_id)
        )
        .options(
            selectinload(models.Order.items)
            .joinedload(models.OrderItem.product)
        )
    )
    return result.scalars().first()

async def update_order_status(db: AsyncSession, order_id: int, status: str):
    await db.execute(
        update(models.Order)
        .where(models.Order.id == order_id)
        .values(status=status)
    )
    await db.commit()
    result = await db.execute(
        select(models.Order)
        .where(models.Order.id == order_id)
        .options(selectinload(models.Order.items).joinedload(models.OrderItem.product))
    )
    return result.scalars().first()

# Support operations
async def create_support_ticket(db: AsyncSession, ticket: schemas.SupportTicketCreate, user_id: int):
    db_ticket = models.SupportTicket(
        user_id=user_id,
        question=ticket.question
    )
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket

async def get_support_tickets(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.SupportTicket)
        .where(models.SupportTicket.user_id == user_id)
    )
    return result.scalars().all()

async def get_support_ticket(db: AsyncSession, ticket_id: int, user_id: int):
    result = await db.execute(
        select(models.SupportTicket)
        .where(
            (models.SupportTicket.id == ticket_id) &
            (models.SupportTicket.user_id == user_id)
        )
    )
    return result.scalars().first()

async def answer_support_ticket(db: AsyncSession, ticket_id: int, answer: str):
    await db.execute(
        update(models.SupportTicket)
        .where(models.SupportTicket.id == ticket_id)
        .values(answer=answer, answered_at=datetime.utcnow())
    )
    await db.commit()
    result = await db.execute(
        select(models.SupportTicket)
        .where(models.SupportTicket.id == ticket_id)
    )
    return result.scalars().first()