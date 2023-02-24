import os

# Get RabbitMQ credentials from environment variables
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '5672')
RABBITMQ_PATH = os.environ.get('RABBITMQ_PATH', '/')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS')
RABBITMQ_COMMANDS_QUEUE = os.environ.get('RABBITMQ_COMMANDS_QUEUE', 'commands')
RABBITMQ_PRODUCER_TAG = os.environ.get('RABBITMQ_PRODUCER_TAG', 'api_server')

# Get the API server host and port from environment variables
API_HOST = os.environ.get('API_HOST', '0.0.0.0')
API_PORT = int(os.environ.get('API_PORT', '3000'))
