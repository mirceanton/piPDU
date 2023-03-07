from prometheus_client import Gauge, start_http_server


class Prometheus():
    def __init__(self):
        # Create the list for the prometheus gauges
        self.gauges = []
        for i in range(16):
            gauge = Gauge(
                f'socket_{i}', f'Socket {i} current in amps', ['unit'])
            self.gauges.append(gauge)

        # Start the metrics server
        start_http_server(8000)
        print('INFO: Prometheus Metrics Server started on port 8000')

    def update(self, values):
        # Update the gauges with the new values
        for i, value in enumerate(values):
            self.gauges[i].labels(unit=['unit']).set(value)
