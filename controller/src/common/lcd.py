from common.config import Config
from RPLCD.i2c import CharLCD

# Wrapper class around the RPLCD.i2c.CharLCD implemented as a singleton
class LCD:
	__instance = None
	__device : CharLCD = None

	# Put the LCD into idle state
	def idle(self):
		pass

	# Show info about a given socket on the LCD
	def info(self, id):
		pass

	# Initialize the LCD display
	def __init__(self):
		self.__device = CharLCD(
			i2c_expander = Config().lcd.expander,
			address = Config().lcd.address,
			port = Config().lcd.port,
			backlight_enabled = Config().lcd.backlight,
		)

	# Clean up by closing the display
	def __del__(self):
		self.__device.close(clear = True)

	# Method for creating a singleton instance of the LCD class
	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)
		return cls.__instance
