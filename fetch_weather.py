import requests
import redis
import json
import os


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": 42.7,
        "longitude": 23.3,
        "hourly": "temperature_2m"
    }

    print("Starting request...")
    response = requests.get(url, params=params, timeout=5)

    print("Response received")
    data = response.json()

    # save only temperature
    temps = data["hourly"]["temperature_2m"]

    r.set("weather_data", json.dumps(temps))

fetch_weather()

