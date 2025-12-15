FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài build-essential để compile một số package nếu cần
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project
COPY . .

# Expose port
EXPOSE 8000

# Chạy uvicorn từ main.py ở root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
