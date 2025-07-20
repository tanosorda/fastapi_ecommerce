import asyncio
import random
from faker import Faker
from app.db.database import AsyncSessionLocal
from app.models.models import (
    Category, Product, Cart, CartItem, 
    Order, OrderItem, SupportTicket
)
from datetime import datetime, timedelta

fake = Faker()

async def create_initial_data():
    async with AsyncSessionLocal() as db:
        # Создаем категории
        categories = []
        for i in range(5):
            category = Category(
                name=fake.unique.word().capitalize() + " Category",
                parent_id=None if i < 3 else random.choice([1, 2, 3]) if i > 2 else None
            )
            db.add(category)
            categories.append(category)
        
        await db.commit()
        
        # Создаем продукты
        products = []
        for i in range(15):
            product = Product(
                name=fake.unique.word().capitalize() + " Product",
                description=fake.text(),
                price=round(random.uniform(10, 1000)),
                category_id=random.choice([c.id for c in categories])
            )
            db.add(product)
            products.append(product)
        
        await db.commit()
        
        # Создаем корзины и товары в корзине
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
        
        # Создаем заказы
        for user_id in range(1, 4):
            order = Order(
                user_id=user_id,
                status=random.choice(["pending", "awaiting_confirmation", "cancelled"]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(order)
            await db.commit()
            
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=random.randint(1, 3),
                    price=product.price
                )
                db.add(order_item)
        
        await db.commit()
        
        # Создаем тикеты поддержки
        for user_id in range(1, 4):
            for _ in range(random.randint(1, 3)):
                ticket = SupportTicket(
                    user_id=user_id,
                    question=fake.sentence(),
                    answer=fake.sentence() if random.choice([True, False]) else None,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15)),
                    answered_at=datetime.utcnow() - timedelta(days=random.randint(1, 10)) if random.choice([True, False]) else None
                )
                db.add(ticket)
        
        await db.commit()