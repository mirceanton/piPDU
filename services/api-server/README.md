# PiPDU API Server

The `api-server` project is a Flask-based microservice meant to run on the PiPDU server in order to facilitate interacting with the relays

 web server that exposes a REST API to control relays on a Raspberry Pi.

## Directory Structure

The API Server's directory structure is as follows:

```bash
api-server/
├── Dockerfile # docker image recipe
├── requirements.txt # required dependencies
├── src/
│   ├── api.py # defines the API routes
│   ├── config.py # handles the config file parsing
│   ├── globals.py # stores global variables
│   ├── __init__.py # starts the API server
│   └── relay.py # abstracts away the interaction with the relays
├── tests/
│   ├── test_api.py
│   ├── test_config.py
│   └── test_relay.py
└── VERSION
```

## Flask Application

The Flask application code is in the src/api.py file. The application defines the following endpoints:

- `GET /relays/<int:index>`: Returns the state of the relay with the specified index.
- `PUT /relays/<int:index>?state={state}`: Sets the state of the relay with the specified index to the specified state.
- `GET /relays`: Returns the state of all the relays.
- `PUT /relays?state={state}`: Sets the state of all the relays to the specified state.

The endpoints take an integer index parameter that specifies the `index` of the relay to get or set. The PUT endpoints also take a `state` parameter that specifies the desired state of the relay(s) as a string (`true` or `false`).

## Configuration File

The configuration file is in YAML format and specifies the pins, initial states, and reversed status of the relays. The file is loaded by the parse_yaml function in src/config.py and used to create a list of Relay objects.

The configuration file must have the following structure:

```yaml
apiVersion: v1.0.0
kind: ApiServerConfig
data:
  relays:
    - pin: 17
      initialState: true
      reversed: false
    - pin: 18
      initialState: false
      reversed: true
```

Each relay is specified as a dictionary with the following keys:

| Key | Type |Description | Required | Default |
| :-: | :-: | :- | :-: | :-: |
| `pin`| `int` | The GPIO pin number that the relay is connected to, in BCM format | Required | `N/A` |
| `initialState` | `bool` | The initial state that will be assigned to the relay | Optional | `True` |
| `reversed` | `bool` | Whether or not the circuit is wired to the `NC` or `NO` of the relay, i.e. if the circuit is active when the relay is supplied with 5V (`True`) or if it is active when it is pulled to ground (`False`) | Optional | `False` |

## Running the API Server

To run the API server, first build the Docker image using the Dockerfile:

```bash
docker build -t api-server .
```

Then run the Docker container:

```bash
docker run -d --name api-server -p 3000:3000 api-server
```

This will start the API server and expose it on port `3000`.

## Running Unit Tests

To run the unit tests, navigate to the project root directory and run the following command:

```
pip3 install pytest
python3 -m pytest tests/
```

This will run all the tests in the `tests/` directory.
