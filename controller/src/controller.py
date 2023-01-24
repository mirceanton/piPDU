import time
import threading
from utils.lcd import LCD, LCDStates
from utils.led_array import LedArray
from utils.button_matrix import ButtonMatrix
from utils.metrics import Metrics
from config.config import Config

# =================================================================================================
# SETUP
# =================================================================================================
ButtonMatrix()          # Inititalize the buttons
LedArray()              # Initialize LEDs
LCD().set_state(LCDStates.IDLE)            # Initialize LCD Display


# =================================================================================================
# METRICS THREAD
# =================================================================================================
# def metrics_loop():
#     while True:
#         Metrics().collect() # Collect the metrics
#         LedArray().update() # Update the LED status indicators
#         LCD().update()
#         time.sleep(Config().metrics.pollPeriodSeconds)

# metrics_thread = threading.Thread(target=metrics_loop)
# metrics_thread.start()


# =================================================================================================
# MAIN LOOP
# =================================================================================================
while True:
    ButtonMatrix().poll()
    time.sleep(Config().button.pollPeriodSeconds)
