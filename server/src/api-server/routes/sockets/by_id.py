from utils.rabbitmq import rabbitmq
from utils.message_builder import MessageBuilder
from utils.sockets import sockets
from flask import Blueprint, make_response, jsonify, request
import json

blueprint = Blueprint('sockets_by_id', __name__)

def turn(id: int, state: bool):
    message = MessageBuilder().setState(state).setId(id).build()
    status, err = rabbitmq.publish(message)

    if err is None:
        return make_response({
            'status': True,
            'payload': {}
        }, 200)

    return make_response(jsonify(({
        'status': False,
        'payload': {
            'error': 'Unable to send message'
        }
    }), 500))

def setState(id: int, state: bool):
    sockets[id].state = state
    return make_response({
        'status': True,
        'payload': { 'message': 'Socket status updated' }
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
