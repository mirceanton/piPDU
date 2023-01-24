import config.defaults as defaults
from utils.logger import logger
from types import SimpleNamespace
import yaml


class Config(object):
    """
    This is a singleton object used to parse and "cache" the configuration settings.

    Attributes
    ----------

    api.host: str
        The address on which the Flask API server will bind

    api.port: int
        The port on which the Flask API server will bind

    metrics.enabled: bool (default True)
        Whether or not to enable the metrics exporter

    metrics.pollPeriodSeconds: int (default 1)
        The frequency at which to poll the metrics endpoint exposed by the server.

    led.pins: list
        Array containing the the pins used for the LEDs, mapped for the expanders

    button.pins: list<int>
        Array containing the the pins used for the buttons, mapped for the expanders

    button.longPressDurationSeconds: int (default 3)
        The interval in seconds a button has to be held for it to be considered a long press

    button.pollPeriodSeconds: int (default 0)
        The interval in seconds between 2 subsequent polls for events on the button matrix

    lcd.address: byte (default 0x27)
        The I2C address for the display

    lcd.backlight: bool (default True)
        Whether or not to enable the backlight on the display

    Methods
    -------

    parse():
        Parses the config file or loads the defaults if no file is found.  
        This function is called automatically when the first instance of the singleton is created.
    """

    def parse(self):
        """
        Parse the config file or assume the defaults.
        """
        try:
            logger.info("Parsing config file")
            with open('config.yaml') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                logger.info("Config file parsed.")
                logger.debug(data)

            if 'api' not in data:
                logger.error("The `api` section is missing from the config file!")
                raise ValueError('ERROR: The `api` section is missing from the config file!')
            if 'host' not in data['api']:
                logger.error("The `api.host` is not defined in the config file!")
                raise ValueError('ERROR: `api.host` is not defined in the config file!')
            if 'port' not in data['api']:
                logger.error("The `api.port` is not defined in the config file!")
                raise ValueError('ERROR: `api.port` is not defined in the config file!')

            # Set values from config file/defaults
            self.api = SimpleNamespace(**data['api'])
            logger.debug(f'Loaded API configuration: {self.api}')

            self.expanders = SimpleNamespace(**data.get('expanders', defaults.expanders))
            logger.debug(f'Loaded expanders configuration: {self.expanders}')

            self.metrics = SimpleNamespace(**data.get('metrics', defaults.metrics))
            logger.debug(f'Loaded metrics configuration: {self.metrics}')

            self.led = SimpleNamespace(**data.get('led', defaults.led))
            logger.debug(f'Loaded LED configuration: {self.led}')

            self.button = SimpleNamespace(**data.get('button', defaults.button))
            logger.debug(f'Loaded button configuration: {self.button}')

            self.lcd = SimpleNamespace(**data.get('lcd', defaults.lcd))
            logger.debug(f'Loaded LCD configuration: {self.lcd}')
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
        return cls._instance

