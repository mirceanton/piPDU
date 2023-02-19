from utils.rabbitmq import RabbitMQ
import time

rabbitmq = RabbitMQ()

print('INFO: Metrics scheduler is starting...')
try:
    while True:
        rabbitmq.publish()
        time.sleep(0.25)
except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')
    rabbitmq.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
