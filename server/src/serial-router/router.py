import os
import pika
import serial
import json

# Get the serial device and baud rate from environment variables
SERIAL_DEVICE = os.environ['SERIAL_DEVICE']
BAUD_RATE = int(os.environ['BAUD_RATE'])

# Initialize the serial connection
ser = serial.Serial(SERIAL_DEVICE, BAUD_RATE)
print("INFO: Serial connection initialized")

# Get RabbitMQ credentials from environment variables
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_PATH = os.environ['RABBITMQ_PATH']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_METRICS_QUEUE = 'metrics'
RABBITMQ_COMMANDS_QUEUE = 'commands'

# RabbitMQ connection parameters
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_PATH, credentials)

# Create a RabbitMQ connection and channel, and declare the queue
try:
    connection = pika.BlockingConnection(parameters)
    print('INFO: Connection established to RabbitMQ')
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_COMMANDS_QUEUE)
    channel.queue_declare(queue=RABBITMQ_METRICS_QUEUE)
    print('INFO: RabbitMQ queues declared')
except pika.exceptions.AMQPConnectionError:
    print('ERROR: Could not connect to RabbitMQ. Check your connection settings.')

# Listen to messages from the "api_to_router" queue and forward them to the Arduino over serial
def queue_message_callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    print(f'INFO: Got message from queue: {data}')

    command = data['payload']['command']
    args = data['payload']['args']

    if (command == "metrics"):
        if (ser.in_waiting > 0):
            message = ser.readline().decode('utf-8').rstrip()
            ser.flush()
            print(f'INFO: Got message from serial: {message}')

            channel.basic_publish(
                  exchange='',
                  routing_key=RABBITMQ_METRICS_QUEUE,
                  body=message
            )
            print(f'INFO: Message enqueued')
        return

    if (command == "socket"):
        if args['id'] is None:
            if args['state'] == True:
                cmd = 'r'
            else:
                cmd = 'q'
        else:
            cmd = 'A' if args['state'] else 'a'
            cmd = chr(ord(cmd) + args['id'])

        ser.write(bytes(cmd, 'utf-8'))
        print(f'INFO: Sent message over serial: {cmd}')
        return

    print(f'ERROR: Invalid command {command}')

channel.basic_consume(
    queue=RABBITMQ_COMMANDS_QUEUE,
    on_message_callback=queue_message_callback,
    auto_ack=True,
    exclusive=True,
    consumer_tag="serial_router"
)

try:
    print(f'INFO: Serial Router is listening for messages in the {RABBITMQ_COMMANDS_QUEUE} queue...')
    channel.start_consuming()
except KeyboardInterrupt:
    print(f'INFO: Closing the RabbitMQ Connection.')
    connection.close()
    print(f'INFO: Closing the serial connection.')
    ser.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
