
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

    unsupported_keys = set(server.keys()) - set(supported_keys)
    if (len(unsupported_keys) > 0):
        raise ValueError(f"Unsupported key(s) in server: {unsupported_keys}")

    for key in required_keys:
        if key not in server:
            raise ValueError(f"Missing key in server: {key}")
