import random
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import select, exists

from app.models.models import (
    Category, Product, Cart, CartItem,
    Order, OrderItem, SupportTicket
)

fake = Faker()

async def create_initial_data():
    from app.db.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        # Проверяем, есть ли уже категории или продукты (можно добавить другие сущности)
        category_exists = await db.execute(select(exists().where(Category.id != None)))
        product_exists = await db.execute(select(exists().where(Product.id != None)))
        
        if category_exists.scalar() or product_exists.scalar():
            # Если есть хотя бы одна запись, не создаём начальные данные
            return

        # Категории
        categories = []
        for i in range(5):
            category = Category(
                name=fake.unique.word().capitalize() + " Category",
                parent_id=None if i < 3 else random.choice([1, 2, 3])
            )
            db.add(category)
            categories.append(category)
        await db.commit()

        # Продукты
        products = []
        for _ in range(15):
            product = Product(
                name=fake.unique.word().capitalize() + " Product",
                description=fake.text(),
                price=round(random.uniform(10, 1000)),
                category_id=random.choice([c.id for c in categories])
            )
            db.add(product)
            products.append(product)
        await db.commit()

        # Корзины и позиции
        for user_id in range(1, 4):
            cart = Cart(user_id=user_id)
            db.add(cart)
            await db.commit()
            for _ in range(random.randint(1, 5)):
                item = CartItem(
                    cart_id=cart.id,
                    product_id=random.choice([p.id for p in products]),
                    quantity=random.randint(1, 5)
                )
                db.add(item)
        await db.commit()

        # Заказы и позиции
        for user_id in range(1, 4):
            order = Order(
                user_id=user_id,
                status=random.choice(["pending", "awaiting_confirmation", "cancelled"]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(order)
            await db.commit()
            for _ in range(random.randint(1, 5)):
                prod = random.choice(products)
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=prod.id,
                    quantity=random.randint(1, 3),
                    price=prod.price
                )
                db.add(order_item)
        await db.commit()

        # Тикеты поддержки
        for user_id in range(1, 4):
            for _ in range(random.randint(1, 3)):
                ticket = SupportTicket(
                    user_id=user_id,
                    question=fake.sentence(),
                    answer=fake.sentence() if random.choice([True, False]) else None,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15)),
                    answered_at=(
                        datetime.utcnow() - timedelta(days=random.randint(1, 10))
                    ) if random.choice([True, False]) else None
                )
                db.add(ticket)
        await db.commit()
