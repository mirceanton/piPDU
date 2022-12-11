# Import the necessary libraries
import RPi.GPIO as GPIO
import time
import re
import requests
from common.lcd import LCD
from common.config import Config

def button_interrupt(pin):
	# Scan the rows to detect a button press
	for col_num, col_pin in enumerate(Config().btnArray.colPins):

		# Set the row outputs to HIGH
		for row_num, row_pin in enumerate(Config().btnArray.rowPins):
			GPIO.output(row_pin, GPIO.HIGH)

			# Check if the column input is high
			if GPIO.input(col_pin) == GPIO.HIGH:
				# Print the button number
				print(col_num * len(Config().btnArray.rowPins) + row_num)
				return

		# Set the row outputs to LOW
		for row_pin in Config().btnArray.rowPins:
			GPIO.output(row_pin, GPIO.LOW)

# Define piPDU server prometheus metrics endpoint
METRICS_URL = f"http://{Config().api.host}:{Config().api.port}/metrics"

# Initialize GPIO
GPIO.setwarnings(False)	# Disable GPIO Warnings
GPIO.setmode(GPIO.BCM)	# Set up the GPIO pins for output
GPIO.cleanup()			# Clean up the GPIO pins just in case they're in a bad state

# Initialize LCD Display
display = LCD()
display.idle()

# Initialize LEDs
for led in Config().led.pins:
	GPIO.setup(led, GPIO.OUT)
	GPIO.output(led, GPIO.LOW)

# Initialize Button Array
for row_pin in Config().btnArray.rowPins:
	GPIO.setup(row_pin, GPIO.OUT)
	GPIO.output(row_pin, GPIO.LOW)
for col_pin in Config().btnArray.colPins:
	GPIO.remove_event_detect(col_pin)
	GPIO.setup(col_pin, GPIO.IN)
	GPIO.add_event_detect(col_pin, GPIO.RISING, callback=button_interrupt, bouncetime=50)

try:
	while True:
		response = requests.get(METRICS_URL)
		metrics = []

		for line in response.text.split("\n"):
			if re.search("^socket_", line):
				metrics.append(line.split(' ')[1])
		
		for index, value in enumerate(metrics):
			print(f"Socket {index}: {value}")

		time.sleep(Config().metrics.periodSeconds)

# Clean up the GPIO pins when the script is interrupted
except:
	GPIO.cleanup()