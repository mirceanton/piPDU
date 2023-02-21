from utils.rabbitmq import RabbitMQ
import utils.constants as constants
import time

rabbitmq = RabbitMQ(
    username = constants.RABBITMQ_USER,
    password = constants.RABBITMQ_PASS,
    host = constants.RABBITMQ_HOST,
    port = constants.RABBITMQ_PORT,
    path = constants.RABBITMQ_PATH
)

print('INFO: Metrics scheduler is starting...')
try:
    while True:
        rabbitmq.publish()
        time.sleep(0.4)
except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')
    rabbitmq.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
