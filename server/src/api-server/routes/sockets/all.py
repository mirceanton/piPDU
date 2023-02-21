import utils.constants as constants
from utils.rabbitmq import rabbitmq
from utils.message_builder import MessageBuilder
from utils.sockets import sockets
from flask import Blueprint, make_response

blueprint = Blueprint('sockets_all', __name__)

def turn(state: bool):
    status, err = rabbitmq.publish(
        queue = constants.RABBITMQ_COMMANDS_QUEUE,
        message = MessageBuilder().setState(state).build()
    )

    if err is None:
        setState(state)
        return make_response({
            'status': True,
            'payload': {}
        }, 200)

    return make_response(jsonify(({
        'status': False,
        'payload': {
            'message': 'Unable to send message',
            'error': err
        }
    }), 500))

def setState(state: bool):
    for i in range(16):
        sockets[i].state = state

    return make_response({
        'status': True,
        'payload': { 'message': 'Socket status updated' }
    }, 200)

@blueprint.route('/on', methods=['POST'])
def turnOn():
    return turn(True)

@blueprint.route('/off', methods=['POST'])
def turnOff():
    return turn(False)

@blueprint.route('/on', methods=['PUT'])
def setStateOn():
    return setState(True)

@blueprint.route('/off', methods=['PUT'])
def setStateOff():
    return setState(False)
