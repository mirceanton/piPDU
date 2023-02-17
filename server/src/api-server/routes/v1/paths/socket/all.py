from flask import Blueprint, jsonify

blueprint = Blueprint('sockets', __name__)

@blueprint.route('/off', methods=['POST'])
def off():
    print("Turn off all sockets")
    return "ok"

@blueprint.route('/on', methods=['POST'])
def on():
    print("Turn on all sockets")
    return "ok"
