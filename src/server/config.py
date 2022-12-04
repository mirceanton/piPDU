import yaml
import os


class Config:
    # Singleton instance of the Config class
    __instance = None

    # Path to the configuration file
    __path = "config.yaml"

    # Configuration data
    data = None

    # Method for parsing the configuration file
    def __parse(self):
        print("Info: Parsing config file...")

        # Check if the config file exists
        if not os.path.exists(self.__path):
            print("Warning: No config file found. Assuming default values.")

            # Set default values for config options
            self.data = {
                'api': {
                    'host': '0.0.0.0',
                    'port': 8080
                },
                'metrics': {
                    'enabled': True,
                },
                'arduino': {
                    'device': '/dev/ttyACM0',
                    'baud': 9600
                },
            }
            return

        # Read config from YAML file
        try:
            self.data = yaml.safe_load(open(self.__path))
            print("Info: Config file parsed OK")
        except Exception:
            # Raise an exception with a custom error message if the config file parsing fails
            raise Exception('Error: Failed to parse config file')

    # Method for creating a singleton instance of the Config class
    def __new__(cls):
        if Config.__instance is None:
            Config.__instance = object.__new__(cls)

        if Config.__instance.data is None:
            Config.__instance.__parse()

        return Config.__instance
