from flask import Blueprint, make_response

blueprint = Blueprint('ping', __name__)

@blueprint.route('/')
def ping():
    return make_response({
        'success': True,
        'payload': 'pong'
    }, 200)