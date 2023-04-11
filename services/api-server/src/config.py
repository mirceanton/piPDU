import yaml
from relay import Relay

default_api = {
    'host': '0.0.0.0',
    'port': 3000
}

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

api_port = int( config['data'].get('api', default_api).get('port', default_api['port']) )
api_host = config['data'].get('api', default_api).get('host', default_api['host'])

relays = []
for r in data.get('data').get('relays'):
    relay = Relay(
        pin=r['pin'],
        initialState=r.get('initialState', True),
        reversed=r.get('reversed', False)
    )
    relays.append(relay)
