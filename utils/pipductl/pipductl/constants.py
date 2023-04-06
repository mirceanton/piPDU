import pipdu_sdk
import os

CONFIG_FILE_PATH = os.getenv("PIPDUCTL_CONFIG", f"{os.path.expanduser('~')}/.pipductl/config.yaml")

servers = pipdu_sdk.config.parse_yaml_config(CONFIG_FILE_PATH)
