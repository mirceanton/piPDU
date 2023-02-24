import os

# Get the serial device and baud rate from environment variables
SERIAL_DEVICE = os.environ.get('SERIAL_DEVICE', '/dev/ttyACM0')
SERIAL_BAUDRATE = int(os.environ.get('SERIAL_BAUDRATE', '921600'))

# Get RabbitMQ credentials from environment variables
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '5672')
RABBITMQ_PATH = os.environ.get('RABBITMQ_PATH', '/')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS')
RABBITMQ_METRICS_QUEUE = os.environ.get('RABBITMQ_METRICS_QUEUE', 'metrics')
RABBITMQ_COMMANDS_QUEUE = os.environ.get('RABBITMQ_COMMANDS_QUEUE', 'commands')
RABBITMQ_CONSUMER_TAG = os.environ.get('RABBITMQ_CONSUMER_TAG', 'serial_router')
