import os

# Get RabbitMQ credentials from environment variables
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_PATH = os.environ['RABBITMQ_PATH']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_COMMANDS_QUEUE = 'commands'
RABBITMQ_PRODUCER_TAG = 'api_server'

# Get the API server host and port from environment variables
API_HOST = os.environ['API_HOST']
API_PORT = int(os.environ['API_PORT'])
