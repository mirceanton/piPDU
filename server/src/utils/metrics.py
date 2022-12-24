from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
from flask import Flask
from config.config import Config
from utils.logger import logger

class Exporter:
    """
    This is a singleton class meant to abstract away the Prometheus exporter.

    Attributes
    ----------

    app : PrometheusMetrics()
        The prometheus metrics application

    gauges : list<Gauge>
        The list of 16 gauges to expose in the metrics endpoint

    Methods
    -------

    update(numbers : list)
        Updates the prometheus gauges with the numbers in the given list.
        The list must have exactly 16 floats.

    initialize():
        Initializes the prometheus metrics application and the list of gauges.
    """

    def update(self, numbers: list) -> None:
        """
        Update the values for the gauges with the numbers from the given list

        Args:
            numbers (list<float>): The values for the gauges. Must be exactly 16
        """
        logger.info('Updating values for gauges')
        for i, gauge in enumerate(self.gauges):
            gauge.set(numbers[i])
        logger.info('Gauges updated')
        logger.debug(self.gauges)

    def initialize(self, app: Flask):
        """
        Initialize the Prometheus application and the list of gauges.

        Args:
            app (Flask): A Flask app object.
        """
        logger.info('Initializing prometheus application')
        self.app = PrometheusMetrics(app)
        logger.info('Prometheus OK')

        logger.info('Initializing prometheus gauges')
        self.gauges = [Gauge('socket_{}'.format(i), 'Socket {}'.format(i)) for i in range(16)]
        logger.info('Gauges OK')

    def __new__(cls):
        """
        Create/Retrieve the singleton instance
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new Exporter singleton instance')
            cls._instance = object.__new__(cls)
        else:
            logger.debug('Reused the Exporter singleton instance')
        return cls._instance
