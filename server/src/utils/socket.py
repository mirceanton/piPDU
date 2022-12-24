from utils.arduino import Arduino
from utils.logger import logger
import yaml

class Socket:
    """
    This is a class meant to abstract away the interaction with the actual power sockets.

    Attributes
    ----------

    id : int
        The numeric id of the socket as shown in the PiPDU server diagram

    name: str
        A friendly name for the socket to indicate what is connected to it

    initState: bool
        Whether or not the socket should be on by default or not.
    
    state: bool
        The current on/off state of the socket

    Methods
    -------

    turnOn() -> int:
        If the socket is currently off, send a command over serial to the arduino via the Arduino singleton to turn on the socket.  

        Returns:
            `1` if the socket state has changed
            `0` if there was nothing to do.

    turnOff() -> int:
        If the socket is currently on, send a command over serial to the arduino via the Arduino singleton to turn off the socket.  

        Returns:
            `1` if the socket state has changed
            `0` if there was nothing to do.

    info() -> dict:
        Returns information about the socket in a dictionary format.
    """

    def turnOn(self):
        """
        Turns the socket on.
        """
        logger.info(f"Turning socket {self.id} on.")
        if self.state:
            logger.info(f"Socket {self.id} is already on.")
            return 0

        Arduino().write(chr(self.id + 65)) # 65 is the ASCII code for "A"
        self.state = True
        logger.info(f"Socket {self.id} turned on.")
        return 1

    def turnOff(self, force=False):
        """
        Turns the socket off.
        """
        logger.info(f"Turning socket {self.id} off.")
        if self.state is False:
            logger.info(f"Socket {self.id} is already off.")
            return 0

        Arduino().write(chr(self.id + 97)) # 97 is the ASCII code for "a"
        self.state = False
        logger.info(f"Socket {self.id} turned off.")
        return 1

    def info(self):
        """
        Return a dictionary containing information on the socket.
        """
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "initial_state": self.initState,
        }

    def __init__(self, id=0, name=None, initState=True):
        """Create a new socket object"""
        self.id = id
        self.name = name if name is not None else f"socket_{id}"
        self.initState = initState
        self.state = None

        # Handle the initial state of the socket
        if initState:
            self.turnOn()
        else:
            self.turnOff()