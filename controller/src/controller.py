import RPi.GPIO as GPIO
import time
import threading
from utils.lcd import LCD
import utils.led_array as LedArray
from utils.button_matrix import ButtonMatrix
from utils.metrics import Metrics
from config.config import Config

# =================================================================================================
# SETUP
# =================================================================================================
GPIO.setwarnings(False) # Disable GPIO Warnings
GPIO.setmode(GPIO.BCM)  # Set up the GPIO pins for output
GPIO.cleanup()          # Clean up the GPIO pins just in case they're in a bad state
ButtonMatrix()          # Inititalize the buttons
LedArray.init()         # Initialize LEDs
LCD().idle()            # Initialize LCD Display

# =================================================================================================
# METRICS THREAD
# =================================================================================================
def metrics_loop():
    while True:
        Metrics().collect() # Collect the metrics
        LedArray.update()   # Update the LED status indicators
        LCD.update()
        time.sleep(Config().metrics.pollPeriodSeconds)

metrics_thread = threading.Thread(target=metrics_loop)
metrics_thread.start()

# =================================================================================================
# MAIN LOOP
# =================================================================================================
try:
    while True:
        ButtonMatrix().poll()
        time.sleep(Config().btnArray.pollPeriodSeconds)
except:
    GPIO.cleanup()
