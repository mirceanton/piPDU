# Import the necessary libraries
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

# Define connections
led_pins = []     # TODO
btn_arr_row = []  # TODO
btn_arr_col = []  # TODO
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

# ===============================================
# SETUP
# ===============================================
# Set up the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize the LEDs
for pin in led_pins:
  GPIO.setup(pin, GPIO.OUT)

# Initialize button array
for pin in btn_arr_row:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, GPIO.HIGH)

for pin in btn_arr_col:
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ===============================================
# MAIN LOOP
# ===============================================
while True:
  # TODO
  pass
