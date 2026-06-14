"""
api.py

Simple REST API to:
1. Get all predictions
2. Trigger new prediction
"""

from fastapi import FastAPI
from sqlalchemy import create_engine, text
from prometheus_fastapi_instrumentator import Instrumentator
import pandas as pd
import subprocess
import os

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

app = FastAPI()

# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


@app.get("/")
def root():
    return {"message": "Weather ML API is running"}


@app.get("/predictions")
def get_predictions():
    """
    Return all predictions from PostgreSQL
    """
    query = "SELECT * FROM predictions ORDER BY created_at DESC"
    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")


@app.post("/predict")
def run_prediction():
    """
    Run prediction script and store result
    """
    subprocess.run(["python", "predict.py"])

    return {"status": "Prediction executed"}
