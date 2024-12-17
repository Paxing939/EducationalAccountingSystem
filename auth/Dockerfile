FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files to the container
COPY . .

# Application startup command
CMD ["uvicorn", "auth_service:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
