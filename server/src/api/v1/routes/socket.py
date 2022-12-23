from flask import Blueprint, request, jsonify, make_response
from common.socket import SocketArray
import api.v1.response as resp

blueprint = Blueprint('socket', __name__)

# Return with a custom error message if the number is out of range
@blueprint.before_request
def index_validator():
    number = request.view_args.get('number')
    if number < 0 or number > 15:
        return resp.index_out_of_range()

# Check the status of a given socket
@blueprint.route('/<int:number>/info', methods=['GET'])
def status(number: int):
    return make_response(jsonify({
        'success': True,
        'payload': SocketArray().sockets[number].info()
    }), 200)

# Turn on a given socket
@blueprint.route('/<int:number>/on', methods=['POST'])
def on(number: int):
    if SocketArray().sockets[number].turnOn() == 0:
        return resp.nothing_to_do()
    return resp.socket_on_ok(number)

# Turn off a given socket
@blueprint.route('/<int:number>/off', methods=['POST'])
def off(number: int):
    if SocketArray().sockets[number].turnOff() == 0:
        return resp.nothing_to_do()
    return resp.socket_off_ok(number)
