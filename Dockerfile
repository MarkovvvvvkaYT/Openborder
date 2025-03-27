FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/static
CMD ["python", "main.py"]