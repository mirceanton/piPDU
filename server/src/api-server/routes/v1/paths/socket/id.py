from flask import Blueprint, request, make_response, jsonify
import routes.v1.utils.socket as socket

blueprint = Blueprint('socket', __name__)

@blueprint.before_request
def index_validator():
    number = request.view_args.get('number')
    if number < 0 or number > 15:
        print('ERROR: Index out of range')
        return make_response(jsonify({
            'status': False,
            'payload': {
                'error': 'Index out of range',
                'message': 'Socket id must be between 0 and 15'
            }
        }), 400)

@blueprint.route('/<int:number>/info', methods=['GET'])
def info(number: int):
    print(f'DEBUG: Requested info for socket {number}')
    return make_response(jsonify(
        socket.sockets[number].info()
    ))

@blueprint.route('/<int:number>/on', methods=['POST'])
def on(number: int):
    print(f'DEBUG: Requested ON state for socket {number}')
    return make_response(jsonify(
        socket.sockets[number].on()
    ))

@blueprint.route('/<int:number>/off', methods=['POST'])
def off(number: int):
    print(f'DEBUG: Requested OFF state for socket {number}')
    return make_response(jsonify(
        socket.sockets[number].off()
    ))

@blueprint.route('/<int:number>/on', methods=['PUT'])
def setStateOn(number: int):
    print(f'DEBUG: Requested state update for socket {number} to ON')
    socket.sockets[number].state = True
    return make_response(jsonify({
        'status': True,
        'payload': {}
    }), 200)

@blueprint.route('/<int:number>/off', methods=['PUT'])
def setStateOff(number: int):
    print(f'DEBUG: Requested state update for socket {number} to OFF')
    socket.sockets[number].state = False
    return make_response(jsonify({
        'status': True,
        'payload': {}
    }), 200)
