from prometheus_client.parser import text_string_to_metric_families
import requests


def scrape_metrics(endpoint):
    response = requests.get(endpoint)
    metrics = text_string_to_metric_families(response.text)

    # Extract the gauges from the metrics
    gauges = [metric for metric in metrics if metric.type == 'gauge']

    # Extract the values of the socket gauges
    socket_values = [0] * 16
    for gauge in gauges:
        if gauge.name.startswith('socket_'):
            socket_id = int(gauge.name.split('_')[1])
            socket_values[socket_id] = gauge.samples[0].value

    # Return the list of socket values
    return socket_values
