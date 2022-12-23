from flask import Blueprint

blueprint = Blueprint('sockets', __name__)

# Return with a custom error message if the number is out of range
@blueprint.before_request
def index_validator():
    number = request.view_args.get('number')
    if number < 0 or number > 15:
        return err.index_out_of_range()

# Flask route for checking the status of a socket
@blueprint.route('/info/<int:number>', methods=['GET'])
def check_status(number: int):
    # Return the cached status of the socket
    return jsonify({
        'success': True,
        'payload': {
            'status': socket[number]
        }
    })

# Flask route for sending commands to Arduino
@blueprint.route('/<int:number>', methods=['POST'])
def send_command(number: int):
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