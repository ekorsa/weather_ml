# weather_ml

# fetch weather from https://api.open-meteo.com/v1/forecast:
docker compose run --rm ml python fetch_weather.py

# train model:
docker compose run --rm ml python train.py

# predict:
docker compose run --rm ml python predict.py


# check Prometheus:
http://localhost:9090
http://localhost:9090/targets

# check predictions:
http://localhost:8000/predictions
