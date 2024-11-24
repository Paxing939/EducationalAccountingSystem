FROM python:3.10-slim

# Установить зависимости
RUN pip install fastapi sqlalchemy psycopg2-binary uvicorn

# Скопировать файлы приложения
COPY . /app

# Перейти в директорию приложения
WORKDIR /app

# Команда для запуска приложения
CMD ["uvicorn", "professions_service:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
