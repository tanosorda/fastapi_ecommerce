from aiogram import Bot, Dispatcher, types
from .handlers import start, catalog, cart, payment

bot = Bot(token="")  # token подставляется на стартапе
dp = Dispatcher(bot)

# Регистрируем хендлеры из модулей
start.register(dp)
catalog.register(dp)
cart.register(dp)
payment.register(dp)

async def process_update(update_json: dict):
    update = types.Update(**update_json)
    await dp.process_update(update)