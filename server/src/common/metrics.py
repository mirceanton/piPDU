from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
from common.config import Config


class Exporter:
    # Flag indicating whether metrics are enabled
    __enabled = Config().data['metrics']['enabled']
    __instance = None   # Singleton instance of the Exporter class
    __gauges = None     # List of Prometheus gauges
    __app = None        # Flask app object

    # Method for initializing the Prometheus application
    def initialize(self, app):
        # If metrics are disabled, just exit
        if not self.__enabled:
            return

        # Initialize Prometheus application\
        print('Info: Initializing prometheus application')
        self.__app = PrometheusMetrics(app)
        print('Info: Prometheus OK')

        # Initialize list of Prometheus gauges
        print('Info: Initializing prometheus gauges')
        self.__gauges = [Gauge('socket_{}'.format(i), 'Socket {}'.format(i)) for i in range(16)]
        print('Info: Gauges OK')

    # Method for updating the values for the gauges
    def update(self, numbers):
        # If metrics are disabled, just exit
        if not self.__enabled:
            return

        if self.__app is None or self.__gauges is None:
          raise Exception("Error: Metrics application was not initialized")

        # Set the value of each gauge to the corresponding number
        print('Info: Updating values for gauges')
        for i, gauge in enumerate(self.__gauges):
            gauge.set(numbers[i])
        print('Info: Gauges updated')

    # Method for creating a singleton instance of the Exporter class
    def __new__(cls):
        # Create a new instance if another one doesn't already exist
        if Exporter.__instance is None:
            Exporter.__instance = object.__new__(cls)
        return Exporter.__instance
