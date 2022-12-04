import serial
from config import Config


class Arduino:
    # Singleton instance of the Arduino class
    __instance = None

    # Configured device and baud rate
    __device = Config().data['arduino']['device']
    __baud = Config().data['arduino']['baud']

    # Serial connection to the Arduino
    __conn = None

    # Method for initializing the serial connection
    def __connect(self):
        print("Info: Initializing serial connection...")

        # Open the serial connection
        self.__conn = serial.Serial(self.__device, self.__baud)

        # Check if the serial connection is open
        if not self.__conn.is_open:
            # Raise an exception with a custom error message if the connection is not open
            raise Exception(
                'Error: Failed to open serial connection to Arduino')
        else:
            print("Serial connection initialized OK")

    # Method for listening for data from the serial connection
    def listen(self):
        while True:
            # Read data from the serial connection
            data = self.__conn.readline()

            # Split the data on the separator string
            numbers = data.split(b',')

            # Convert the numbers to floats and store them in a list
            numbers = [float(n) for n in numbers]

            print('Received data from serial: ', numbers)

    # Method for creating a singleton instance of the Arduino class
    def __new__(cls):
        # Create a new instance if another one doesn't already exist
        if Arduino.__instance is None:
            Arduino.__instance = object.__new__(cls)

        # Make sure the instance is connected
        if Arduino.__instance.__conn is None:
            Arduino.__instance.__connect()

        return Arduino.__instance
