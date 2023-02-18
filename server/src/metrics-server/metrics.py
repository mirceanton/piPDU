import os
import pika
from prometheus_client import Gauge, start_http_server

# Get RabbitMQ credentials from environment variables
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_PATH = os.environ['RABBITMQ_PATH']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_QUEUE = "metrics"

# RabbitMQ connection parameters
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_PATH, credentials)

# Create a RabbitMQ connection and channel, and declare the queue
try:
    connection = pika.BlockingConnection(parameters)
    print('INFO: Connection established to RabbitMQ')
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    print('INFO: RabbitMQ queue declared')
except pika.exceptions.AMQPConnectionError:
    print('ERROR: Could not connect to RabbitMQ. Check your connection settings.')
    exit(1)

# Create the list for the prometheus gauges 
gauges = []
for i in range(16):
    gauge = Gauge(f'socket_{i}', f'Socket {i} current in amps', ['unit'])
    gauges.append(gauge)

# Start the metrics server
start_http_server(8000)
print('INFO: Prometheus Metrics Server started on port 8000')

# Define the callback function for handling incoming messages
def queue_message_callback(ch, method, properties, body):
    # Parse the message into a list of float values
    message = body.decode('utf-8').rstrip()
    print(f'INFO: Got message from queue: {message}')
    values = map(float, message.split(' '))

    # Update the gauges with the new values
    for i, value in enumerate(values):
        gauges[i].labels(unit=['unit']).set(value)

# Start consuming messages from the RabbitMQ queue
channel.basic_consume(
    queue=RABBITMQ_QUEUE,
    on_message_callback=queue_message_callback,
    auto_ack=True
)

try:
    print(f'INFO: Metrics server is listening for messages on the {RABBITMQ_QUEUE} queue...')
    channel.start_consuming()
except KeyboardInterrupt:
    # Gracefully close the connection with the RabbitMQ server
    print(f'INFO: Closing the RabbitMQ Connection.')
    connection.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
