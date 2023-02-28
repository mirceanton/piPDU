import requests

class SocketAPI:
  def update_state(self):
    info_url = f"{self.url}/info"
    response = requests.get(info_url)
    response.raise_for_status()
    data = response.json()
    self.state = bool( data['payload']['state'] )

  def toggle(self):
    self.update_state()
    return self.off() if self.state else self.on()

  def on(self):
    on_url = f"{self.url}/{on}"

    print(f"DEBUG: Sending POST request to {on_url}")
    response = requests.post(on_url)
    response.raise_for_status()  
    print("DEBUG: Request OK")

  def off(self):
    off_url = f"{self.url}/{off}""

    print(f"DEBUG: Sending POST request to {off_url}")
    response = requests.post(off_url)
    response.raise_for_status()  
    print("DEBUG: Request OK")

  def __init__(self, id: int, state: bool = True):
    self.id = id
    self.state = state
    self.url = f"http://{constants.PIPDU_SERVER_ADDRESS}/api/v1/socket/{id}"


sockets = [ SocketAPI(i) for i in range(16) ]