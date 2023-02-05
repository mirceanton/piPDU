import config.defaults as defaults
from utils.logger import logger
from types import SimpleNamespace
import yaml
import os


class Config:
    """
    This is a singleton object used to parse and "cache" the configuration settings.

    Attributes
    ----------

    api.host: str (default 0.0.0.0)
        The address on which the Flask API server will bind

    api.port: int (default 8080)
        The port on which the Flask API server will bind

    metrics.enabled: bool (default True)
        Whether or not to enable the metrics exporter

    arduino.device: str (default /dev/ttyACM0)
        The device file name for communicating with the arduino

    arduino.baud: int (default 9600)
        The baud rate for the serial communication

    Methods
    -------

    parse():
        Parses the config file or loads the defaults if no file is found.
    """
    file_path = "config.yaml"

    def parse(self):
        """
        Parse the config file or assume the defaults.
        """
        data = {}
        try:
            logger.info("Parsing config file")
            if os.path.exists(self.file_path):
                data = yaml.load(open(self.file_path), Loader=yaml.FullLoader)
                logger.info("Config file parsed.")
                logger.debug(data)
            else:
                logger.info("No config file found. Assuming defaults.")

            # Set values from config file/defaults
            self.api = SimpleNamespace(**data.get('api', defaults.api))
            logger.debug(f'Loaded API configuration: {self.api}')

            self.metrics = SimpleNamespace(**data.get('metrics', defaults.metrics))
            logger.debug(f'Loaded metrics configuration: {self.metrics}')
            
            self.arduino = SimpleNamespace(**data.get('arduino', defaults.arduino))
            logger.debug(f'Loaded arduino configuration: {self.arduino}')
        except Exception as e: # FIXME generic exception catching is BAD
            # Raise an exception with a custom error message if the config file parsing fails
            logger.error(f"Error: Failed to parse config file")
            logger.debug(f"{e}")

    def __new__(cls):
        """
        Create/Retrieve the singleton instance
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new Config singleton instance')
            cls._instance = object.__new__(cls)
            cls._instance.parse()
        else:
            logger.debug('Reused the Config singleton instance')
        return cls._instance
