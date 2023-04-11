import yaml
from relay import Relay


def parse_yaml(file_path):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    relays = []
    for r in data.get('data').get('relays', []):
        relay = Relay(
            pin=r['pin'],
            initialState=r.get('initialState', True),
            reversed=r.get('reversed', False)
        )
        relays.append(relay)

    return relays
