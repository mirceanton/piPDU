from config import Config
from flask import Flask

# Parse the config file
config = Config().data

# Create a Flask application
app = Flask(__name__)

# Define a route for the /ping endpoint to validate connections
@app.route('/ping')
def ping():
    return 'pong'

# Start the Flask API server
app.run(host=config['api']['host'], port=config['api']['port'])
