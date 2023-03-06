import utils.constants as constants
from utils.metrics import scrape_metrics
from utils.display import Display, DisplayState
import time
import json
import os

print(f'DEBUG: Initializing LCD display')
display = Display(
    expander=constants.DISPLAY_I2C_EXPANDER,
    i2c_bus=constants.DISPLAY_I2C_BUS,
    i2c_address=constants.DISPLAY_I2C_ADDR,
    backlight=constants.DISPLAY_BACKLIGHT_ENABLED
)

print(f'DEBUG: Creating named pipe {constants.FIFO}')
if not os.path.exists(constants.FIFO):
    os.mkfifo(constants.FIFO)

print(f'DEBUG: Opening named pipe in read-only mode')
pipe = open(constants.FIFO, 'r')


def pipe_message_callback(body):
    if len(body) == 0:
        return

    print(f'DEBUG: Got message from pipe: {body}')
    data = json.loads(body)
    print(f'DEBUG: Parsed JSON as: {data}')

    state = DisplayState[data['state'].upper()]
    socket = int(data['socket']) if 'socket' in data else None

    if state == DisplayState.IDLE and socket is not None:
        raise ValueError(
            f'Poorly formatted message; No socket should be set for IDLE state: {data}')

    if state == DisplayState.INFO and not (0 <= socket < 16):
        raise ValueError(
            f'Poorly formatted message; Invalid socket number for INFO state: {data}')

    display.set_state(state, socket)


print(f'INFO: Starting main loop')
try:
    while True:
        pipe_message_callback(pipe.read())
        display.update(scrape_metrics(constants.METRICS_ENDPOINT_URL))
        time.sleep(constants.METRICS_POLL_INTERVAL_SECONDS)
except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')
    display.close()
    pipe.close()
