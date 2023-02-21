import utils.constants as constants
import pika

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

    def setCallback(self, callback):
        self.channel.basic_consume(
            queue = constants.RABBITMQ_METRICS_QUEUE,
            on_message_callback = callback,
            auto_ack = True,
            exclusive = True,
            consumer_tag = constants.RABBITMQ_CONSUMER_TAG
        )

    def consume(self):
        print(f'INFO: Serial Router is listening for messages in the {constants.RABBITMQ_METRICS_QUEUE} queue...')
        self.channel.start_consuming()
    
    def close(self):
        print(f'INFO: Closing the RabbitMQ Connection.')
        self.connection.close()
