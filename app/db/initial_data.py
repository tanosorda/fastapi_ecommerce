import random
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import select, exists, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import (
    Category, Product, Cart, CartItem,
    Order, OrderItem, SupportTicket
)

fake = Faker()

async def clear_existing_data(db: AsyncSession):
    """Удаление всех существующих данных"""
    await db.execute(delete(SupportTicket))
    await db.execute(delete(OrderItem))
    await db.execute(delete(Order))
    await db.execute(delete(CartItem))
    await db.execute(delete(Cart))
    await db.execute(delete(Product))
    await db.execute(delete(Category))
    await db.commit()

async def create_initial_data(overwrite: bool = True):
    """Создание начальных данных
    
    Args:
        overwrite (bool): Если True - перезаписывает существующие данные
                         Если False - пропускает если данные уже существуют
    """
    from app.db.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        # Проверка наличия данных
        has_data = await db.execute(
            select(exists().where(Category.id.isnot(None)))
        )
        has_data = has_data.scalar()

        if has_data:
            if not overwrite:
                return  # Данные уже есть и перезаписывать не нужно
            await clear_existing_data(db)

        # Создание категорий
        categories = []
        category_names = [
            "CBD Масла",
            "CBD Косметика",
            "CBD Жевательные конфеты",
            "CBD Для животных",
            "CBD Напитки"
        ]
        
        for name in category_names:
            category = Category(name=name)
            db.add(category)
            categories.append(category)
        await db.commit()

        # Создание продуктов
        products = []
        product_descriptions = [
            "Высококачественный продукт с CBD",
            "Органический продукт без добавок",
            "Премиальное качество, лабораторно проверено",
            "Натуральные ингредиенты",
            "Без ГМО и глютена"
        ]
        
        for i in range(15):
            product = Product(
                name=f"Продукт CBD-{i+1:02d} {fake.word().capitalize()}",
                description=random.choice(product_descriptions),
                price=round(random.uniform(100, 5000), 2),
                category_id=random.choice([c.id for c in categories])
            )
            db.add(product)
            products.append(product)
        await db.commit()

        # Создание корзин и позиций
        for user_id in range(1, 4):
            cart = Cart(user_id=user_id)
            db.add(cart)
            await db.commit()
            
            items_count = random.randint(1, 5)
            selected_products = random.sample(products, items_count)
            
            for product in selected_products:
                item = CartItem(
                    cart_id=cart.id,
                    product_id=product.id,
                    quantity=random.randint(1, 3)
                )
                db.add(item)
        await db.commit()

        # Создание заказов
        order_statuses = ["pending", "awaiting_confirmation", "completed", "cancelled"]
        for user_id in range(1, 4):
            order = Order(
                user_id=user_id,
                status=random.choice(order_statuses),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)))
            db.add(order)
            await db.commit()
            
            items_count = random.randint(1, 5)
            selected_products = random.sample(products, items_count)
            
            for product in selected_products:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=random.randint(1, 3),
                    price=product.price * (1 - random.uniform(0, 0.2))  # Случайная скидка до 20%
                )
                db.add(order_item)
        await db.commit()

        # Создание тикетов поддержки
        for user_id in range(1, 4):
            for _ in range(random.randint(1, 3)):
                is_answered = random.choice([True, False])
                created_at = datetime.utcnow() - timedelta(days=random.randint(1, 15))
                
                ticket = SupportTicket(
                    user_id=user_id,
                    question=f"Вопрос: {fake.sentence()}",
                    answer=f"Ответ: {fake.sentence()}" if is_answered else None,
                    created_at=created_at,
                    answered_at=created_at + timedelta(days=random.randint(1, 3)) if is_answered else None
                )
                db.add(ticket)
        await db.commit()