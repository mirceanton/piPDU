import RPi.GPIO as GPIO
from common.config import Config
import datetime

class ButtonMatrix:
	# Singleton instance of the ButtonMatrix class
	__instance = None

    # Store the current and previous states of each button in the matrix
	__old_states = [False] * 16
	__cur_state = [False] * 16

    # Store the time at which each button was pressed
	__times = [0.0] * 16

	def poll(self):
		for index, state in enumerate(self.__cur_state):
			self.__old_states[index] = state

		for col in Config().btnArray.colPins:
			GPIO.output(col, GPIO.HIGH)

			for row in Config().btnArray.rowPins:
				ri = Config().btnArray.rowPins.index(row)
				ci = Config().btnArray.colPins.index(col)
				index = ri * 8 + ci

				# Update the current state of the buttons
				self.__cur_state[index] = ( GPIO.input(row) == GPIO.HIGH )

				# Check if the button has been pressed
				if self.__cur_state[index] is True and self.__old_states[index] is False:
					self.__times[index] = datetime.datetime.now()
						
				# Check if the button has been released
				if self.__cur_state[index] is False and self.__old_states[index] is True:
						time_held = (datetime.datetime.now() - self.__times[index]).total_seconds()
						if time_held >  Config().btnArray.longPressDurationSeconds:
							print(f"Button {index} long press")
						else:
							print(f"Button {index} short press")

			GPIO.output(col, GPIO.LOW)

	# Initialize the pins used for the button matrix
	def __init__(self):
		for pin in Config().btnArray.colPins:
			GPIO.setup(pin, GPIO.OUT)

		for pin in Config().btnArray.rowPins:
			GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	# Method for creating a singleton instance of the ButtonMatrix class
	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)
		return cls.__instance
