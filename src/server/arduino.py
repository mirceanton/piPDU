import serial
from config import Config
from metrics import Exporter


class Arduino:
    __instance = None   # Singleton instance of the Arduino class
    __conn = None       # Serial connection to the Arduino
    __device = Config().data['arduino']['device']   # Configured device file
    __baud = Config().data['arduino']['baud']       # Configured baud rate

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
            print("Info: Serial connection initialized OK")

    # Method for listening for data from the serial connection
    def listen(self):
        print('Info: Listening for data from serial...')
        while True:
            # Read data from the serial connection
            data = self.__conn.readline()

            # Log to console
            print('Info: Received data from serial: ', data)

            # Split the data on the separator string
            numbers = data.split(b',')

            # Convert the numbers to floats and store them in a list
            try:
                numbers = [float(n) for n in numbers]

                # Update Prometheus metrics
                Exporter().update(numbers)
            except Exception as ex:
                print(ex)

    # Method for writing data to the serial connection
    def write(self, msg):
        self.__conn.write(msg.encode())
        print('Info: Sent data over serial: ', msg)

    # Method for creating a singleton instance of the Arduino class
    def __new__(cls):
        # Create a new instance if another one doesn't already exist
        if Arduino.__instance is None:
            Arduino.__instance = object.__new__(cls)

        # Make sure the instance is connected
        if Arduino.__instance.__conn is None:
            Arduino.__instance.__connect()

        return Arduino.__instance
