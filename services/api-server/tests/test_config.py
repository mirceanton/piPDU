import pytest
import yaml
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from relay import Relay
from config import parse_yaml


def test_parse_yaml():
    test_yaml = '''
    apiVersion: v1.0.0
    kind: ApiServerConfig
    data:
        relays:
        - pin: 1
          initialState: false
          reversed: true
    '''
    with open('test.yaml', 'w') as f:
        f.write(test_yaml)

    relays = parse_yaml('test.yaml')

    assert isinstance(relays, list)
    assert len(relays) == 1
    assert isinstance(relays[0], Relay)
    assert relays[0].pin == 1
    assert relays[0].get_state() == False
    assert relays[0].reversed == True

    # Clean up the test YAML file
    os.remove('test.yaml')
