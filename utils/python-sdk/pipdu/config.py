import yaml
from . import v1_0_0 as v1_0_0

API_VERSION_PARSERS = {
    'v1.0.0': {
        "ClientConfig": v1_0_0.parse_client_config,
    },
}


def parse_yaml_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)

    # Validate format and restrictions
    if 'apiVersion' not in config or not isinstance(config['apiVersion'], str):
        raise ValueError('Invalid or missing `apiVersion`')
    if 'kind' not in config or not isinstance(config['kind'], str):
        raise ValueError('Invalid or missing `kind`')

    # Check if supported apiVersion
    if config['apiVersion'] not in API_VERSION_PARSERS:
        raise ValueError(f'Unsupported `apiVersion`: {config["apiVersion"]}')

    if config['kind'] not in API_VERSION_PARSERS[config['apiVersion']]:
        raise ValueError(f'Unsupported `kind`: {config["kind"]}')

    # Call appropriate function based on apiVersion and kind
    return API_VERSION_PARSERS[config['apiVersion']][config['kind']](config)
