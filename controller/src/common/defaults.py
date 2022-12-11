# Default config section
metrics = { 'enabled': True }
led = {'pins':  [33, 35, 37, 40, 38, 36, 32, 30, 28, 26, 24, 22, 18, 16, 12, 10, 8]}
btnArray = {
	'rowPins': [19, 23],
	'colPins': [21, 23, 29, 31, 15, 13, 11, 7],
	'longPressDurationSeconds': 5,
}
lcd = {
	'expander': "PCF8574",
	'address': 0x27,
	'port': 1,
	'backlight': True,
	'messageDurationSeconds': 5,
}