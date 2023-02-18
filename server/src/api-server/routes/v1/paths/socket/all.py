from flask import Blueprint, make_response, jsonify
import routes.v1.utils.socket as socket

blueprint = Blueprint('sockets', __name__)

@blueprint.route('/off', methods=['POST'])
def off():
    print(f'DEBUG: Requested OFF state for all sockets')
    return make_response(jsonify(
        socket.allOff()
    ))

@blueprint.route('/on', methods=['POST'])
def on():
    print(f'DEBUG: Requested ON state for all sockets')
    return make_response(jsonify(
        socket.allOn()
    ))

@blueprint.route('/on', methods=['PUT'])
def setStateOn():
    print(f'DEBUG: Requested state update for socket {number} to ON')
    return make_response(jsonify(
        socket.setAllOn()
    ))

@blueprint.route('/off', methods=['PUT'])
def setStateOff():
    print(f'DEBUG: Requested state update for socket {number} to ON')
    returnmake_response(jsonify(
        socket.setAllOff()
    ))
