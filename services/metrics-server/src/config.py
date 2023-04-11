import yaml

# Read the config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Parse the config
server_port = config['data'].get('server', {'port': 8000}).get('port')
serial_device = config['data']['serial'].get('device')
serial_baud = config['data']['serial'].get('baud', 9600)
poll_interval_seconds = float(config['data'].get('pollingIntervalSeconds', 1))
sensors = config['data']['sensors']

# Check for required fields
if serial_device is None:
    raise ValueError('Serial device is required')
if sensors is None or len(sensors) < 1:
    raise ValueError('At least one sensor is required')
