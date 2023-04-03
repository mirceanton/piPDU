
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

    server_template = {
        'id': str,
        'name': str,
        'host': str,
        'apiPort': int,
        'metricsPort': int,
    }

    unsupported_keys = set(server.keys()) - set(server_template.keys())
    if (len(unsupported_keys) > 0):
        raise ValueError(f"Unsupported key(s) in server: {unsupported_keys}")

    # Ensure data type integrity
    for key, datatype in server_template:
        if key not in server or not isinstance(server[key], datatype):
            raise ValueError(f"Invalid or missing server.`{key}`")
