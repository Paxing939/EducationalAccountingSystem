FROM python:3.10-slim

# Установить зависимости
RUN pip install fastapi sqlalchemy uvicorn
RUN pip install requests
RUN pip install psycopg2-binary
# Скопировать файлы приложения
COPY . /app

# Перейти в директорию приложения
WORKDIR /app

# Команда для запуска приложения
CMD ["uvicorn", "students_service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]