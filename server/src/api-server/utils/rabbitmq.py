import utils.constants as constants
import pika
import json
import time

class RabbitMQ:
    def __init__(self):
        self.connection = None
        self.channel = None

        # RabbitMQ connection parameters
        credentials = pika.PlainCredentials(constants.RABBITMQ_USER, constants.RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(constants.RABBITMQ_HOST, constants.RABBITMQ_PORT, constants.RABBITMQ_PATH, credentials)

        # Create a RabbitMQ connection and channel, and declare the queue
        try:
            self.connection = pika.BlockingConnection(parameters)
            print('INFO: Connection established to RabbitMQ')
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=constants.RABBITMQ_COMMANDS_QUEUE)
            print('INFO: RabbitMQ queue declared')

        except pika.exceptions.AMQPConnectionError:
            print('ERROR: Could not connect to RabbitMQ. Check your connection settings.')
            exit(1)

    def publish(self, message: str):
        try:
            self.channel.basic_publish(
                exchange = '',
                routing_key = constants.RABBITMQ_COMMANDS_QUEUE,
                body = message
            )
            print("INFO: Sent message to queue: " + message)
            return True, None
        except Exception as ex:
            print(f'ERROR: An error occured publishing the message: {ex}')
            return False, ex

    def __del__(self):
        print(f'INFO: Closing the RabbitMQ Connection.')
        self.connection.close()

rabbitmq = RabbitMQ()
