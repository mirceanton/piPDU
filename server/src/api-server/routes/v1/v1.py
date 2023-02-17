from flask import Blueprint
from routes.v1.paths.ping import blueprint as ping_blueprint
from routes.v1.paths.socket.all import blueprint as socket_all_blueprint
from routes.v1.paths.socket.id import blueprint as socket_id_blueprint

v1_blueprint = Blueprint('v1', __name__)
v1_blueprint.register_blueprint(ping_blueprint, url_prefix="/ping")
v1_blueprint.register_blueprint(socket_all_blueprint, url_prefix="/socket/all")
v1_blueprint.register_blueprint(socket_id_blueprint, url_prefix="/socket")