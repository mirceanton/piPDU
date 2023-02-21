from utils.rabbitmq import RabbitMQ
from utils.prometheus import Prometheus
import utils.constants as constants

rabbitmq = RabbitMQ(
    username = constants.RABBITMQ_USER,
    password = constants.RABBITMQ_PASS,
    host = constants.RABBITMQ_HOST,
    port = constants.RABBITMQ_PORT,
    path = constants.RABBITMQ_PATH
)
prometheus = Prometheus()

# Define the callback function for handling incoming messages
def queue_message_callback(ch, method, properties, body):
    # Parse the message into a list of float values
    message = body.decode('utf-8').rstrip()
    print(f'INFO: Got message from queue: {message}')
    values = message.split(' ')

    if len(values) != 16:
        print(f'WARNING: Invalid message format; incomplete values array: f{message}')
    else:
        prometheus.update( map(float, values) )

rabbitmq.setCallback(queue_message_callback)

try:
    rabbitmq.consume()
except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')
    rabbitmq.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
