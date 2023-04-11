from flask import Flask, jsonify, request
from globals import relays

app = Flask(__name__)


@app.route('/relays/<int:index>', methods=['GET'])
def get_relay_state(index):
    if index < 0 or index >= len(relays):
        return jsonify({'error': 'Invalid relay index'}), 400

    relay = relays[index]
    return jsonify({'pin': relay.pin, 'state': relay.get_state()}), 200


@app.route('/relays/<int:index>', methods=['PUT'])
def set_relay_state(index):
    if index < 0 or index >= len(relays):
        return jsonify({'error': 'Invalid relay index'}), 400

    state = request.args.get('state')
    if state is None:
        return jsonify({'error': 'Missing state parameter'}), 400
    state = state.lower() == 'true'

    relay = relays[index]
    relay.set_state(state)

    return jsonify({'pin': relay.pin, 'state': relay.get_state()}), 200


@app.route('/relays', methods=['GET'])
def get_all_relays_state():
    states = [{'pin': r.pin, 'state': r.get_state()} for r in relays]
    return jsonify(states), 200


@app.route('/relays', methods=['PUT'])
def set_all_relays_state():
    state = request.args.get('state')
    if state is None:
        return jsonify({'error': 'Missing state parameter'}), 400
    state = state.lower() == 'true'

    for r in relays:
        r.set_state(state)
    return get_all_relays_state()
