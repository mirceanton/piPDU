from config.config import Config
from utils.logger import logger
from utils.button import Button

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
        for btn in self.buttons:
            btn.poll()

    def setup(self):
        """
        Initialize the buttons array and the pins used for the button matrix
        """
        self.buttons = []
        for pin_index, pin_number in enumerate(Config().button.pins):
            self.buttons.append(
                Button(
                    index = pin_index,
                    expander_id = pin_number // 8,
                    pin_id = pin_number % 8,
                )
            )

    def __new__(cls):
        """
        Create a singleton instance of the ButtonMatrix class.
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new ButtonMatrix singleton instance')
            cls._instance = object.__new__(cls)
            cls._instance.setup()
        return cls._instance
