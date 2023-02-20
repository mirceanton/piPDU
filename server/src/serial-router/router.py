from utils.rabbitmq import RabbitMQ
from utils.arduino import Arduino
import json

rabbitmq = RabbitMQ()
arduino = Arduino()

def queue_message_callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    print(f'INFO: Got message from queue: {data}')

    command = data['payload']['command']
    args = data['payload']['args']

    if (command == "metrics"):
        message = arduino.read()
        if message:
            rabbitmq.publish(message)
            print(f'INFO: Message enqueued')
    elif (command == "socket"):
        if args['id'] is None:
            cmd = 'r' if args['state'] is True else 'q'
            arduino.write(cmd)
        else:
            cmd = 'A' if args['state'] is True else 'a'
            cmd = chr(ord(cmd) + args['id'])
            arduino.write(cmd)
    else:
        print(f'ERROR: Invalid command {command}')

rabbitmq.setCallback(queue_message_callback)

try:
    rabbitmq.consume()
except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')
    arduino.close()
    rabbitmq.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
