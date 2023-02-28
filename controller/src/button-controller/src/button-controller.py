from pcf8574 import PCF8574
import time
import utils.constants as constants
from utils.button import Button

buttons = [ Button(index, expanders[pin // 8], pin % 8) for index, pin in enumerate(constants.BUTTON_PINS ]

print("Polling...")
while True:
    for btn in buttons:
        btn.poll()
