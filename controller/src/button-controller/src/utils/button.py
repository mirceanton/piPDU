import utils.constants as constants
from utils.socket import sockets
from pcf8574 import PCF8574
import datetime

class Button:
    def poll(self) -> None:
        self.old_state = self.current_state
        self.current_state = self.expander.get_pin_state(self.pin)

        # If the button has now been pressed, record the time
        if self.is_pressed():
            print(f"INFO: Button {self.index} pressed.")
            self.last_press_time = datetime.datetime.now()

        # If the button is currently being held and has been held for longer
        # than the long press threshold, execute the long_press action
        if self.is_held() and self.held_threshold_passed():
            print(f"INFO: Button {self.index} held.")
            self.long_press()

        # If the button has been released, check if the long press threshold
        # has been triggered or not and reset the time
        if self.is_released():
            print(f"INFO Button {self.index} released.")
            self.last_press_time = None
            if not self.held_threshold_passed():
                self.short_press()

    def short_press(self) -> None:
        print(f"DEBUG: Executing short press action for button {self.index}")
        # TODO set LCD status to INFO/IDLE

    def long_press(self) -> None:
        print(f"DEBUG:Executing long press action for button {self.index}")
        self.socket.toggle()

    def is_pressed(self) -> bool:
        return self.current_state is True and self.old_state is False

    def is_held(self) -> bool:
        return self.current_state is True and self.old_state is True

    def is_released(self) -> bool:
        return self.current_state is False and self.old_state is True

    def held_threshold_passed(self) -> bool:
        if self.last_press_time is None:
            return False
        time_held = (datetime.datetime.now() - self.last_press_time).total_seconds()
        return time_held > constants.BUTTON_LONG_PRESS_DURATION_SECONDS

    def __init__(self, index: int, expander: PCF8574, pin: int):
        print(f"DEBUG: Initializing button {index}")
        self.index = index
        self.expander = expander
        self.pin = pin
        self.current_state = False
        self.old_state = False
        self.last_press_time = 0
        self.socket = sockets[index]

        # Initialize the pin by setting it to LOW as it is HIGH by default??
        self.expander.set_output(self.pin, False)
