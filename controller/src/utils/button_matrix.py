from config.config import Config
from utils.logger import logger
from utils.button import Button
import RPi.GPIO as GPIO

class ButtonMatrix:
    """
    This is a singleton class meant to abstract away the logic for the button matrix.

    Attributes
    ----------

    buttons : list<Button>
        The list of button objects

    Methods
    -------

    poll() -> None:
        Polls the matrix for button press events and triggers the required actions.

    setup() -> None:
        Sets up the pins for the button matrix and creates 16 Button instances.  
        This function is called automatically when the first instance of the singleton is created.
    """

    def poll(self) -> None:
        """
        Poll the button matrix for button press events.
        """
        logger.debug('Polling button matrix')
        for col in Config().btnArray.colPins:
            GPIO.output(col, GPIO.HIGH) 

            for row in Config().btnArray.rowPins:
                # Calculate the button index
                row_index = Config().btnArray.rowPins.index(row)
                col_index = Config().btnArray.colPins.index(col)
                btn_index = row_index * 8 + col_index
                btn_value = GPIO.input(row)
                logger.debug(f"Button {btn_index} at row {row_index} and column {col_index} is {btn_value}")

                self.buttons[btn_index].poll(btn_value)

            GPIO.output(col, GPIO.LOW)

    def setup(self):
        """
        Initialize the buttons array and the pins used for the button matrix
        """
        logger.debug("Setting column pins as outputs")
        for pin in Config().btnArray.colPins:
            GPIO.setup(pin, GPIO.OUT)

        logger.debug("Setting row pins as inputs")
        for pin in Config().btnArray.rowPins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        logger.debug("Initializing ButtonMatrix button array")
        self.buttons = [Button(i) for i in range(0, 16)]

    def __new__(cls):
        """
        Create a singleton instance of the ButtonMatrix class.
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new ButtonMatrix singleton instance')
            cls._instance = object.__new__(cls)
            cls._instance.setup()
        else:
            logger.debug('Reused the ButtonMatrix singleton instance')
        return cls._instance
