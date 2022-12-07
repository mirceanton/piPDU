from flask import jsonify

def index_out_of_range():
    print('Error: Socket number should be between 0 and 15')
    return jsonify({
        'success': False,
        'payload': {},
        'error': {
            'code': 'OOR (out-of-range)',
            'message': 'Socket number should be between 0 and 15',
        }
    }), 400