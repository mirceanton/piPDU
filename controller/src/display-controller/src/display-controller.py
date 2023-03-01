from utils.rabbitmq import RabbitMQ
import utils.constants as constants
import utils.lcd as lcd

def queue_message_callback(body):
    # TODO
    pass

rabbitmq = RabbitMQ()

while True:
    metrics = scrape_metrics(constants.PIPDU_METRICS_URL)

    # Update LCD state
    if rabbitmq.has_message(queue = constants.RABBITMQ_LCD_QUEUE):
        rabbitmq.consume(
            queue = constants.RABBITMQ_LCD_QUEUE,
            callback = queue_message_callback
        )
        
    lcd.update(metrics)
