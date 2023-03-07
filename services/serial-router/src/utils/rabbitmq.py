import pika


class RabbitMQ:
    def __init__(self, username: str, password: str, host: str, port: int, path: str):
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
        self.channel.queue_declare(queue=queue)

    def publish(self, queue: str, message: str):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=message
            )
            print("INFO: Sent message to queue: " + message)
        except Exception as ex:
            print(f'ERROR: An error occured publishing the message: {ex}')

    def consume(self, queue: str, callback):
        method_frame, header_frame, body = self.channel.basic_get(queue)
        if method_frame is None:
            return
        callback(body)
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def hasMessage(self, queue: str):
        return self.channel.queue_declare(queue=queue).method.message_count

    def close(self):
        print('INFO: Closing the RabbitMQ Connection.')
        self.connection.close()
