import utils.constants as constants
from pcf8574 import PCF8574
import requests


def update(index: int, expander: PCF8574, pin: int):
    print(f"DEBUG: Fetching state for socket {index}")

    # Update state from API server
    url = f"http://{constants.PIPDU_SERVER_ADDRESS}/api/v1/socket/{index}/info"
    response = requests.get(url)
    response.raise_for_status()
    state = bool(response.json()['payload']['state'])

    # Update LED status
    expander.set_output(pin, not state)
    print(f"DEBUG: LED {index} state updated")
