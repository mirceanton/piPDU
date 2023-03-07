from utils.rabbitmq import RabbitMQ
from utils.arduino import Arduino
import utils.constants as constants
import json
import time

arduino = Arduino(
    device = constants.SERIAL_DEVICE,
    baud_rate = constants.SERIAL_BAUDRATE
)

rabbitmq = RabbitMQ(
    username = constants.RABBITMQ_USER,
    password = constants.RABBITMQ_PASS,
    host = constants.RABBITMQ_HOST,
    port = constants.RABBITMQ_PORT,
    path = constants.RABBITMQ_PATH
)
rabbitmq.declareQueue(constants.RABBITMQ_COMMANDS_QUEUE)
rabbitmq.declareQueue(constants.RABBITMQ_METRICS_QUEUE)

def queue_message_callback(body):
    data = json.loads(body.decode('utf-8'))
    print(f'INFO: Got message from queue: {data}')

    if data['id'] is None:
        return arduino.write('r' if data['state'] is True else 'q')

    cmd = 'A' if data['state'] is True else 'a'
    cmd = chr(ord(cmd) + data['id'])
    arduino.write(cmd)

try:
    while True:
        if rabbitmq.hasMessage(queue = constants.RABBITMQ_COMMANDS_QUEUE):
            rabbitmq.consume(
                queue = constants.RABBITMQ_COMMANDS_QUEUE,
                callback = queue_message_callback
            )
        else:
            print("No Rabbit")
        
        if arduino.hasMessage():
            message = arduino.read()
            print(f'DEBUG: Message read from arduino: {message}')
            rabbitmq.publish(
                queue = constants.RABBITMQ_METRICS_QUEUE,
                message = message
            )
            print(f'INFO: Message enqueued')
        else:
            print("No Arduino")

        time.sleep(0.1)

except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')
    arduino.close()
    rabbitmq.close()
