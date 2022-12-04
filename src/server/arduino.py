import serial
from config import Config


class Arduino:
    __instance = None
    __device = Config().data['arduino']['device']
    __baud = Config().data['arduino']['baud']
    __conn = None

    def connect(self):
      print("Info: Initializing serial connection...")
      self.__conn = serial.Serial(self.__device, self.__baud)

      # Check if serial connection is open
      if not self.__conn.is_open:
          # Raise an exception with a custom error message if the connection is not open
          raise Exception('Error: Failed to open serial connection to Arduino')
      else:
          print("Serial connection initialized OK")

    def listen(self):
      while True:
        # Read data from the serial connection
        data = self.__conn.readline()

        # Split the data on the separator string
        numbers = data.split(b',')

        # Convert the numbers to integers and store them in a list
        numbers = [float(n) for n in numbers]

        print('Received data from serial: ', numbers)

    def __new__(cls):
        if Arduino.__instance is None:
            Arduino.__instance = object.__new__(cls)
        return Arduino.__instance
