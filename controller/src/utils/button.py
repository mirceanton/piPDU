from utils.lcd import LCD, LCDStates
from config.config import Config
from utils.logger import logger
import RPi.GPIO as GPIO
import datetime
import requests

class Button:
    """
    This is a class meant to abstract away the logic required for handling buttons.

    Attributes
    ----------

    index : int
        The index of the button.

    current_state : bool
        The current state of the button. True means the button is pressed, False means it is not.

    old_state : bool
        The previous state of the button. True means the button is pressed, False means it is not.

    last_press_time : int
        The time the button was last pressed

    Methods
    -------

    poll(value : int) -> None:
        Updates the states (current and old) of the button based on the given value;  
        Checks if the button is being pressed/held/released and takes the appropriate action.

    short_press() -> None:
        Executes the short press action. -> Puts the LCD in the info state

    long_press() -> None:
        Executes the long press action. -> Toggles the state of the socket and puts the LCD in idle

    is_pressed() -> bool:
        Checks if the button has been pressed or not.

    is_held() -> bool:
        Checks if the button is being held or not.

    is_released() -> bool:
        Checks if th ebutton has been released or not.

    held_threshold_passed() -> bool:
        Checks if the amount of time for which the button has been held down is longer than the long press threshold.    
    """

    def poll(self, value: int) -> None:
        """
        Poll the button for a press event; either a long press or a short press.
        
        Parameters:
        value (int): The current value of the button.
        """
        logger.debug(f"Updating button {self.index} status.")
        self.old_state = self.current_state
        logger.debug(f"Button {self.index} old state: {self.old_state}")

        self.current_state = value == GPIO.HIGH
        logger.debug(f"Button {self.index} current state: {self.current_state}")

        # If the button has now been pressed, record the time
        if self.is_pressed():
            logger.info(f"Button {self.index} pressed.")
            self.last_press_time = datetime.datetime.now()

        # If the button is currently being held and has been held for longer
        # than the long press threshold, execute the long_press action
        if self.is_held() and self.held_threshold_passed():
            logger.info(f"Button {self.index} held.")
            self.long_press()

        # If the button has been released, check if the long press threshold
        # has been triggered or not and reset the time
        if self.is_released():
            logger.info(f"Button {self.index} released.")
            self.last_press_time = None
            if not self.held_threshold_passed():
                self.short_press()

    def short_press(self) -> None:
        """
        Execute the action for a short press of the button.
        """
        logger.debug(f"Executing short press action for button {self.index}")
        LCD().setState(self.index)

    def long_press(self) -> None:
        """
        Execute the action for a long press of the button.
        """
        logger.debug(f"Executing long press action for button {self.index}")

        logger.debug(f"Sending POST request to {self.url}")
        resp = requests.post(self.url)

        if (resp.status_code != 200):
            logger.warn("Request failed")
            return
        logger.info(f"Request for button {self.index} OK")
        logger.debug(resp)
        LCD().setState(LCDStates.IDLE)

    def is_pressed(self) -> bool:
        """
        Return True if the button has just been pressed, False otherwise.
        """
        return self.current_state is True and self.old_state is False

    def is_held(self) -> bool:
        """
        Return True if the button is being held down, False otherwise.
        """
        return self.current_state is True and self.old_state is True

    def is_released(self) -> bool:
        """
        Return True if the button has just been released, False otherwise.
        """
        return self.current_state is False and self.old_state is True

    def held_threshold_passed(self) -> bool:
        """
        Return True if the button has been held down for longer than the long press threshold, False otherwise.
        """
        if self.last_press_time is None:
            return False
        time_held = (datetime.datetime.now() - self.last_press_time).total_seconds()
        return time_held > Config().btnArray.longPressDurationSeconds

    def __init__(self, index, current_state=False, old_state=False, time=0):
        """
        Initialize a Button object with the given index, current state, old state, and time.
        
        Parameters:
            index (int): The index of the button.
            current_state (bool): The current state of the button. Defaults to False.
            old_state (bool): The previous state of the button. Defaults to False.
            time (int): The time the button was last pressed. Defaults to 0.
        """
        logger.debug(f"Initializing button {index}")
        self.index = index
        self.current_state = current_state
        self.old_state = old_state
        self.last_press_time = time
        self.url = f"http://{Config().api.host}:{Config().api.port}/api/v1/socket/{self.index}/toggle"
