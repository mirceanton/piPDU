from utils.rabbitmq import RabbitMQ
from utils.arduino import Arduino
import utils.constants as constants
import json
import time
import os

arduino = Arduino(
    device=constants.SERIAL_DEVICE,
    baud_rate=constants.SERIAL_BAUDRATE
)

print(f'DEBUG: Creating named pipe {constants.METRICS_FIFO}')
if not os.path.exists(constants.METRICS_FIFO):
    os.mkfifo(constants.METRICS_FIFO)

print('DEBUG: Opening named pipe in write-only mode')
metrics_pipe = open(constants.METRICS_FIFO, 'w')

print(f'DEBUG: Creating named pipe {constants.COMMANDS_FIFO}')
if not os.path.exists(constants.COMMANDS_FIFO):
    os.mkfifo(constants.COMMANDS_FIFO)

print('DEBUG: Opening named pipe in read-only mode')
commands_pipe = open(constants.COMMANDS_FIFO, 'r')

def pipe_message_callback(body):
    data = json.loads(body.decode('utf-8'))
    print(f'INFO: Got message from pipe: {data}')

    if data['id'] is None:
        return arduino.write('r' if data['state'] is True else 'q')

    cmd = 'A' if data['state'] is True else 'a'
    cmd = chr(ord(cmd) + data['id'])
    arduino.write(cmd)


try:
    while True:
        pipe_message_callback(commands_pipe.read())

        if arduino.hasMessage():
            message = arduino.read()
            print(f'DEBUG: Message read from arduino: {message}')
            os.write(metrics_pipe, message);
            print('INFO: Message enqueued')

        time.sleep(0.1)

except KeyboardInterrupt:
    print('INFO: Received Keyboard Interrupt')
    arduino.close()
    metrics_pipe.close()
    commands_pipe.close()
