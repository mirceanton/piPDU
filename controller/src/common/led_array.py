import RPi.GPIO as GPIO
from common.config import Config


# Update LED status based on relay status
def led_array_update():
	pass

# Initialize the LEDs by confoiguring the pins as outputs and setting them to LOW
def led_array_init():
	for led in Config().led.pins:
		GPIO.setup(led, GPIO.OUT)
		GPIO.output(led, GPIO.HIGH)

