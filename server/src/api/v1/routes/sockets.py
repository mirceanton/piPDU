# =================================================================================================
# This file contains the code for the endpoints that concern ALL sockets.
# 
# There are 2 actions possible:
#   - turn all sockets on
#   - turn all sockets off
# =================================================================================================
from flask import Blueprint, request, jsonify
from utils.socket_array import SocketArray
import api.v1.response as resp

blueprint = Blueprint('sockets', __name__)

@blueprint.route('/off', methods=['POST'])
def off():
    """Turn off all sockets"""
    for socket in SocketArray().sockets:
        socket.turnOff()
    return resp.all_sockets_off_ok()

@blueprint.route('/on', methods=['POST'])
def on():
    """Turn on all sockets"""
    for socket in SocketArray().sockets:
        socket.turnOn()
    return resp.all_sockets_on_ok()
