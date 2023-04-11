from config import parse_yaml
import os

api_port = int(os.environ.get('API_SERVER_PORT', '3000'))
api_host = os.environ.get('API_SERVER_HOST', '0.0.0.0')

config_file = os.environ.get('API_SERVER_CONFIG', 'config.yaml')

relays = parse_yaml(config_file)
