import utils.constants as constants
from utils.rabbitmq import RabbitMQ
from utils.sockets import sockets
from flask import Blueprint, make_response, request
import json

blueprint = Blueprint('sockets_by_id', __name__)


def turn(id: int, state: bool):
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
        message=json.dump({'id': id, 'state': state})
    )
    rabbitmq.close()

    if err is None:
        setState(id, state)
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


def setState(id: int, state: bool):
    sockets[id].state = state
    return make_response({
        'status': True,
        'payload': {'message': 'Socket status updated'}
    }, 200)


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


@blueprint.route('/<int:number>/on', methods=['PUT'])
def setStateOn(number: int):
    return setState(number, True)


@blueprint.route('/<int:number>/off', methods=['PUT'])
def setStateOff(number: int):
    return setState(number, False)
