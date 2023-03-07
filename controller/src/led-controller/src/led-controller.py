import utils.constants as constants
import utils.led as led
import time

print('INFO: Initializing PCF expanders')
expanders = constants.get_expanders()

print('INFO: Starting main loop')
try:
    while True:
        for index, pin in enumerate(constants.LED_PINS):
            led.update(
                index=index,
                expander=expanders[pin // 8],
                pin=pin % 8
            )
        time.sleep(constants.LED_UPDATE_INTERVAL_SECONDS)
except KeyboardInterrupt:
    print('INFO: Received Keyboard Interrupt')
