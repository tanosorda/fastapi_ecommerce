# start.ps1 - С миграциями

# 1. Активируем виртуальное окружение
.\venv\Scripts\Activate.ps1

# 2. Устанавливаем зависимости
pip install -r requirements.txt

# 3. Применяем миграции (если используете Alembic)
alembic upgrade head

# 4. Запускаем приложение
$env:POSTGRES_URL = "postgresql+asyncpg://postgres:qwerty123@localhost:5432/cbdShop"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000