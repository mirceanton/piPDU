import utils.constants as constants
from routes.ping import blueprint as ping_blueprint
from routes.sockets.all import blueprint as sockets_all_blueprint
from routes.sockets.by_id import blueprint as sockets_by_id_blueprint
from flask import Flask

# Create a Flask application and register the endpoints
app = Flask(__name__)
app.register_blueprint(ping_blueprint, url_prefix="/api/v1/ping")
app.register_blueprint(sockets_all_blueprint, url_prefix="/api/v1/sockets/all")
app.register_blueprint(sockets_by_id_blueprint, url_prefix="/api/v1/socket")

print(f'INFO: Flask Server started on {constants.API_HOST}:{constants.API_PORT}')
app.run(
    host=constants.API_HOST,
    port=constants.API_PORT
)
