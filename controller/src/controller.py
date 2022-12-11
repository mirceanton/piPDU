# Import the necessary libraries
import RPi.GPIO as GPIO
import time
import re
import requests
from common.lcd import LCD
from common.config import Config

# Define piPDU server prometheus metrics endpoint
METRICS_URL = f"http://{Config().api.host}:{Config().api.port}/metrics"

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

while True:
	response = requests.get(METRICS_URL)
	metrics = []

	for line in response.text.split("\n"):
		if re.search("^socket_", line):
			metrics.append(line.split(' ')[1])
	
	for index, value in enumerate(metrics):
		print(f"Socket {index}: {value}")

	time.sleep(Config().metrics.periodSeconds)

# Clean up the GPIO pins
GPIO.cleanup()