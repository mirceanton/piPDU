# Import the necessary libraries
import RPi.GPIO as GPIO
import time
from common.lcd import LCD
from common.led_array import led_array_init, led_array_update
from common.button_matrix import ButtonMatrix
from common.config import Config
from common.metrics import Metrics

# =================================================================================================
# SETUP
# =================================================================================================
GPIO.setwarnings(False)	# Disable GPIO Warnings
GPIO.setmode(GPIO.BCM)	# Set up the GPIO pins for output
GPIO.cleanup()			# Clean up the GPIO pins just in case they're in a bad state
ButtonMatrix()			# Inititalize the buttons
led_array_init()		# Initialize LEDs
LCD().idle()			# Initialize LCD Display

# =================================================================================================
# METRICS THREAD
# =================================================================================================
def metrics_loop():
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
except:
	GPIO.cleanup()
