import os
import pika
import serial
import json

# Get the serial device and baud rate from environment variables
SERIAL_DEVICE = os.environ['SERIAL_DEVICE']
BAUD_RATE = int(os.environ['BAUD_RATE'])

# Get RabbitMQ credentials from environment variables
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_PATH = os.environ['RABBITMQ_PATH']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']

# RabbitMQ connection parameters
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_PATH, credentials)

# Create a RabbitMQ connection and channel
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queues
channel.queue_declare(queue='commands')
channel.queue_declare(queue='metrics')

# Initialize the serial connection
ser = serial.Serial(SERIAL_DEVICE, BAUD_RATE)

# Listen to messages from the "api_to_router" queue and forward them to the Arduino over serial
def queue_message_callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    print(data)
    
    command = data['payload']['command']
    args = data['payload']['args']

    if (command == "metrics"):
        if (ser.in_waiting > 0):
            message = ser.readline().decode('utf-8').rstrip()
            ser.flush()
            channel.basic_publish(
                  exchange='',
                  routing_key='metrics',
                  body=message
            )
            print(message)
        return

    if (command == "socket"):
        cmd = 'A' if args['state'] else 'a'
        cmd = chr(ord(cmd) + args['id'])
        print(cmd)
        ser.write(bytes(cmd, 'utf-8'))
        return

    print("invalid command")

channel.basic_consume(
    queue='commands',
    on_message_callback=queue_message_callback,
    auto_ack=True,
    exclusive=True,
    consumer_tag="serial_router"
)

try:
    # Start consuming messages
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close()
    ser.close()
