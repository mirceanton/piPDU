from flask import Blueprint, make_response

blueprint = Blueprint('ping', __name__)

# "Liveness probe" endpoint
@blueprint.route('/')
def ping():
    return make_response({
        'success': True,
        'payload': 'pong'
    }, 200)
