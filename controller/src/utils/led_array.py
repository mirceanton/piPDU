import requests
import json
from config.config import Config
from utils.logger import logger
from utils.led import Led


class LedArray:
    """
    This is a singleton class meant to abstract away the logic for the LED Array.

    Attributes
    ----------

    leds : list<Led>
        The list of Led objects

    Methods
    -------

    update() -> None:
        Sends GET requests to the status endpoint for each socket on the API server and updates the LED status.

    setup() -> None:
        Sets up the pins for the LED array and creates 16 LED instances.  
        This function is called automatically when the first instance of the singleton is created.
    """

    def update(self):
        """
        Update LED status based on relay status
        """
        logger.info("Updating LED Array")
        for index, led in enumerate(self.leds):
            url = f"http://{Config().api.host}:{Config().api.port}/api/v1/socket/{index}/info"

            logger.debug(f"Sending get request to {url}")
            response = requests.get(url)
            
            if response.status_code != 200:
                logger.error("Failed to query status endpoint")
                logger.debug(f"Response code was {response.status_code} and not 200")
                logger.debug(response)
                return
            json_data = json.loads(response.text)
            logger.debug(json_data)
            led.setState(json_data['payload']['state'])

    def setup(self):
        """
        Initialize the LEDs by configuring the pins as outputs and setting them to LOW
        """
        logger.debug("Initializing LED array")
        self.leds = [Led(i, Config().led.pins[i]) for i in range(0, 16)]

    def __new__(cls):
        """
        Create a singleton instance of the LedArray class.
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new LedArray singleton instance')
            cls._instance = object.__new__(cls)
            cls._instance.setup()
        else:
            logger.debug('Reused the LedArray singleton instance')
        return cls._instance
