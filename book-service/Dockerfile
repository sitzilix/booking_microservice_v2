FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Сначала требования
COPY book-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Копируем ОБЩУЮ папку common в корень /app
COPY common/ ./common/

# 3. Копируем СОДЕРЖИМОЕ book-service в корень /app
# Внимание: здесь мы копируем все файлы ИЗ папки сервиса прямо в текущий WORKDIR
COPY book-service/ .

# 4. Копируем .env (если нужен внутри)
COPY .env .

# Путь для поиска common и внутренних модулей
ENV PYTHONPATH=/app

# Запуск. Теперь папка app/ лежит прямо в /app/, 
# и команда 'app.main:app' сработает идеально.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]