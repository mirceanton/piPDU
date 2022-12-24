# =================================================================================================
# This file contains some predefined responses for the API server to make the code more readable.
# =================================================================================================
from flask import make_response
from utils.logger import logger

def index_out_of_range():
    """Error Response if the given socket id is out of range."""
    logger.error('Socket number should be between 0 and 15')
    return make_response({
        'success': False,
        'payload': {},
        'error': {
            'code': 'OOR (out-of-range)',
            'message': 'Socket number should be between 0 and 15',
        }
    }, 400)

def nothing_to_do():
    """OK Response for no action to be done"""
    logger.info('The requested state is the same with the current state. There is nothing to do.')
    return make_response({
        'success': True,
        'payload': {
            'message': 'The requested state is the same with the current state. There is nothing to do.'
        }
    }, 200)

def socket_off_ok(index):
    """OK Custom info response for turning a socket off"""
    logger.info(f"Socket {index} state is now OFF.")
    return make_response({
        'success': True,
        'payload': {
            'message': f"Socket {index} state is now OFF."
        }
    }, 200)

def socket_on_ok(index):
    """OK Response for turning a socket on"""
    logger.info(f"Socket {index} state is now ON.")
    return make_response({
        'success': True,
        'payload': {
            'message': f"Socket {index} state is now ON."
        }
    }, 200)

def all_sockets_off_ok():
    """OK Response for turning all sockets off"""
    logger.info("All sockets are now Off.")
    return make_response({
        'success': True,
        'payload': {
            'message': "All sockets are now OFF."
        }
    }, 200)

def all_sockets_on_ok():
    """OK Response for turning all sockets on"""
    logger.info("All sockets are now ON.")
    return make_response({
        'success': True,
        'payload': {
            'message': "All sockets are now ON."
        }
    }, 200)
