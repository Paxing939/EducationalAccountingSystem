FROM python:3.10-slim

# Установить зависимости
RUN pip install fastapi sqlalchemy psycopg2-binary uvicorn
RUN pip install requests
RUN pip install authx
#RUN pip install --no-cache-dir -r requirements.txt
# Скопировать файлы приложения
COPY . /app
COPY . /testLoginsAndPasswords.txt
# Перейти в директорию приложения
WORKDIR /app

# Команда для запуска приложения
CMD ["uvicorn", "auth_service:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
