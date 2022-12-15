from common.metrics import Metrics
from common.config import Config
from enum import Enum
from RPLCD.i2c import CharLCD

class LCDStates(Enum):
    IDLE = -1
    SCK0 = 0
    SCK1 = 1
    SCK2 = 2
    SCK3 = 3
    SCK4 = 4
    SCK5 = 5
    SCK6 = 6
    SCK7 = 7
    SCK8 = 8
    SCK9 = 9
    SCK10 = 10
    SCK11 = 11
    SCK12 = 12
    SCK13 = 13
    SCK14 = 14
    SCK15 = 15

# Wrapper class around the RPLCD.i2c.CharLCD implemented as a singleton
class LCD:
    __instance = None
    __device : CharLCD = None
    __state : int = -1

    def update(self):
        if self.__state == -1:
            self.idle()
        else:
            self.__info(self.__state)

    def setState(self, state : LCDStates):
        if (self.__state == state):
            self.__state = LCDStates.IDLE
        else:
            self.__state = state

    # Put the LCD into idle state
    def __idle(self):
        with self.__device as dev:
            dev.clear()
            dev.write_string("       Pi PDU       ")
            dev.crlf()
            dev.crlf()
            dev.write_string(f"Current: {Metrics().total} A")
            dev.crlf()
            dev.write_string(f"Power: {Metrics().total * 220} W")

    # Show info about a given socket on the LCD
    def __info(self, id):
        with self.__device as dev:
            dev.clear()
            dev.write_string(f"Socket {id}: ")
            dev.crlf()
            dev.crlf()
            dev.write_string(f"Current: {Metrics().metrics[id]} A")
            dev.crlf()
            dev.write_string(f"Power: {Metrics().metrics[id] * 220} W")

    # Initialize the LCD display
    def __init__(self):
        self.__device = CharLCD(
            i2c_expander = Config().lcd.expander,
            address = Config().lcd.address,
            port = Config().lcd.port,
            backlight_enabled = Config().lcd.backlight,
        )

    # Clean up by closing the display
    def __del__(self):
        self.__device.close(clear = True)

    # Method for creating a singleton instance of the LCD class
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
