from config import Config
from arduino import Arduino
from flask import Flask

# Parse the config file
config = Config().data

# Initialize serial connection to the arduino
arduino = Arduino()

# Create a Flask application
app = Flask(__name__)

# Define a route for the /ping endpoint to validate connections
@app.route('/ping')
def ping():
    return 'pong'

# Flask route for sending commands to Arduino
@app.route('/api/v1/sockets/<socket_id>', methods=['POST'])
def send_command(number):
    # Convert the socket number to an integer
    number = int(number)

    # Check if the number is in the valid range
    if 0 <= number <= 15:
        # Convert the number to a lowercase character
        command = chr(number + 97)

        # Write the command to the serial connection
        arduino.write(command.encode())

        print('Sent command to serial:', command)
    else:
        # Raise an exception with a custom error message if the number is out of range
        raise Exception('Error: Socket number should be between 0 and 15')

# Start the Flask API server
app.run(host=config['api']['host'], port=config['api']['port'])
