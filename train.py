"""
train.py

This script:
1. Loads weather data from Redis
2. Prepares a simple time-series dataset
3. Trains a Linear Regression model
4. Saves the trained model to disk
"""

import json
import redis
import numpy as np
import joblib
import os
from sklearn.linear_model import LinearRegression

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Connect to Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# Path where the model will be saved
MODEL_PATH = "models/weather_model.pkl"

def load_data_from_redis(key="weather_data"):
    """
    Load temperature data from Redis.

    Expected format:
    JSON list of numbers, e.g. [20.1, 21.3, 19.8, ...]
    """
    raw = redis_client.get(key)

    if raw is None:
        raise ValueError("No data found in Redis under key: {}".format(key))

    data = json.loads(raw)
    return data


def prepare_dataset(temps, window_size=3):
    """
    Convert time series into supervised learning dataset.

    Example:
    Input:  [t1, t2, t3] -> Output: t4
    """
    X, y = [], []

    for i in range(len(temps) - window_size):
        X.append(temps[i:i + window_size])
        y.append(temps[i + window_size])

    return np.array(X), np.array(y)


def train_model(X, y):
    """
    Train a simple Linear Regression model.
    """
    model = LinearRegression()
    model.fit(X, y)
    return model


def save_model(model, path=MODEL_PATH):
    """
    Save trained model to disk using joblib.
    """
    joblib.dump(model, path)
    print(f"Model saved to {path}")


def main():
    print("Loading data from Redis...")
    temps = load_data_from_redis()

    # Optional: limit dataset size to avoid heavy computation
    temps = temps[-500:]

    print("Preparing dataset...")
    X, y = prepare_dataset(temps)

    print("Training model...")
    model = train_model(X, y)

    print("Saving model...")
    save_model(model)

    print("Training completed successfully.")


if __name__ == "__main__":
    main()
