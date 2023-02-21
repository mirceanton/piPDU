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

    def publish(self, queue: str, message: str):
        try:
            self.channel.basic_publish(
                exchange = '',
                routing_key = queue,
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

rabbitmq = RabbitMQ(
    username = constants.RABBITMQ_USER,
    password = constants.RABBITMQ_PASS,
    host = constants.RABBITMQ_HOST,
    port = constants.RABBITMQ_PORT,
    path = constants.RABBITMQ_PATH
)
rabbitmq.declareQueue(constants.RABBITMQ_COMMANDS_QUEUE)
