from pipdu_sdk import PiPDU


def parse_client_config(data):
    if 'servers' not in data or not isinstance(data['servers'], dict):
        raise ValueError('Invalid or missing `servers`')

    parsed_servers = {}

    for server_id, server_data in data['servers'].items():
        validate_server_dict(server_data)
        parsed_servers[server_id] = PiPDU(
            host=server_data.get('host'),
            name=server_data.get("name", ""),
            apiPort=server_data.get('apiPort', 3000),
            metricsPort=server_data.get('metricsPort', 8000)
        )

    return parsed_servers


def validate_server_dict(server):
    if not isinstance(server, dict):
        raise ValueError('Invalid `servers`.')

    supported_keys = ['host', 'apiPort', 'metricsPort']
    required_keys = ['host']

    unsupported_keys = set(server.keys()) - set(supported_keys)
    if (len(unsupported_keys) > 0):
        raise ValueError(f"Unsupported key(s) in server: {unsupported_keys}")

    for key in required_keys:
        if key not in server:
            raise ValueError(f"Missing key in server: {key}")
