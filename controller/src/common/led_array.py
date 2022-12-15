import RPi.GPIO as GPIO
from common.config import Config
from common.metrics import Metrics

# Update LED status based on relay status
def led_array_update():
    for index, led in enumerate(Config().led.pins):
        GPIO.output(led, GPIO.HIGH if Metrics().metrics[index] > 0 else GPIO.LOW) 

# Initialize the LEDs by confoiguring the pins as outputs and setting them to LOW
def led_array_init():
    for led in Config().led.pins:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.HIGH)
