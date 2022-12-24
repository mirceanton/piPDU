# TODO
import RPi.GPIO as GPIO
from config.config import Config
from utils.metrics import Metrics

def led_array_update():
    """Update LED status based on relay status"""
    for index, led in enumerate(Config().led.pins):
        GPIO.output(led, GPIO.HIGH if Metrics().metrics[index] > 0 else GPIO.LOW) 

def led_array_init():
    """Initialize the LEDs by configuring the pins as outputs and setting them to LOW"""
    for led in Config().led.pins:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.HIGH)
