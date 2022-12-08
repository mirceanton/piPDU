from common.config import Config
from common.arduino import Arduino
from common.metrics import Exporter
import common.errors as err
import threading
from flask import Flask, jsonify

# Parse the config file
config = Config().data

# Initialize serial connection to the arduino
arduino = Arduino()

# State array for the 17 sockets
socket = [True] * 16

# Create a Flask application
app = Flask(__name__)

# Initialize the Prometheus Exporter
Exporter().initialize(app)

# Start a background thread to listen for data over
# serial and expose it via Prometheus
listener_thread = threading.Thread(target=arduino.listen)
listener_thread.start()

# Define a route for the /ping endpoint to validate connections
@app.route('/ping')
def ping():
    return jsonify({
        'success': True,
        'payload': 'pong'
    })

# Flask route for checking the status of a socket
@app.route('/api/v1/sockets/<int:number>', methods=['GET'])
def check_status(number: int):
    # Return with a custom error message if the number is out of range
    if number < 0 or number > 15:
        return err.index_out_of_range()

    # Return the cached status of the socket
    return jsonify({
        'success': True,
        'payload': {
            'status': socket[number]
        }
    })

# Flask route for sending commands to Arduino
@app.route('/api/v1/sockets/<int:number>', methods=['POST'])
def send_command(number: int):
    # Return with a custom error message if the number is out of range
    if number < 0 or number > 15:
        return err.index_out_of_range()

    # Convert the number to a lowercase character
    command = chr(number + 97) # 97 is the ascii code for 'a'

    # Write the command to the serial connection
    arduino.write(command)

    # Update the state array
    socket[number] = ~socket[number]

    print('Sent command to serial:', command)
    return jsonify({
        'success': True,
        'payload': {
            'socket_number': number,
            'command': command,
            'new_status': socket[number],
            'old_status': ~socket[number],
        }
    })

# Start the Flask API server
app.run(host=config['api']['host'], port=config['api']['port'])
