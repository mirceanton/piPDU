import RPi.GPIO as GPIO
from utils.logger import logger
from utils.expanders import expanders

class Led:
    """
    This is a class meant to abstract away the logic required for handling LEDs.

    Attributes
    ----------

    index : int
        The index of the button.

    expander : PCF8574
        The PCF8574 device that this LED is connected to

    pin_name : str
        The name of the pin on the PCF device, as interpreted by the pcf8574_io library

    state : bool
        Whether or not the LED is currently on.

    Methods
    -------

    turnOn() -> None:
        Turns the LED on.
        
    turnOff() -> None:
        Turns the LED off.
    
    setState(state: bool) -> None:
        Sets the LED to the given state.
    """

    def turnOn(self) -> None:
        """
        Turn on the LED by setting the GPIO to HIGH
        """
        logger.info(f"Turning LED {self.index} ON")
        self.state = True
        self.expander.write(self.pin_name, "LOW")

    def turnOff(self) -> None:
        """
        Turn on the LED by setting the GPIO to LOW
        """
        logger.info(f"Turning LED {self.index} OFF")
        self.state = False
        self.expander.write(self.pin_name, "HIGH")

    def setState(self, state: bool):
        """
        Set the state of the LED to the given value
        """
        logger.info(f"Setting LED {self.index} state to {state}")
        if self.state == state:
            logger.info(f"LED is already in the desired state")
            return

        if state:
            return self.turnOn()
        return self.turnOff()

    def __init__(self, index: int, expander_id: int, pin_id: int):
        logger.debug(f"Initializing LED {index}")
        self.index = index
        self.expander = expanders[expander_id]
        self.pin_name = f"p{pin_id}"
        self.state = None

        self.expander.pin_mode(self.pin_name, "OUTPUT")

        self.setState(False)
