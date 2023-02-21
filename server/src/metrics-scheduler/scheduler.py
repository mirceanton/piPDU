from utils.rabbitmq import RabbitMQ
import utils.constants as constants
import time
import json

rabbitmq = RabbitMQ(
    username = constants.RABBITMQ_USER,
    password = constants.RABBITMQ_PASS,
    host = constants.RABBITMQ_HOST,
    port = constants.RABBITMQ_PORT,
    path = constants.RABBITMQ_PATH
)
rabbitmq.declareQueue(constants.RABBITMQ_COMMANDS_QUEUE)

print('INFO: Metrics scheduler is starting...')
try:
    while True:
        rabbitmq.publish(
            queue = constants.RABBITMQ_COMMANDS_QUEUE,
            tag = constants.RABBITMQ_PRODUCER_TAG,
            message = json.dumps({
                "timestamp": str(time.time()),
                "sender": constants.RABBITMQ_PRODUCER_TAG,
                "payload": {
                    "command": "metrics",
                    "args": {}
                }
            })
        )
        time.sleep(constants.MESSAGE_INTERVAL)
except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')
    rabbitmq.close()
except Exception as e:
    print(f'ERROR: An unexpected error occurred: {e}')
