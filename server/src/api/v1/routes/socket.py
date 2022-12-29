# =================================================================================================
# This file contains the code for the endpoints for managing individual sockets
# 
# There are 3 possible actions:
#   - turn the socket on
#   - turn the socket off
#   - query the server for the status of the socket
# =================================================================================================
from flask import Blueprint, request, jsonify, make_response
from utils.socket_array import SocketArray
import api.v1.response as resp

blueprint = Blueprint('socket', __name__)

@blueprint.before_request
def index_validator():
    """
    Check if the `number` argument from each request is within the valid [0,15] range.
    """
    number = request.view_args.get('number')
    if number < 0 or number > 15:
        return resp.index_out_of_range()

@blueprint.route('/<int:number>/info', methods=['GET'])
def status(number: int):
    """
    Check the status of a given socket
    """
    return make_response(jsonify({
        'success': True,
        'payload': SocketArray().sockets[number].info()
    }), 200)

@blueprint.route('/<int:number>/on', methods=['POST'])
def on(number: int):
    """
    Turn on a given socket
    """
    if SocketArray().sockets[number].turnOn() == 0:
        return resp.nothing_to_do()
    return resp.socket_on_ok(number)

@blueprint.route('/<int:number>/off', methods=['POST'])
def off(number: int):
    """
    Turn off a given socket
    """
    if SocketArray().sockets[number].turnOff() == 0:
        return resp.nothing_to_do()
    return resp.socket_off_ok(number)

@blueprint.route('/<int:number>/toggle', methods=['POST'])
def toggle(number: int):
    """
    Toggle a given socket
    """
    SocketArray().sockets[number].toggle()
    return resp.socket_off_ok(number)
