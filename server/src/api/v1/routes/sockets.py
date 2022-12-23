from flask import Blueprint, request, jsonify
from common.socket import SocketArray
import api.v1.response as resp

blueprint = Blueprint('sockets', __name__)

# Turn all sockets off
@blueprint.route('/off', methods=['POST'])
def off():
    for socket in SocketArray().sockets:
        socket.turnOff()
    return resp.all_sockets_off_ok()

# Turn all sockets on
@blueprint.route('/on', methods=['POST'])
def on():
    for socket in SocketArray().sockets:
        socket.turnOn()
    return resp.all_sockets_on_ok()
