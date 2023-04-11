import utils.constants as constants
from utils.sockets import sockets
from flask import Blueprint, make_response
import json
import os

blueprint = Blueprint('sockets_all', __name__)


def turn(state: bool):
    try:
        # Open the named pipe for writing using a with block, in non-blocking mode
        with os.open(constants.FIFO, os.O_WRONLY | os.O_NONBLOCK) as pipe:
            os.write(pipe, json.dumps({'id': None, 'state': state}))

        for i in range(16):
            sockets[i].state = state

        return make_response({
            'status': True,
            'payload': {}
        }, 200)

    except Exception as e:
        return make_response({
            'status': False,
            'payload': {
                'error': 'Unable to send message',
            }
        }, 500)


@blueprint.route('/on', methods=['POST'])
def turnOn():
    return turn(True)


@blueprint.route('/off', methods=['POST'])
def turnOff():
    return turn(False)
