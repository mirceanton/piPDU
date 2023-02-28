from pcf8574_io import PCF
from config.config import Config

expanders = [PCF(address) for address in Config().expanders.addresses]
