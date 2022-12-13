# Default config section
metrics = {
	'enabled': True,
	'pollPeriodSeconds': 1,
}
led = {'pins':  [13, 19, 26, 21, 20, 16, 12, 1, 7, 8, 25, 24, 23, 18, 15, 14]}
btnArray = {
	'rowPins': [10, 11],
	'colPins': [9, 0, 5, 6, 22, 27, 17, 4],
	'longPressDurationSeconds': 3,
}
lcd = {
	'expander': "PCF8574",
	'address': 0x27,
	'port': 1,
	'backlight': True,
	'messageDurationSeconds': 5,
}