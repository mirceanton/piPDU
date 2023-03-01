import utils.constants as constants
from pcf8574 import PCF8574
import requests

expanders = constants.get_expanders()

def update_led(index: int, expander: PCF8574, pin: int):
    print(f"DEBUG: Fetching state for socket {index}")

    # Update state from API server
    url = f"http://{constants.PIPDU_SERVER_ADDRESS}/api/v1/socket/{index}/info"
    response = requests.get(url)
    response.raise_for_status()
    state = bool( response.json()['payload']['state'] )

    # Update LED status
    expander.set_output(pin, not state)
    print(f"DEBUG: LED {index} state updated")

try:
    while True:
        for index, pin in enumerate(constants.LED_PINS):
            update_led(index, expanders[pin // 8], pin % 8)
except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')

