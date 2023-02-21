import utils.constants as constants
import serial

class Arduino:
    def __init__(self):
        try:
            self.ser = serial.Serial(constants.SERIAL_DEVICE, constants.SERIAL_BAUDRATE)
            print("INFO: Serial connection initialized")
        except serial.SerialException as err:
            print(f'ERROR: Could not connect to serial device: {err}')
            exit(1)

    def read(self):
        if (self.ser.in_waiting <= 0):
            return None

        message = self.ser.readline().decode('utf-8').rstrip()
        print(f'INFO: Got message from serial: {message}')

        return message

    def write(self, message: str):
        self.ser.write(bytes(message, 'utf-8'))
        print(f'INFO: Sent message over serial: {message}')

    def close(self):
        print(f'INFO: Closing the serial connection.')
        self.ser.close()
