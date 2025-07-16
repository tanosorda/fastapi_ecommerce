# Активируем виртуальное окружение
. .\.venv\Scripts\Activate.ps1

# Запускаем ngrok в фоне (порт 8000)
# Start-Process -NoNewWindow -FilePath "ngrok" -ArgumentList "http 8000"

# Ждём, пока ngrok поднимется
# Start-Sleep -Seconds 4 

# Получаем публичный URL ngrok

# Запускаем FastAPI через uvicorn
uvicorn app.__main__:app --reload --host 127.0.0.1 --port 8000
