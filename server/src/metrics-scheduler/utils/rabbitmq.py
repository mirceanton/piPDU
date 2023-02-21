import utils.constants as constants
import pika
import json
import time

class RabbitMQ:
    def __init__(self, username, password, host, port, path):
        self.connection = None
        self.channel = None

        # RabbitMQ connection parameters
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host, port, path, credentials)

        # Create a RabbitMQ connection and channel, and declare the queue
        try:
            self.connection = pika.BlockingConnection(parameters)
            print('INFO: Connection established to RabbitMQ')
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=constants.RABBITMQ_COMMANDS_QUEUE)
            self.channel.queue_declare(queue=constants.RABBITMQ_METRICS_QUEUE)
            print('INFO: RabbitMQ queues declared')

        except pika.exceptions.AMQPConnectionError:
            print('ERROR: Could not connect to RabbitMQ. Check your connection settings.')
            exit(1)

    def publish(self):
        # Build the message to be sent
        message = json.dumps({
            "timestamp": str(time.time()),
            "sender": constants.RABBITMQ_PRODUCER_TAG,
            "payload": {
                "command": "metrics",
                "args": {}
            }
        })

        try:
            self.channel.basic_publish(
                exchange = '',
                routing_key = constants.RABBITMQ_COMMANDS_QUEUE,
                body = message
            )
            print("INFO: Sent message to queue: " + message)
        except Exception as ex:
            print(f'ERROR: An error occured publishing the message: {ex}')

    def close(self):
        print(f'INFO: Closing the RabbitMQ Connection.')
        self.connection.close()
