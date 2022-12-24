# =================================================================================================
# This file contains the definition for the v1 version of the API.
# All routes defined in the `routes/` directory are registered at the apprpriate prefix
# inside a blueprint that represents the API.
# =================================================================================================
from flask import Blueprint
from api.v1.routes.socket import blueprint as bp_single_socket
from api.v1.routes.sockets import blueprint as bp_all_sockets

api_v1 = Blueprint('v1', __name__)

# TODO implement certificate based auth

# Endpoints for managing individual sockets
api_v1.register_blueprint(bp_single_socket, url_prefix="/socket")

# Endpoints for managing all sockets
api_v1.register_blueprint(bp_all_sockets, url_prefix="/sockets/all")
