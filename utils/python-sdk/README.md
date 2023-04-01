# PiPDU - Python SDK

PiPDU is a Python package for controlling and monitoring PiPDU power distribution units.  
It allows you to:

- get global metrics
- get metrics for a specific socket
- get the state of a socket
- set the state of a socket
- test the connection to the PiPDU unit.

## Installation

You can install PiPDU using pip:

```bash
pip install pipdu
```

## Usage

To use PiPDU, import the PiPDU class from the `pipdu` module, and create an instance of the class with the certificate, host, and optional API and metrics ports:

```python
from pipdu import PiPDU

certificate = "path/to/certificate.pem"
host = "192.168.1.100"
api_port = 3000
metrics_port = 8000

pdu = PiPDU(host, api_port, metrics_port, certificate)
```

### Getting the Global Metrics

To get the global metrics for all sockets, call the `getGlobalMetrics` method:

```python
metrics = pdu.getGlobalMetrics()
```

This method returns a list of `floats` representing the current drawn on each socket.

### Getting Metrics for a Specific Socket

To get the metrics for a specific socket, call the `getMetricsFor` method with the socket ID:

```python
socket_id = 1
metrics = pdu.getMetricsFor(socket_id)
```

This method returns a `float` representing the current drawn by the specified socket.

### Getting the State of a Socket

To get the state of a socket, call the `getStateFor` method with the socket ID:

```python
socket_id = 1
state = pdu.getStateFor(socket_id)
```

This method returns a `boolean` value representing the current state of the specified socket (`True` for on, `False` for off).

### Setting the State of a Socket

To set the state of a socket, call the `setStateFor` method with the socket ID and the desired state (`True` for on, `False` for off):

```python
socket_id = 1
state = True
pdu.setStateFor(socket_id, state)
```

This method sets the state of the specified socket to the desired state.

### Testing the Connection

To test the connection to the PiPDU unit, call the `testConnection` method:

```python
connected = pdu.testConnection()
```

This method returns a `boolean` value representing whether the connection to the PiPDU unit was successful (`True` for connected, `False` for not connected).

## Notes

- The certificate parameter is the path to the certificate file for HTTPS connections. If you are using HTTP, you can pass an empty string.
- The API port and metrics port default to `3000` and `8000`, respectively, but can be changed if necessary.
