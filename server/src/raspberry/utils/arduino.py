import serial
from config.config import Config
from utils.metrics import Exporter
from utils.logger import logger

class Arduino:
    """
    This is a singleton class meant to abstract away the interaction over serial with the Arduino.

    Attributes
    ----------

    serial_conn : serial.Serial()
        The serial connection object itself

    Methods
    -------
    listen() -> str:
        Listens for messages over the serial connection from the Arduino device.

    write(message : str) -> None:
        Send the given message over the serial connection to the Arduino device.

    connect():
        Establishes the serial connection to the Arduino based on the `device` and `baud` given from the Config singleton.  
        This function is called automatically when the first instance of the singleton is created.
    """

    def listen(self) -> str:
        """
        Listen for incoming messages over the serial connection from the Arduino.
        """
        logger.info('Listening for data from serial')
        data = self.serial_conn.readline()
        logger.info(f'Received data from serial: {data}')
        return data

    def write(self, message : str) -> None:
        """
        Send the gven message over the serial connection to the Arduino.

        Args:
            message (str): The data to send over serial
        """
        logger.info(f'Sending data over serial: {message}')
        try:
            bytes = self.serial_conn.write(message.encode())
            logger.info(f'Sent {bytes} bytes over serial: {message}')
        except SerialTimeoutException as ex:
            logger.error(f'Faield to send data over serial: {message}')

    def connect(self):
        """
        Initialize the Serial Connection.
        """
        logger.info("Initializing serial connection")
        print(Config().arduino)
        try:
            self.serial_conn = serial.Serial(Config().arduino.device, Config().arduino.baud)
            if self.serial_conn.is_open:
                logger.info("Serial connection is open.")
            else:
                logger.error("Failed to open serial connection.")
        except serial.SerialException as ex:
            logger.error("Failed to open serial connection to Arduino: The device can not be found or can not be configured.")
            logger.debug(ex)
        except ValueError as err:
            logger.error("Failed to open serial connection to Arduino: Parameters are out of range.")
            logger.debug(err)

    def __new__(cls):
        """
        Create/Retrieve the singleton instance
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new Arduino singleton instance')
            cls._instance = object.__new__(cls)
            cls._instance.connect()
        else:
            logger.debug('Reused the Arduino singleton instance')
        return cls._instance
