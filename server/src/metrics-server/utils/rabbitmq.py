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
        except pika.exceptions.AMQPConnectionError:
            print('ERROR: Could not connect to RabbitMQ. Check your connection settings.')
            exit(1)

    def declareQueue(self, queue: str):
        self.channel.queue_declare(queue = queue)

    def setConsumeCallback(self, queue, callback, tag):
        self.channel.basic_consume(
            queue = queue,
            on_message_callback = callback,
            auto_ack = True,
            exclusive = True,
            consumer_tag = tag
        )

    def startConsuming(self):
        print(f'INFO: Serial Router is listening for messages...')
        self.channel.start_consuming()
    
    def close(self):
        print(f'INFO: Closing the RabbitMQ Connection.')
        self.connection.close()
