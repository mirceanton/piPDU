from flask import Blueprint, jsonify

blueprint = Blueprint('ping', __name__)

# "Liveness probe" endpoint
@blueprint.route('/')
def ping():
    return jsonify({
        'success': True,
        'payload': 'pong'
    })
