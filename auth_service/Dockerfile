FROM python:3.11-slim

WORKDIR /app

# 1. Копируем зависимости (путь относительно контекста сборки в docker-compose)
COPY auth_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Копируем код
COPY common/ /app/common/
COPY auth_service/ /app/auth_service/

# 3. КРИТИЧЕСКИЙ МОМЕНТ: 
# Добавляем в PYTHONPATH и корень (для common), и папку сервиса (для app)
ENV PYTHONPATH=/app:/app/auth_service

# 4. Запуск uvicorn (теперь он увидит папку 'app' внутри auth-service)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]