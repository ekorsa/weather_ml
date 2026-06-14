from prometheus_client import start_http_server, Gauge
import time

prediction_metric = Gauge("ml_prediction_value", "Last prediction value")

def start_metrics_server():
    start_http_server(8001)  # separate port


def record_prediction(value):
    prediction_metric.set(value)
