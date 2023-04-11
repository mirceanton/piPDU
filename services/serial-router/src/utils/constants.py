import os

# Get the serial device and baud rate from environment variables
SERIAL_DEVICE = os.environ.get('SERIAL_DEVICE', '/dev/ttyACM0')
SERIAL_BAUDRATE = int(os.environ.get('SERIAL_BAUDRATE', '921600'))

METRICS_FIFO = os.environ.get('METRICS_FIFO', '/tmp/metrics_fifo')
COMMANDS_FIFO = os.environ.get('COMMANDS_FIFO', '/tmp/commands_fifo')
