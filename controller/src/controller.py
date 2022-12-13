from common.functions import setup, loop

setup()

try:
	while True:
		loop()

# Clean up the GPIO pins when the script is interrupted
except:
	GPIO.cleanup()

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
