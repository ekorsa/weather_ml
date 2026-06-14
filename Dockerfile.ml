# Dockerfile.ml

FROM python:3.10-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

# Same env variables for DB access
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=weather_db

# Default command
CMD ["python", "train.py"]
