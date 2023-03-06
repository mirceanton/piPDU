import utils.constants as constants
import requests

def __get_state(id : int) -> bool:
    info_url = f"http://{constants.PIPDU_SERVER_ADDRESS}/api/v1/socket/{id}/info"
    response = requests.get(info_url)
    response.raise_for_status()
    data = response.json()
    return bool( data['payload']['state'] )

def __turn_on(id : int):
    on_url = f"http://{constants.PIPDU_SERVER_ADDRESS}/api/v1/socket/{id}/on"
    print(f"DEBUG: Sending POST request to {on_url}")
    response = requests.post(on_url)
    response.raise_for_status()
    print("DEBUG: Request OK")

def __turn_off(id : int):
    off_url = f"http://{constants.PIPDU_SERVER_ADDRESS}/api/v1/socket/{id}/off"
    print(f"DEBUG: Sending POST request to {off_url}")
    response = requests.post(off_url)
    response.raise_for_status()
    print("DEBUG: Request OK")

def toggle(id : int):
  if __get_state(id) == True:
    __turn_off(id)
  else:
    __turn_on(id)
