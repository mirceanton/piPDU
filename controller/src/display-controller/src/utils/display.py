from RPLCD.i2c import CharLCD
import datetime
from enum import Enum

class DisplayState(Enum):
    IDLE = "IDLE"
    INFO = "INFO"

class Display:
    def update(self, metrics):
        if self.__state_threshold_passed()
            self.set_state(DisplayState.IDLE)

        if self.state == DisplayState.IDLE:
            self.__update_idle(metrics)
        else:
            self.__update_info(metrics)

    def __update_idle(self, metrics):
        amps = sum(metrics)
        watts = amps * constants.VOLTS

        with self.device as dev:
            dev.clear()
            dev.write_string(constants.IDLE_TITLE_LINE)
            dev.clrf()
            dev.clrf()
            dev.write_string(f"Total Amps: {amps}A")
            dev.clrf()
            dev.write_string(f"Total Watts: {watts}W")

    def __update_info(self, metrics):
        amps = metrics[self.socket]
        watts = amps * constants.VOLTS

        with self.device as dev:
            dev.clear()
            dev.write_string(f"Socket {self.socket}:")
            dev.clrf()
            dev.clrf()
            dev.write_string(f"Amps: {amps}A")
            dev.clrf()
            dev.write_string(f"Watts: {watts}W")

    def set_state(self, state: DisplayState, socket : int = None):
        # Setting the same INFO state twice => going into IDLE state
        if self.state == state == DisplayState.INFO and self.socket == socket:
            self.set_state(DisplayState.IDLE)
            return

        self.state = state
        self.socket = socket
        self.last_state_change_time = datetime.datetime.now()

    def __state_threshold_passed(self) -> bool:
        if self.last_state_change_time is None:
            return False
        state_time = (datetime.datetime.now() - self.last_state_change_time).total_seconds()
        return time_held > constants.LCD_INFO_STATE_DURATION_SECONDS

    def close(self):
        if self.device is not None:
            self.device.close(clear = True)

    def __init__(self, expander: str, i2c_bus: int, i2c_address: int, backlight: bool):
        self.state = DisplayState.IDLE
        self.socket = None
        self.device = CharLCD(
            i2c_expander = expander,
            address = i2c_address,
            port = i2c_bus,
            backlight_enabled = backlight
        )
        self.last_state_change_time = None
