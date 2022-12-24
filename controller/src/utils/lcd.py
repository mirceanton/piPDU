from utils.metrics import Metrics
from utils.logger import logger
from config.config import Config
from enum import Enum
from RPLCD.i2c import CharLCD

class LCDStates(Enum):
    """
    An enum representing the possible states for the LCD display.
    """
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

class LCD:
    """
    A wrapper class around the RPLCD.i2c.CharLCD implemented as a singleton.

    This class provides methods for updating and setting the state of the LCD display.

    Attributes
    ----------

    device : CharLCD
        The CharLCD object instance for the LCD display.

    state : LCDStates
        The current state of the display

    Methods
    -------

    update() -> None
        Updates the actual text printed on the display based on the current state

    set_state(state : LCDStates) -> None
        Modify the current state of the display

    idle_state() -> None
        Show generic information about the PDU as a whole on the LCD display.  
        Called by the update() method.

    info_state(id : int) -> None
        Show information about a specific socket on the LCD.  
        Called by the update() method.

    setup(): -> None
        Initialize the CharLCD device.  
        This function is called automatically when the first instance of the singleton is created.
    """
    device : CharLCD = None
    state : LCDStates = None

    def update(self) -> None:
        """
        Update the text on the LCD based on the current state.
        """
        logger.debug("Updating LCD.")
        if self.state == LCDStates.IDLE:
            self.idle_state()
        else:
            self.info_state(self.state)

    def set_state(self, state : LCDStates) -> None:
        """
        Set the state of the LCD display.

        If the state is already set, the display is set to the idle state. Otherwise, the state is set to the specified value.

        Args:
            state (LCDStates): The state to set the display to.
        """
        logger.info(f"LCD state change to {state} requested.")
        logger.debug(f"Current LCD state is {self.state}")
        if (self.state == state):
            logger.info(f"New state is the same as the current state -> defaulting to IDLE state ({LCDStates.IDLE})")
            self.state = LCDStates.IDLE
        else:
            logger.info(f"LCD State changed to {state}")
            self.state = state

    def idle_state(self) -> None:
        """
        Show info about the PDU as a whole.
        """
        logger.debug("Executing LCD IDLE State")
        with self.device as dev:
            dev.clear()
            dev.write_string("       Pi PDU       ")
            dev.crlf()
            dev.crlf()
            dev.write_string(f"Current: {Metrics().total} A")
            dev.crlf()
            dev.write_string(f"Power: {Metrics().total * 220} W")

    def info_state(self, id : int) -> None:
        """
        Show info about a given socket on the LCD display.

        Args:
            id (int): The id of the socket to show info for.
        """
        logger.debug(f"Executing LCD INFO State {id}")
        with self.device as dev:
            dev.clear() # Clear the current contents
            dev.write_string(f"Socket {id}: ")
            dev.crlf()
            dev.crlf()
            dev.write_string(f"Current: {Metrics().metrics[id]} A")
            dev.crlf()
            dev.write_string(f"Power: {Metrics().metrics[id] * 220} W")

    def setup(self):
        """
        Initialize the LCD display.
        """
        logger.debug("Initializing LCD object.")
        self.device = CharLCD(
            i2c_expander = Config().lcd.expander,
            address = Config().lcd.address,
            port = Config().lcd.port,
            backlight_enabled = Config().lcd.backlight,
        )

    def __del__(self):
        """
        Clean up by closing the display.
        """
        logger.debug("Clearing and closing LCD object.")
        if self.device is not None:
            self.device.close(clear = True)

    def __new__(cls):
        """
        Create/Retrieve the singleton instance
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new LCD singleton instance')
            cls._instance = object.__new__(cls)
            cls._instance.setup()
        else:
            logger.debug('Reused the LCD singleton instance')
        return cls._instance

