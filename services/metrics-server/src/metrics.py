from utils.prometheus import Prometheus
import utils.constants as constants
import os

prometheus = Prometheus()

print(f'DEBUG: Creating named pipe {constants.FIFO}')
if not os.path.exists(constants.FIFO):
    os.mkfifo(constants.FIFO)

print('DEBUG: Opening named pipe in read-only mode')
pipe = open(constants.FIFO, 'r')


def pipe_message_callback(body):
    if len(body) == 0:
        return

    print(f'DEBUG: Got message from pipe: {body}')
    values = body.split(' ')
    print(f'DEBUG: Parsed values as: {values}')

    if len(values) != 16:
        print(
            f'WARNING: Invalid message format; incomplete values array: f{body}')
    else:
        prometheus.update(map(float, values))


try:
    pipe_message_callback(pipe.read())
except KeyboardInterrupt:
    print('INFO: Received Keyboard Interrupt')
    pipe.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
