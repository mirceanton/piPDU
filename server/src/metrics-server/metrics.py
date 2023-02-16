import os
import pika
from prometheus_client import Gauge, start_http_server

# Get RabbitMQ credentials from environment variables
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_PATH = os.environ['RABBITMQ_PATH']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']

# RabbitMQ connection parameters
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_PATH, credentials)

# Create a RabbitMQ connection and channel, and declare the queue
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='metrics')

# Create the list for the prometheus gauges and start the metrics server
gauges = []
for i in range(16):
    gauge = Gauge(f'metric_{i}', f'Metric {i}', ['unit'])
    gauges.append(gauge)

start_http_server(8000)

# Define the callback function for handling incoming messages
def queue_message_callback(ch, method, properties, body):
    # Parse the message into a list of float values
    message = body.decode('utf-8').rstrip()
    values = map(float, message.split(' '))
    
    # Update the gauges with the new values
    for i, value in enumerate(values):
        print(i, ":", value)
        gauges[i].labels(unit='A').set(value)
  
# Start consuming messages from the RabbitMQ queue
channel.basic_consume(
  queue='metrics',
  on_message_callback=queue_message_callback,
  auto_ack=True
)

print('Metrics server is listening for messages on the metrics queue...')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close()

