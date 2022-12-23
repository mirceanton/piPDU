from flask import make_response

def index_out_of_range():
    print('Error: Socket number should be between 0 and 15')
    return make_response({
        'success': False,
        'payload': {},
        'error': {
            'code': 'OOR (out-of-range)',
            'message': 'Socket number should be between 0 and 15',
        }
    }, 400)

def nothing_to_do():
    print('INFO: The requested state is the same with the current state. There is nothing to do.')
    return make_response({
        'success': True,
        'payload': {
            'message': 'The requested state is the same with the current state. There is nothing to do.'
        }
    }, 200)

def socket_off_ok(index):
    return make_response({
        'success': True,
        'payload': {
            'message': f"Socket {index} state is now OFF."
        }
    }, 200)

def socket_on_ok(index):
    return make_response({
        'success': True,
        'payload': {
            'message': f"Socket {index} state is now ON."
        }
    }, 200)

def all_sockets_on_ok():
    return make_response({
        'success': True,
        'payload': {
            'message': "All sockets are now ON."
        }
    }, 200)

def all_sockets_off_ok():
    return make_response({
        'success': True,
        'payload': {
            'message': "All sockets are now OFF."
        }
    }, 200)