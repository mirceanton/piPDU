from common.arduino import Arduino
import yaml

class SocketArray:
  __instance = None
  sockets = []

  # Method for creating a singleton instance of the Config class
  def __new__(cls):
      if cls.__instance is None:
          cls.__instance = super().__new__(cls)
      return cls.__instance

  def __init__(self):
    if len(self.sockets) > 0:
      return

    with open('sockets.yaml') as file:
      data = yaml.load(file, Loader=yaml.FullLoader)
  
      for i in range(0, 16):
        sck = data[f"socket_{i}"] if f"socket_{i}" in data else {}
        self.sockets.append(Socket(
          id = i,
          name = sck['name'] if 'name' in sck else None,
          initState = sck['initState'] == "True" if 'initState' in sck else True
        ))

class Socket:
  id = None
  name = None
  initState = None
  state = None

  def __init__(self, id=0, name=None, initState=True):
    self.id = id
    self.name = name if name is not None else f"socket_{id}"
    self.initState = initState
    self.state = None

    if initState:
      self.turnOn()
    else:
      self.turnOff()

  def turnOn(self):
    if self.state:
      return 0

    Arduino().write(chr(self.id + 65)) # 65 is the ASCII code for "A"
    self.state = True
    return 1

  def turnOff(self, force=False):
    if self.state is False:
      return 0

    Arduino().write(chr(self.id + 97)) # 97 is the ASCII code for "a"
    self.state = False
    return 1

  def info(self):
    return {
      "id": self.id,
      "name": self.name,
      "state": self.state,
      "initial_state": self.initState,
    }