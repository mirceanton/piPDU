import os


PCF_BUS = os.environ.get('PCF_BUS')
PCF_ADDR = os.environ.get('PCF_ADDR').split(",")

expanders = [
    
]

LONG_PRESS_DURATION_SECONDS = int(os.environ.get('LONG_PRESS_DURATION_SECONDS'), '5')
BUTTON_PINS = [ int(pin) for pin in os.environ.get('BUTTON_PINS', '1,3,5,7,9,11,13,15,0,2,4,6,8,10,12').split(",") ]

