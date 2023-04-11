import os

FIFO = os.environ.get('FIFO', '/tmp/metrics_fifo')

# Get the API server host and port from environment variables
API_HOST = os.environ.get('API_HOST', '0.0.0.0')
API_PORT = int(os.environ.get('API_PORT', '3000'))
