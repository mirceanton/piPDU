import pika
import time
import json
import os

# Read RabbitMQ parameters from environment variables
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_PATH = os.environ['RABBITMQ_PATH']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_QUEUE = "commands"

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

try:
    print('INFO: Metrics scheduler is starting...')
    while True:
        # Build the message to be sent
        message = json.dumps({
            "timestamp": str(time.time()),
            "sender": "metrics_scheduler",
            "payload": {
                "command": "metrics",
                "args": {}
            }
        })

        # Send the message to the queue
        channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message)
        print("INFO: Sent message to queue: " + message)

        # Wait for 0.25 seconds before sending the next message
        time.sleep(0.25)
except KeyboardInterrupt:
    # Gracefully close the connection with the RabbitMQ server
    print(f'INFO: Closing the RabbitMQ Connection.')
    connection.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
