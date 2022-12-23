from flask import Blueprint
from api.v1.routes.socket import blueprint as bp_single_socket
from api.v1.routes.sockets import blueprint as bp_all_sockets

api_v1 = Blueprint('v1', __name__)

# TODO implement some auth, probably in a `@before_request`

api_v1.register_blueprint(bp_single_socket, url_prefix="/socket")
api_v1.register_blueprint(bp_all_sockets, url_prefix="/sockets/all")