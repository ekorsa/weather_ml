"""
predict.py

This script:
1. Loads trained model
2. Reads data from Redis
3. Makes prediction
4. Saves prediction to PostgreSQL
"""

import json
import redis
import joblib
import numpy as np
import os
from sqlalchemy import create_engine
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import pandas as pd
from datetime import datetime

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# PostgreSQL connection
engine = create_engine(DATABASE_URL)


MODEL_PATH = "models/weather_model.pkl"


def load_data_from_redis(key="weather_data"):
    raw = redis_client.get(key)

    if raw is None:
        raise ValueError("No data found in Redis")

    return json.loads(raw)


def load_model():
    return joblib.load(MODEL_PATH)


def predict_next_temperature(model, temps, window_size=3):
    last_values = temps[-window_size:]
    arr = np.array(last_values).reshape(1, -1)

    return model.predict(arr)[0]


def save_prediction_to_postgres(prediction):
    """
    Save prediction into PostgreSQL table
    """
    df = pd.DataFrame([{
        "prediction": float(prediction),
        "created_at": datetime.utcnow()
    }])

    df.to_sql("predictions", engine, if_exists="append", index=False)


def main():
    print("Loading model...")
    model = load_model()

    print("Loading data...")
    temps = load_data_from_redis()

    print("Predicting...")
    prediction = predict_next_temperature(model, temps)

    print(f"Prediction: {prediction}")

    print("Saving to PostgreSQL...")
    save_prediction_to_postgres(prediction)

    
    from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

    registry = CollectorRegistry()

    g = Gauge(
        'ml_prediction_value',
        'Last ML prediction value',
        registry=registry
    )

    g.set(prediction)

    push_to_gateway(
        'pushgateway:9091',   # service name in docker-compose
        job='ml_job',
        registry=registry
    )


    print("Done!")


if __name__ == "__main__":
    main()
