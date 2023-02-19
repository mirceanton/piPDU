import os

# Get the serial device and baud rate from environment variables
SERIAL_DEVICE = os.environ['SERIAL_DEVICE']
SERIAL_BAUDRATE = int(os.environ['SERIAL_BAUDRATE'])

# Get RabbitMQ credentials from environment variables
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_PATH = os.environ['RABBITMQ_PATH']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_METRICS_QUEUE = 'metrics'
RABBITMQ_COMMANDS_QUEUE = 'commands'
RABBITMQ_CONSUMER_TAG = 'serial_router'
