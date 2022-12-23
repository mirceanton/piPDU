from common.config import Config
from common.arduino import Arduino
from common.metrics import Exporter
from common.socket import SocketArray
from api.ping import blueprint as route_ping
from api.v1.api import api_v1
import threading
from flask import Flask, jsonify

SocketArray() # initialize sockets

# Create a Flask application
app = Flask(__name__)

# Register the endpoints
app.register_blueprint(route_ping, url_prefix="/ping")
app.register_blueprint(api_v1, url_prefix="/api/v1/")

# Initialize the Prometheus Exporter
Exporter().initialize(app)

# Start a the Arduino communication thread in the background
listener_thread = threading.Thread(target=Arduino().listen)
listener_thread.start()

print(app.url_map)

# Start API server
app.run(host=Config().data['api']['host'], port=Config().data['api']['port'])
