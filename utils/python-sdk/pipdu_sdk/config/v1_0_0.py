
def parse_client_config(data):
    if 'servers' not in data or not isinstance(data['servers'], list):
        raise ValueError('Invalid or missing `servers`')

    parsed_servers = []

    for server in data['servers']:
        validate_server_dict(server)
        parsed_servers.append(server)

    return parsed_servers


def validate_server_dict(server):
    if not isinstance(server, dict):
        raise ValueError('Invalid `servers`. Expected list of maps.')

    supported_keys = ['id', 'name', 'host', 'apiPort', 'metricsPort']
    required_keys = ['id', 'host']

    unsupported_keys = server.keys() - supported_keys
    if (len(unsupported_keys) > 0):
        raise ValueError(f"Unsupported key(s) in server: {unsupported_keys}")

    if (len(server.keys()) != len(required_keys)):
        raise ValueError(f"Missing key(s) in server: {required_keys - server.keys()}")
