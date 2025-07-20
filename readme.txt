
alembic init alembic

alembic revision --autogenerate -m "init"

alembic upgrade head

uvicorn app.main:app --reload --port 8000


powershell start command : powershell -ExecutionPolicy Bypass -File .\start.ps1

.venv/scripts/activate

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

ngrok http 8000

powershell -ExecutionPolicy Bypass -File .\start.ps1

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

.\.venv\Scripts\alembic.exe revision --autogenerate -m "add description to categories"
.\.venv\Scripts\alembic.exe upgrade head
alembic revision --autogenerate -m "fix_relations"


pydantic mapping in tg bot 
inline keyboard 
fsm multi step state 


