import RPi.GPIO as GPIO
import time
import threading
from utils.lcd import LCD
from utils.led_array import led_array_init, led_array_update
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
led_array_init()        # Initialize LEDs
LCD().idle()            # Initialize LCD Display

# =================================================================================================
# METRICS THREAD
# =================================================================================================
def metrics_loop():
    while True:
        Metrics().collect()	# Collect the metrics
        led_array_update()	# Update the LED status indicators
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
