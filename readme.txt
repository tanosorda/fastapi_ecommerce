
alembic init alembic

alembic revision --autogenerate -m "init"

alembic upgrade head

uvicorn app.main:app --reload --port 8000