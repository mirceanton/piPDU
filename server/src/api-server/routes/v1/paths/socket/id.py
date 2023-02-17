from flask import Blueprint, request, make_response

blueprint = Blueprint('socket', __name__)

@blueprint.before_request
def index_validator():
    number = request.view_args.get('number')
    if number < 0 or number > 15:
        print("index out of range")
        return "index out of range"

@blueprint.route('/<int:number>/info', methods=['GET'])
def status(number: int):
    return make_response(jsonify({
        'success': True,
        'payload': "info here"
    }), 200)

@blueprint.route('/<int:number>/on', methods=['POST'])
def on(number: int):
    print(f'Turn on socket {number}')
    return "ok"

@blueprint.route('/<int:number>/off', methods=['POST'])
def off(number: int):
    print(f'Turn off socket {number}')
    return "ok"