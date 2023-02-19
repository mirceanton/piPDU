from utils.rabbitmq import rabbitmq
from utils.message_builder import MessageBuilder
from utils.sockets import sockets
from flask import Blueprint, make_response

blueprint = Blueprint('sockets_all', __name__)

def turn(state: bool):
    message = MessageBuilder().setState(state).build()
    status, err = rabbitmq.publish(message)

    if err is None:
        return make_response({
            'status': True,
            'payload': {}
        }, 200)
    
    return make_response(({
        'status': False,
        'payload': {
            'error': 'Unable to send message',
            'message': err
        }
    }), 500)

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