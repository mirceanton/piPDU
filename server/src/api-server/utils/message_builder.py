import utils.constants as constants
import time
import json

class MessageBuilder():
    def __init__(self):
        self.message = {
            'timestamp': None,
            'sender': constants.RABBITMQ_PRODUCER_TAG,
            'payload': {
                'command': 'socket',
                'args': {
                    'id': None,
                    'state': None
                }
            }
        }

    def setId(self, id: int):
        self.message['payload']['args']['id'] = id
        return self

    def setState(self, state: bool):
        self.message['payload']['args']['state'] = state
        return self

    def build(self):
        self.message['timestamp'] = str(time.time())
        return json.dumps(self.message)
