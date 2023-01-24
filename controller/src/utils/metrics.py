from config.config import Config
from utils.logger import logger
import requests
import re

class Metrics:
    """
    This is a singleton class meant to abstract away the Prometheus metrics scraper.

    Attributes
    ----------

    url : str
        The URL for the metrics endpoint which this class scrapes

    metrics: list<float>
        The values for the 16 gauges the endpoint exposes

    total: float
        The sum of all 16 gauges

    Methods
    -------

    collect()
        Scrapes the metrics endpoint and parses the data into the `metrics` and `total` fields.
    """
    url = f"http://{Config().api.host}:{Config().api.port}/metrics"

    def collect(self):
        """Scrape the metrics endpoint and update the cache."""
        # Clean up the metrics from the previous scrape
        self.metrics = []
        self.total = 0

        logger.info("Scraping metrics endpoint")
        response = requests.get(self.url)

        if response.status_code != 200:
            logger.error("Failed to scrape metrics endpoint")
            logger.debug(f"Response code was {response.status_code} and not 200")
            logger.debug(response)
            return
        logger.info("Metrics scraped successfully.")
        logger.debug(response.text)

        logger.info("Parsing metrics.")
        for line in response.text.split("\n"):
            if re.search("^socket_", line):
                value = float(line.split(' ')[1])
                self.metrics.append(value)
                self.total += value
        logger.info("Metrics parsed.")
        logger.debug(f"Metrics Updated: {self.metrics}")
        logger.debug(f"Total calculated: {self.total}")

    def __new__(cls):
        """
        Create/Retrieve the singleton instance
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new Metrics singleton instance')
            cls._instance = object.__new__(cls)
        return cls._instance
