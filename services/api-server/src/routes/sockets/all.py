import utils.constants as constants
from utils.rabbitmq import RabbitMQ
from utils.sockets import sockets
from flask import Blueprint, make_response
import json

blueprint = Blueprint('sockets_all', __name__)


def turn(state: bool):
    rabbitmq = RabbitMQ(
        username=constants.RABBITMQ_USER,
        password=constants.RABBITMQ_PASS,
        host=constants.RABBITMQ_HOST,
        port=constants.RABBITMQ_PORT,
        path=constants.RABBITMQ_PATH
    )
    rabbitmq.declareQueue(constants.RABBITMQ_COMMANDS_QUEUE)
    status, err = rabbitmq.publish(
        queue=constants.RABBITMQ_COMMANDS_QUEUE,
        message=json.dumps({'state': state, 'id': None})
    )
    rabbitmq.close()

    if err is None:
        setState(state)
        return make_response({
            'status': True,
            'payload': {}
        }, 200)

    return make_response({
        'status': False,
        'payload': {
            'error': 'Unable to send message',
        }
    }, 500)


def setState(state: bool):
    for i in range(16):
        sockets[i].state = state

    return make_response({
        'status': True,
        'payload': {'message': 'Socket status updated'}
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
