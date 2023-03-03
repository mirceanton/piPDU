from RPLCD.i2c import CharLCD

class Display:
    def __init__(self, expander: str, i2c_bus: int, i2c_address: int, backlight: bool):
        print("DEBUG: Initializing LCD object.")
        self.state = "IDLE"
        self.socket = None
        self.device = CharLCD(
            i2c_expander = expander,
            address = i2c_address,
            port = i2c_bus,
            backlight_enabled = backlight
        )

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

    def update(self, metrics):
        if self.state == "IDLE":
            self.__update_idle(metrics)
        else:
            self.__update_info(metrics)

    def close(self):
        print("DEBUG: Clearing and closing LCD object.")
        if self.device is not None:
            self.device.close(clear = True)
