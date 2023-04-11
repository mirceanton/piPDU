import pytest
import yaml
import RPi.GPIO as GPIO
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from relay import Relay

# Default values for Relay initialization
pin = 10
initialState = True
reversed = False


@pytest.fixture
def gpio_mock():
    gpio_mock = MagicMock()
    GPIO.setup = gpio_mock.setup
    GPIO.output = gpio_mock.output
    GPIO.cleanup = gpio_mock.cleanup
    yield gpio_mock


def test_relay_initialization(gpio_mock):
    relay = Relay(pin, initialState, reversed)

    GPIO.setup.assert_called_once_with(pin, GPIO.OUT)
    GPIO.output.assert_called_once_with(pin, initialState)
    assert relay.pin == pin
    assert relay.current_state == initialState
    assert relay.reversed == reversed


def test_relay_set_state(gpio_mock):
    relay = Relay(pin, initialState, reversed)
    gpio_mock.reset_mock()

    new_state = not initialState
    relay.set_state(new_state)

    GPIO.output.assert_called_once_with(pin, new_state if not reversed else not new_state)
    assert relay.current_state == new_state


def test_relay_get_state(gpio_mock):
    relay = Relay(pin, initialState, reversed)
    assert relay.get_state() == initialState


def test_relay_cleanup(gpio_mock):
    relay = Relay(pin, initialState, reversed)
    del relay
    GPIO.cleanup.assert_called_once_with(pin)
