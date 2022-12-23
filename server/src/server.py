from common.config import Config
from common.arduino import Arduino
from common.metrics import Exporter
from routes.ping import blueprint as bp_ping
from routes.socket import blueprint as bp_sock
import threading
from flask import Flask, jsonify

# State array for the 17 sockets
socket = [True] * 16

# Create a Flask application
app = Flask(__name__)

# Register the endpoints
app.register_blueprint(bp_ping, url_prefix="/ping")
app.register_blueprint(bp_sock, url_prefix="/api/v1/sockets")

# Initialize the Prometheus Exporter
Exporter().initialize(app)

# Start a the Arduino communication thread in the background
# listener_thread = threading.Thread(target=Arduino().listen)
# listener_thread.start()

print(app.url_map)

# Start API server
app.run(host=Config().data['api']['host'], port=Config().data['api']['port'])
