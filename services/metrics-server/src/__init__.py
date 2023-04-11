from arduino import Arduino
from prometheus_client import start_http_server, Gauge, CollectorRegistry
import config
import time

# Connect to the Arduino board over serial
arduino = Arduino(
    device=config.serial_device,
    baud_rate=config.serial_baud
)

# Define a new Collector Registry 
socket_registry = CollectorRegistry()

# Define a Prometheus gauge for each current sensor to expose
socket_gauges = []
for i in range(0, len(config.sensors)):
    socket_gauges.append(Gauge('socket_{}_amps'.format(i), 'Current consumption for socket {} in Amps'.format(i), registry=socket_registry))

# Start the Prometheus HTTP server
start_http_server(config.server_port, registry=socket_registry)

# Loop forever, reading values from the Arduino and updating the Prometheus metrics
try:
    while True:
        if arduino.hasMessage():
            message = arduino.read()

            # Split the line into float values
            values = [float(x) for x in message.split(' ')]

            # Ensure the number of sensor readings matches the number of configured gauges
            if len(values) != len(socket_gauges):
                raise RuntimeError("Invalid number of sensor readings!")

            # Update the Prometheus metrics with the new values
            for i, gauge in enumerate(socket_gauges):
                gauge.set(values[i])

        time.sleep(config.poll_interval_seconds)
except KeyboardInterrupt:
    print('INFO: Received Keyboard Interrupt')
    arduino.close()
