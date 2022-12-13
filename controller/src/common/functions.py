# Import the necessary libraries
import RPi.GPIO as GPIO
import time
import re
import requests
from common.lcd import LCD
from common.config import Config

# Define piPDU server prometheus metrics endpoint
METRICS_URL = f"http://{Config().api.host}:{Config().api.port}/metrics"

# =================================================================================================
# Main Functions
# =================================================================================================

def setup():
	__setup_gpio()
	__setup_buttons()
	__setup_leds()
	__setup_lcd()

def loop():
	response = requests.get(METRICS_URL)
	metrics = []

	for line in response.text.split("\n"):
		if re.search("^socket_", line):
			metrics.append(line.split(' ')[1])
	
	for index, value in enumerate(metrics):
		print(f"Socket {index}: {value}")

	time.sleep(Config().metrics.periodSeconds)


# =================================================================================================
# Utility Functions
# =================================================================================================

# Initialize GPIO
def __setup_gpio():
  GPIO.setwarnings(False)	# Disable GPIO Warnings
  GPIO.setmode(GPIO.BCM)	# Set up the GPIO pins for output
  GPIO.cleanup()			# Clean up the GPIO pins just in case they're in a bad state

# Initialize the pins used for the button array
def __setup_buttons():
	for row_pin in Config().btnArray.rowPins:
		GPIO.setup(row_pin, GPIO.OUT)
		GPIO.output(row_pin, GPIO.LOW)
	for col_pin in Config().btnArray.colPins:
		GPIO.remove_event_detect(col_pin)
		GPIO.setup(col_pin, GPIO.IN)

# Initialize the pins used to control the LEDs as outputs and set them to LOW
def __setup_leds():
	for led in Config().led.pins:
		GPIO.setup(led, GPIO.OUT)
		GPIO.output(led, GPIO.LOW)

# Initialize LCD Display
def __setup_lcd():	
	display = LCD()
	display.idle()
