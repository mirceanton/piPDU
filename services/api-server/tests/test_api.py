import pytest
import yaml
import RPi.GPIO as GPIO
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from relay import Relay
from config import parse_yaml
from api import app


# Fixture for setting up and tearing down the Flask app for testing
@pytest.fixture
def client():
    config_yaml = '''
    apiVersion: v1.0.0
    kind: ApiServerConfig
    data:
        relays:
        - pin: 1
          initialState: true
          reversed: false
    '''
    with open('config.yaml', 'w') as f:
        f.write(config_yaml)

    with app.test_client() as client:
        yield client
    os.remove('config.yaml')

def test_get_relay_state(client):
    response = client.get('/relays/0')
    assert response.status_code == 200
    assert response.json == {'pin': 1, 'state': True}

def test_get_relay_state_invalid_index(client):
    response = client.get('/relays/1')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid relay index'}
    
def test_set_relay_state(client):
    response = client.put('/relays/0?state=false')
    assert response.status_code == 200
    assert response.json == {'pin': 1, 'state': False}

    response = client.put('/relays/0?state=true')
    assert response.status_code == 200
    assert response.json == {'pin': 1, 'state': True}

def test_set_relay_state_invalid_index(client):
    response = client.put('/relays/1?state=true')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid relay index'}

def test_set_relay_state_missing_state(client):
    response = client.put('/relays/0')
    assert response.status_code == 400
    assert response.json == {'error': 'Missing state parameter'}


def test_get_all_relay_state(client):
    response = client.get('/relays')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0] == {'pin': 1, 'state': True}

def test_set_all_relay_state(client):
    response = client.put('/relays?state=false')
    assert response.status_code == 200
    assert response.json == [{'pin': 1, 'state': False}]
    
def test_set_all_relay_state_missing_state(client):
    response = client.put('/relays')
    assert response.status_code == 400
    assert response.json == {'error': 'Missing state parameter'}
