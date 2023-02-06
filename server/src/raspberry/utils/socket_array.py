from utils.socket import Socket
from utils.logger import logger
import yaml
import os

class SocketArray:
    """
    This is a singleton class meant to cache the array of Socket objects and expose them globally.

    Attributes
    ----------

    sockets : list<Socket>
        The list of socket objects

    Methods
    -------

    setup():
        Parses the sockets.yaml configuration file and creates the socket objects.
    """
    sockets = []
    file_path = "sockets.yaml"

    def setup(self):
        """
        Initialize the sockets list
        """
        data = {}
        logger.info("Parsing sockets file")
        if os.path.exists(self.file_path):
            data = yaml.load(open(self.file_path), Loader=yaml.FullLoader)
            logger.info("Sockets file parsed.")
            logger.debug(data)
        else:
            logger.info("No sockets file found. Assuming defaults.")

        logger.info("Creating socket objects.")
        for i in range(0, 16):
            sck = data[f"socket_{i}"] if f"socket_{i}" in data else {}
            self.sockets.append(Socket(
                id = i,
                name = sck.get('name', None),
                initState = sck.get('initState', "True") == "True",
                prePowerOnHook = sck.get('prePowerOnHook', {}),
                postPowerOnHook = sck.get('postPowerOnHook', {}),
                prePowerOffHook = sck.get('prePowerOffHook', {}),
                postPowerOffHook = sck.get('postPowerOffHook', {}),
            ))

    def __new__(cls):
        """
        Create/Retrieve the singleton instance
        """
        if not hasattr(cls, '_instance'):
            logger.debug('Created a new SocketArray singleton instance')
            cls._instance = object.__new__(cls)
            cls._instance.setup()
        else:
            logger.debug('Reused the SocketArray singleton instance')
        return cls._instance
