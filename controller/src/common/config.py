import common.defaults as defaults
from types import SimpleNamespace
import yaml


class Config:
    # Singleton instance of the Config class
    __instance = None

    # Parse the config file and initialize the Config object
    def __init__(self):
        with open('config.yaml') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        if 'api' not in data:
            raise ValueError('ERROR: The `api` section is missing from the config file!')
        if 'host' not in data['api']:
            raise ValueError('ERROR: `api.host` is not defined in the config file!')
        if 'port' not in data['api']:
            raise ValueError('ERROR: `api.port` is not defined in the config file!')

        # Set values from config file/defaults
        self.api = SimpleNamespace(**data['api'])
        self.metrics = SimpleNamespace(**data.get('metrics', defaults.metrics))
        self.led = SimpleNamespace(**data.get('led', defaults.led))
        self.btnArray = SimpleNamespace(**data.get('btnArray', defaults.btnArray))
        self.lcd = SimpleNamespace(**data.get('lcd', defaults.lcd))

    # Method for creating a singleton instance of the Config class
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
