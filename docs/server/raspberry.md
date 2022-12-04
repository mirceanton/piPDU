## The API Server

### Usage

To use this API server, you need to have Python 3 and the required libraries installed on your system. You also need to have an Arduino Mega connected to your Raspberry via a serial/USB connection.

To install the required libraries, run the following command:

```bash
pip3 install -r server-requirements.txt
```

To run the API server, use the following command:

```bash
python3 server.py
```

This will start the API server and the serial listener thread. You can then send commands to the Arduino Mega by making a POST request to the API server using the following URL format:

```bash
http://<host>:<port>/api/v1/sockets/<number>
```

Where `<host>` is the hostname or IP address of the computer running the API server, `<port>` is the port number on which the API server is listening, and `<number>` is the id of the socket that will be toggled on/off.

For example, if the API server is running on localhost on port 8080, you can send toggle the socket `5` by making the following POST request:

```bash
http://localhost:8080/api/v1/sockets/5
```

You can access the Prometheus metrics endpoint by making a GET request to the following URL:

```bash
http://<host>:<port>/metrics
```

The metrics endpoint will return the current values of the 16 gauges, which are named socket_0, socket_1, ..., socket_15 and represent the 16 sockets on the Arduino Mega.

### Configuration

The API server and the serial listener thread can be configured using the `config.yaml` file. This file should be in the same directory as the `server.py` script.

A basic `config.yaml` file has the following format:

``` yaml
api:
  host: 0.0.0.0
  port: 8080

metrics:
  enabled: true

arduino:
  device: /dev/ttyACM0
  baud: 9600
```

The `api` section contains the settings to configure the Flask API server `host` and `port`.

The `metrics` section contains the on/off toggle for the Prometheus `/metrics` endpoint.

The `arduino` section contains the settings for the serial connection to the Arduino Mega. The `device` field specifies the device file name of the serial connection and the `baud` field specifies the baud rate.

After modifying the `config.yaml` file, you need to restart the `server.py` script to apply the changes.

### Exception Handling

The API server and the serial listener thread can throw exceptions under certain conditions. For example, if the config file is not found or if the connection to the Arduino Mega is not successful.

When an exception is thrown, the `server.py` script catches the exception and logs it to the standard output.
