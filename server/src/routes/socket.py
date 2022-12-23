from flask import Blueprint, request, jsonify
import common.errors as err

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
            'status': "N/A"
        }
    })

# Flask route for sending commands to Arduino
@blueprint.route('/allOff', methods=['POST'])
def all_off(number: int):
    pass

# Flask route for sending commands to Arduino
@blueprint.route('/allOn', methods=['POST'])
def all_on(number: int):
    pass
    
# Flask route for sending commands to Arduino
@blueprint.route('/on/<int:number>', methods=['POST'])
def socket_on(number: int):
    pass

# Flask route for sending commands to Arduino
@blueprint.route('/off/<int:number>', methods=['POST'])
def socket_off(number: int):
    pass

# Flask route for sending commands to Arduino
@blueprint.route('/toggle/<int:number>', methods=['POST'])
def socket_toggle(number: int):
    pass