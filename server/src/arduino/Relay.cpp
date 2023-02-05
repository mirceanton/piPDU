#include "Relay.h"

Relay::Relay(int _pin) {
  pinMode(_pin, OUTPUT);
  pin = _pin;
  on();
}

Relay::Relay(int _pin, bool defaultState) {
  pinMode(_pin, OUTPUT);
  pin = _pin;

  if (defaultState) on();
  else off();
}

Relay::Relay(int _pin, int onSignal, int offSignal, bool defaultState) {
  pinMode(_pin, OUTPUT);
  pin = _pin;
  ON = onSignal;
  OFF = offSignal;

  if (defaultState) on();
  else off();
}

void Relay::on() {
  Serial.print("Turning on relay ");
  Serial.println(pin);

  digitalWrite(pin, ON);
  state = true;
}

void Relay::off() {
  Serial.print("Turning off relay ");
  Serial.println(pin);

  digitalWrite(pin, OFF);
  state = false;
}

void Relay::toggle() {
  if (state == true) off();
  else on();
}

void Relay::setOnSignal(int signal) {
  ON = signal;
}

void Relay::setOffSignal(int signal) {
  OFF = signal;
}