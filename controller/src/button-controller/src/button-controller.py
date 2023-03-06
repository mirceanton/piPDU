from utils.button import buttons
from utils.socket import SocketAPI
import utils.constants as constants
import os
import time

print(f'INFO: Creating named pipe {constants.FIFO}')
if not os.path.exists(constants.FIFO):
    os.mkfifo(constants.FIFO)

print(f'INFO: Initializing PCF expanders')
expanders = constants.get_expanders()

print(f'INFO: Initializing buttons arrray')
buttons = []
for index, pin in enumerate(constants.BUTTON_PINS):
    btn = Button(
        index = index,
        expander = expanders[ pin // 8 ],
        pin = pin % 8,
    )
    buttons.append(btn)

print('INFO: Polling for button events...')
while True:
    for btn in buttons:
        btn.poll()
    time.sleep(constants.BUTTON_POLL_INTERVAL_SECONDS)