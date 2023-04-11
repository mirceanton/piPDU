import utils.constants as constants
from utils.sockets import sockets
import os
from flask import Blueprint, make_response, request
import json

blueprint = Blueprint('sockets_by_id', __name__)


def turn(id: int, state: bool):
    try:
        # Open the named pipe for writing using a with block, in non-blocking mode
        with os.open(constants.FIFO, os.O_WRONLY | os.O_NONBLOCK) as pipe:
            os.write(pipe, json.dumps({'id': id, 'state': state}))

        sockets[id].state = state

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


@blueprint.before_request
def index_validator():
    number = request.view_args.get('number')
    if number < 0 or number > 15:
        return make_response({
            'success': False,
            'payload': {
                'error': 'Index out of range.'
            }
        }, 400)


@blueprint.route('/<int:number>/info', methods=['GET'])
def info(number: int):
    return make_response({
        'success': True,
        'payload': sockets[number].info()
    }, 200)


@blueprint.route('/<int:number>/on', methods=['POST'])
def turnOn(number: int):
    return turn(number, True)


@blueprint.route('/<int:number>/off', methods=['POST'])
def turnOff(number: int):
    return turn(number, False)
