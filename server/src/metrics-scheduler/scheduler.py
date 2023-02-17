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

# Establish a connection with the RabbitMQ server
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_PATH, credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue if it doesn't already exist
channel.queue_declare(queue=RABBITMQ_QUEUE)

# Main program loop
try:
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
    connection.close()
