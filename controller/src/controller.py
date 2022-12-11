# Import the necessary libraries
import RPi.GPIO as GPIO
import time
import requests
from common.lcd import LCD
from common.config import Config

display = LCD()
display.idle()
time.sleep(2)