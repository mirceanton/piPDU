import os
import time
import pika
import json

class RabbitMQ:
    def sendMessage(self, state: bool, id = None):
        # Build the message to be sent
        message = {
            'timestamp': str(time.time()),
            'sender': 'api_server',
            'payload': {
                'command': 'socket',
                'args': {
                    'id': id,
                    'state': state
                }
            }
        }

        print('DEBUG: Sending message to queue...')
        try:
            self.channel.basic_publish(
                exchange = '',
                routing_key = self.RABBITMQ_QUEUE,
                body = json.dumps(message)
            )
            print(f'INFO: Sent message to queue: {message}')
            return ({
                'status': True,
                'payload': {}
            }), 200

        except pika.exceptions.AMQPError as err:
            print(f'ERROR: Unable to send message: {err}')
            return ({
                'status': False,
                'payload': {
                    'error': 'Unable to send message',
                    'message': err
                }
            }), 500

    def connect(self):
        print('DEBUG: Extracting RabbitMQ parameters from environment variables...')
        self.RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
        self.RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
        self.RABBITMQ_PATH = os.environ['RABBITMQ_PATH']
        self.RABBITMQ_USER = os.environ['RABBITMQ_USER']
        self.RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
        self.RABBITMQ_QUEUE = 'commands'
        print('INFO: Extracted RabbitMQ parameters from environment variables')

        # RabbitMQ connection parameters
        self.credentials = pika.PlainCredentials(
            self.RABBITMQ_USER,
            self.RABBITMQ_PASS
        )
        self.parameters = pika.ConnectionParameters(
            self.RABBITMQ_HOST,
            self.RABBITMQ_PORT,
            self.RABBITMQ_PATH,
            self.credentials
        )

        print('DEBUG: Creating a RabbitMQ connection and channel, and declare the queue...')
        try:
            self.connection = pika.BlockingConnection(self.parameters)
            print('INFO: Connection established to RabbitMQ')
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue = self.RABBITMQ_QUEUE)
            print('INFO: RabbitMQ queue declared')
        except pika.exceptions.AMQPConnectionError:
            print('ERROR: Could not connect to RabbitMQ. Check your connection settings.')

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
            cls._instance.connect()
        return cls._instance
