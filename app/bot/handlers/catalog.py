from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from app.services.catalog_service import CatalogService
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def show_catalog(message: types.Message):
    async with AsyncSessionLocal() as session:
        service = CatalogService(session)
        cats = await service.get_categories()
    kb = InlineKeyboardMarkup(row_width=2)
    for c in cats:
        kb.insert(InlineKeyboardButton(c.name, callback_data=f'cat:{c.id}'))
    await message.answer('Выберите категорию:', reply_markup=kb)

async def category_callback(callback: types.CallbackQuery):
    _, cat_id = callback.data.split(':')
    cat_id = int(cat_id)
    async with AsyncSessionLocal() as session:
        service = CatalogService(session)
        products = await service.get_products(cat_id)
    media = [InputMediaPhoto(p.image_url, caption=f"{p.name}
{p.price}₽") for p in products]
    await callback.message.answer_media_group(media)
    await callback.answer()


def register(dp: Dispatcher):
    dp.register_message_handler(show_catalog, lambda m: m.text == '📦 Каталог')
    dp.register_callback_query_handler(category_callback, lambda c: c.data and c.data.startswith('cat:'))