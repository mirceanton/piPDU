# =================================================================================================
# This file contains the default values for the config file
# =================================================================================================
metrics = {
    'enabled': True,
    'pollPeriodSeconds': 1,
}

expanders = {
    'addresses': [ 0x20, 0x21, 0x22, 0x24 ]
}

led = {
    'pins': [5,  1, 13,  9, 21, 17, 29, 25, 4, 0, 12, 20, 8, 16, 28, 24]
}
button = {
    'pins': [6, 2, 14, 22, 10, 18, 30, 26, 7, 3, 15, 11, 23, 19, 31, 27],
    'longPressDurationSeconds': 3,
    'pollPeriodSeconds': 0,
}

lcd = {
    'address': 0x27,
    'backlight': True,
}
