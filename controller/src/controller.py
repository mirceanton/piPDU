# Import the necessary libraries
import RPi.GPIO as GPIO
import time
import requests
from common.lcd import LCD
from common.config import Config

# Initialize GPIO
GPIO.setwarnings(False)		# Disable GPIO Warnings
GPIO.cleanup()				# Clean up the GPIO pins just in case they're in a bad state
GPIO.setmode(GPIO.BCM)	# Set up the GPIO pins for output

# Initialize LCD Display
display = LCD()
display.idle()

# Initialize LEDs
for led in Config().led.pins:
	GPIO.setup(led, GPIO.OUT)
	GPIO.output(led, GPIO.LOW)

# Clean up the GPIO pins
GPIO.cleanup()