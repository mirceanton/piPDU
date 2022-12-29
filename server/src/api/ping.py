# =================================================================================================
# This file contains the endpoint that can be used as a liveness probe for the API.
# This endpoint is version agnostic, so it should be present in any api version.
# =================================================================================================
from flask import Blueprint, make_response

blueprint = Blueprint('ping', __name__)

# ===============================================
# "Liveness probe" endpoint
# ===============================================
@blueprint.route('/')
def ping():
    return make_response({
        'success': True,
        'payload': 'pong'
    }, 200)
