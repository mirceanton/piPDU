import RPi.GPIO as GPIO
from common.config import Config
import datetime
import requests
from common.lcd import LCD, LCDStates

class ButtonMatrix:
    # Singleton instance of the ButtonMatrix class
    __instance = None

    # Store the current and previous states of each button in the matrix
    __old_states = [False] * 16
    __cur_state = [False] * 16

    # Store the time at which each button was pressed
    __times = [0.0] * 16

    def poll(self):
        # Update old state = state
        for index, state in enumerate(self.__cur_state):
            self.__old_states[index] = state

        for col in Config().btnArray.colPins:
            GPIO.output(col, GPIO.HIGH)

            for row in Config().btnArray.rowPins:
                # Calculate the button index
                row_index = Config().btnArray.rowPins.index(row)
                col_index = Config().btnArray.colPins.index(col)
                btn_index = row_index * 8 + col_index

                # Update the current state of the button
                self.__cur_state[btn_index] = ( GPIO.input(row) == GPIO.HIGH )

                # If the button has just been pressed, record the time
                if self.__cur_state[btn_index] is True and self.__old_states[btn_index] is False:
                    self.__times[btn_index] = datetime.datetime.now()

                # If the button has been released, see for how long it has been pressed
                if self.__cur_state[btn_index] is False and self.__old_states[btn_index] is True:
                    time_held = (datetime.datetime.now() - self.__times[btn_index]).total_seconds()
                    if time_held >  Config().btnArray.longPressDurationSeconds:
                        self.__long_press(btn_index)
                    else:
                        self.__short_press(btn_index)

            GPIO.output(col, GPIO.LOW)

    # Handle a long press on one of the buttons -> toggle relay
    def __long_press(self, index):
        resp = requests.post(f"http://{Config().api.host}:{Config().api.port}/api/v1/sockets/{index}")
        print(resp)
        LCD().setState(LCDStates.IDLE) # idle

    # Handle a short press on one of the buttons -> set LCD to info
    def __short_press(self, index):
        LCD().setState(index)

    # Initialize the pins used for the button matrix
    def __init__(self):
        for pin in Config().btnArray.colPins:
            GPIO.setup(pin, GPIO.OUT)

        for pin in Config().btnArray.rowPins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Method for creating a singleton instance of the ButtonMatrix class
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
