import utils.constants as constants
from utils.metrics import scrape_metrics
from utils.rabbitmq import RabbitMQ
from utils.display import Display

# =================================================================================================
# LCD SETUP
# =================================================================================================
display = Display(
    expander = constants.DISPLAY_I2C_EXPANDER,
    i2c_bus = constants.DISPLAY_I2C_BUS,
    i2c_address = constants.DISPLAY_I2C_ADDR,
    backlight = constants.DISPLAY_BACKLIGHT_ENABLED
)


# =================================================================================================
# RABBITMQ SETUP
# =================================================================================================
rabbitmq = RabbitMQ(
    username = constants.RABBITMQ_USER,
    password = constants.RABBITMQ_PASS,
    host = constants.RABBITMQ_HOST,
    port = constants.RABBITMQ_PORT,
    path = constants.RABBITMQ_PATH
)
rabbitmq.declareQueue(constants.RABBITMQ_DISPLAY_QUEUE)

def queue_message_callback(body):
    data = json.loads(body.decode('utf-8'))
    print(f'INFO: Got message from queue: {data}')

    state = data['state'].upper()
    socket = int(data['socket']) if data['socket'] is not None else None

    if state == "IDLE" and socket is None:
        display.state = "IDLE"
        return

    if state == "INFO" and (0 <= socket < 16):
        display.state = "INFO"
        display.socket = socket
        return

    raise ValueError(f'Poorly formatted message: {data}')


# =================================================================================================
# ENTRYPOINT
# =================================================================================================
try:
    while True:
        if rabbitmq.has_message(queue = constants.RABBITMQ_DISPLAY_QUEUE):
            rabbitmq.consume(
                queue = constants.RABBITMQ_DISPLAY_QUEUE,
                callback = queue_message_callback
            )
            
        display.update( scrape_metrics(constants.METRICS_ENDPOINT_URL) )

        time.sleep(constants.METRICS_POLL_INTERVAL_SECONDS)

except KeyboardInterrupt:
    print(f'INFO: Received Keyboard Interrupt')
    rabbitmq.close()
