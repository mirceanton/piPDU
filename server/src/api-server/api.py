import os
from flask import Flask, jsonify
from routes.routes import api_blueprint

# Get the serial device and baud rate from environment variables
API_HOST = os.environ['API_HOST']
API_PORT = int(os.environ['API_PORT'])

# Create a Flask application and register the endpoints
app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix="/api")

print(f'INFO: Flask Server started on host {API_HOST} on port {API_PORT}')
app.run(host=API_HOST, port=API_PORT)
