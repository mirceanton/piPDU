from config.config import Config
from utils.arduino import Arduino
from utils.metrics import Exporter
from utils.socket_array import SocketArray
from api.ping import blueprint as route_ping
from api.v1.api import api_v1
import threading
from flask import Flask, jsonify

# =================================================================================================
# SETUP
# =================================================================================================
# Initialize Singletons
Arduino()
SocketArray()

# Create a Flask application and register the endpoints
app = Flask(__name__)
app.register_blueprint(route_ping, url_prefix="/ping")
app.register_blueprint(api_v1, url_prefix="/api/v1/")

# Initialize the Prometheus Exporter
Exporter().initialize(app)

# =================================================================================================
# SERIAL COMMUNICATION THREAD
# =================================================================================================
def serial_loop():
    while True:
        data = Arduino().listen()
        try:
            numbers = [float(n) for n in data.split(b',')]
            Exporter().update(numbers)
        except Exception as ex:
            logger.error(f"Failed to parse the serial message: {data}")
            logger.debug(ex)

listener_thread = threading.Thread(target=serial_loop)
listener_thread.start()

# =================================================================================================
# MAIN LOOP: Start API Server
# =================================================================================================
app.run(host=Config().api.host, port=Config().api.port)
