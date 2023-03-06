from pcf8574 import PCF8574
import os

EXPANDER_I2C_BUS = [ int(x) for x in os.environ.get('EXPANDER_I2C_BUS').split(",") ]
EXPANDER_I2C_ADDR = [ int(x, 16) for x in os.environ.get('EXPANDER_I2C_ADDR').split(",")]

BUTTON_LONG_PRESS_DURATION_SECONDS = int(os.environ.get('LONG_PRESS_DURATION_SECONDS', '5'))
BUTTON_PINS = [ int(pin) for pin in os.environ.get('BUTTON_PINS', '1,3,5,7,9,11,13,15,0,2,4,6,8,10,12').split(",") ]
BUTTON_POLL_INTERVAL_SECONDS = int(os.environ.get('BUTTON_POLL_INTERVAL_SECONDS', '1'))

PIPDU_SERVER_ADDRESS = os.environ.get('PIPDU_SERVER_ADDRESS')
FIFO = os.environ.get('FIFO', '/tmp/display_fifo')

def get_expanders():
  if len(EXPANDER_I2C_BUS) < 1:
    raise ValueError("At least 1 i2c bus must be speciffied!\nEXPANDER_I2C_BUS is empty")

  expanders = []

  # If there is only 1 bus specified, the same bus will be used for all expanders
  if len(EXPANDER_I2C_BUS) == 1:
    bus = EXPANDER_I2C_BUS[0]
    for addr in EXPANDER_I2C_ADDR:
      expanders.append( PCF8574(bus, addr) )
    return expanders

  # If there are multiple busses specified, there should be 1 bus per address
  if len(EXPANDER_I2C_BUS) > 1 and len(EXPANDER_I2C_BUS) != len(EXPANDER_I2C_ADDR):
    raise ValueError("If more than 1 i2c bus is specified, there should be 1 i2c bus per i2c address.\nEXPANDER_I2C_BUS and EXPANDER_I2C_ADDR must have the same number of elements if EXPANDER_I2C_BUS has more than 1 element.")

  for bus, addr in zip(EXPANDER_I2C_BUS, EXPANDER_I2C_ADDR):
    expanders.append( PCF8574(bus, addr) )
  return expanders
