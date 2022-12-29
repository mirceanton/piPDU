from utils.arduino import Arduino
from utils.logger import logger
import subprocess
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
            `-2` if the post action hook failed but the socket has been turned on
            `-1` if the pre action hook failed, so the socket has not been turned on
            `1` if the socket state has changed
            `0` if there was nothing to do.

    turnOff() -> int:
        If the socket is currently on, send a command over serial to the arduino via the Arduino singleton to turn off the socket.  

        Returns:
            `-2` if the post action hook failed but the socket has been turned off
            `-1` if the pre action hook failed, so the socket has not been turned off
            `1` if the socket state has changed
            `0` if there was nothing to do.

    toggle() -> None:
        If the socket is currently on, turn it off and vice versa.

    info() -> dict:
        Returns information about the socket in a dictionary format.
    """

    def turnOn(self) -> int:
        """
        Turns the socket on.
        """
        if self.executeHook(self.prePowerOnHook, "pre power on") != 0:
            return -1

        logger.info(f"Turning socket {self.id} on.")
        if self.state:
            logger.info(f"Socket {self.id} is already on.")
            return 0

        Arduino().write(chr(self.id + 65)) # 65 is the ASCII code for "A"
        self.state = True
        logger.info(f"Socket {self.id} turned on.")

        if self.executeHook(self.postPowerOnHook, "post power on") != 0:
            return -2

        return 1

    def turnOff(self) -> int:
        """
        Turns the socket off.
        """
        if self.executeHook(self.prePowerOffHook, "pre power off") != 0:
            return -1

        logger.info(f"Turning socket {self.id} off.")
        if self.state is False:
            logger.info(f"Socket {self.id} is already off.")
            return 0

        Arduino().write(chr(self.id + 97)) # 97 is the ASCII code for "a"
        self.state = False
        logger.info(f"Socket {self.id} turned off.")

        if self.executeHook(self.postPowerOffHook, "post power off") != 0:
            return -2

        return 1

    def executeHook(self, hook: list, name: str) -> int:
        logger.info(f"Executing hook {name} for socket {self.id}")
        return_code = subprocess.run(hook['command'])

        if return_code == 0:
            logger.info(f"Hook {name} executed successfuly.")
            return 0

        if hook['ignoreErrors']: # return code is not 0
            logger.info(f"Hook {name} for socket {self.id} failed but ignoreErrors is set to `True`.")
            return 0

        logger.error(f"Hook {name} failed for socket {self.id} and ignoreErrors is set to `False`. Aborting power off.")
        return 1

    def toggle(self) -> None:
        """
        Toggles the socket.
        """
        logger.info(f"Toggling socket {self.id} off.")
        logger.debug(f"Current state for socket {self.id} is {self.state}")
        if self.state:
            self.turnOff()
        else:
            self.turnOff()

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

    def __init__(self, id=0, name=None, initState=True, prePowerOnHook={}, postPowerOnHook={}, prePowerOffHook={}, postPowerOffHook={}):
        """Create a new socket object"""
        self.id = id
        self.name = name if name is not None else f"socket_{id}"
        self.initState = initState
        self.state = None
        self.prePowerOnHook = prePowerOnHook
        self.postPowerOnHook = postPowerOnHook
        self.prePowerOffHook = prePowerOffHook
        self.postPowerOffHook = postPowerOffHook

        # Handle the initial state of the socket
        if initState:
            self.turnOn()
        else:
            self.turnOff()