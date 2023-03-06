import utils.constants as constants
import utils.socket as socket
from pcf8574 import PCF8574
import datetime
import os

class Button:
    def poll(self) -> None:
        self.old_state = self.current_state
        self.current_state = self.expander.get_pin_state(self.pin)

        # If the button has now been pressed, record the time
        if self.__is_pressed():
            print(f"DEBUG: Button {self.index} pressed.")
            self.last_press_time = datetime.datetime.now()

        # If the button is currently being held and has been held for longer
        # than the long press threshold, execute the __execute_long_press action
        if self.__is_held() and self.__held_threshold_passed():
            print(f"DEBUG: Button {self.index} held.")
            self.__execute_long_press()
            self.last_press_time = None

        # If the button has been released, check if the long press threshold
        # has been triggered or not and reset the time
        if self.__is_released():
            print(f"DEBUG: Button {self.index} released.")
            if not self.__held_threshold_passed():
                self.__execute_short_press()
                self.last_press_time = None

    def __execute_short_press(self) -> None:
        print(f"INFO: Executing short press action for button {self.index}")
        with open(constants.FIFO, 'w') as pipe:
            pipe.write(f'{"state": "INFO", "socket": "{self.index}"}')
            pipe.close()

    def __execute_long_press(self) -> None:
        print(f"INFO: Executing long press action for button {self.index}")
        socket.toggle(self.index)

    def __is_pressed(self) -> bool:
        return self.current_state is True and self.old_state is False

    def __is_held(self) -> bool:
        return self.current_state is True and self.old_state is True

    def __is_released(self) -> bool:
        return self.current_state is False and self.old_state is True

    def __held_threshold_passed(self) -> bool:
        if self.last_press_time is None:
            return False
        time_held = (datetime.datetime.now() - self.last_press_time).total_seconds()
        return time_held > constants.BUTTON___execute_long_press_DURATION_SECONDS

    def __init__(self, index: int, expander: PCF8574, pin: int):
        print(f"DEBUG: Initializing button {index}")
        self.index = index
        self.expander = expander
        self.pin = pin
        self.current_state = False
        self.old_state = False
        self.last_press_time = None

        # Initialize the pin by setting it to LOW as it is HIGH by default??
        self.expander.set_output(self.pin, False)
