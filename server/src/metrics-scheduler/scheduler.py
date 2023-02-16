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

# Establish a connection with the RabbitMQ server
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_PATH, credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the "commands" queue if it doesn't already exist
channel.queue_declare(queue='commands')


def generator_loop():
    while True:
        # Build the message to be sent
        message = {
            "timestamp": str(time.time()),
            "sender": "metrics_scheduler",
            "payload": {
                "command": "metrics",
                "args": {}
            }
        }
        
        # Convert the message to a JSON string
        message_json = json.dumps(message)
        
        # Send the message to the "commands" queue
        channel.basic_publish(exchange='', routing_key='commands', body=message_json)
        
        # Print the sent message for debugging purposes
        print("Sent message to queue: " + message_json)
        
        # Wait for 0.25 seconds before sending the next message
        time.sleep(0.25)

try:
    generator_loop()
except KeyboardInterrupt:
    connection.close()
