import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Relay:
    def __init__(self, pin, initialState=True, reversed=False):
        self.pin = pin
        self.current_state = None
        self.reversed = reversed
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.set_state(initialState)

    def set_state(self, state):
        GPIO.output(self.pin, state if not self.reversed else not state)
        self.current_state = state

    def get_state(self):
        return self.current_state

    def __del__(self):
        GPIO.cleanup(self.pin)
