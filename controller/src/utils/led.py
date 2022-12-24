import RPi.GPIO as GPIO
from utils.logger import logger

class Led:
    """
    This is a class meant to abstract away the logic required for handling LEDs.

    Attributes
    ----------

    index : int
        The index of the button.

    pin : int
        The pin number for the LED.

    state : bool
        Whether or not the LED is currently on.

    Methods
    -------

    turnOn() -> None:
        Turns the LED on.
        
    turnOff() -> None:
        Turns the LED off.
    
    setState(state: bool):
        Sets the LED to the given state.
    """

    def turnOn(self) -> None:
        """
        Turn on the LED by setting the GPIO to HIGH
        """
        logger.info(f"Turning LED {self.index} ON")
        self.state = True
        GPIO.output(self.pin, GPIO.HIGH)

    def turnOff(self) -> None:
        """
        Turn on the LED by setting the GPIO to LOW
        """
        logger.info(f"Turning LED {self.index} OFF")
        self.state = False
        GPIO.output(self.pin, GPIO.LOW)

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

    def __init__(self, index: int, pin: int, state = False):
        logger.debug(f"Initializing LED {index}")
        self.index = index
        self.pin = pin
        self.state = None

        GPIO.setup(pin, GPIO.OUT)
        logger.info(f"Pin {pin} configured as output")
        GPIO.output(pin, GPIO.LOW)
        logger.info(f"Pin {pin} set to LOW")

        self.setState(state)
