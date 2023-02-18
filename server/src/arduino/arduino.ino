#include "Relay.h"
#include "ACS712.h"

const int numSockets = 16;
unsigned long time;

// ================================================================================================
// RELAY VARIABLES
// ================================================================================================
const int relayPins[numSockets] = {41, 42, 44, 49, 50, 52, 38, 43, 46, 51, 39, 40, 45, 47, 48, 53};
Relay *relays[numSockets];

// ================================================================================================
// SENSOR VARIABLES
// ================================================================================================
const int sensorPins[numSockets] = {A11, A10, A1, A7, A6, A2, A14, A15, A5, A0, A9, A12, A13, A3, A4, A1};
ACS712 *sensors[numSockets];

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < numSockets; i++) {
    relays[i] = new Relay(relayPins[i], true);
    sensors[i] = new ACS712(sensorPins[i], 145);
    sensors[i]->setNoiseFloor(0.1);
  }
}

void loop() {
  for(int i = 0; i < 500; i++) {
    for (int j = 0; j < numSockets; j++) {
      sensors[j]->poll();
    }
  }

  String message = "";
  for (int i = 0; i < numSockets; i++) {
    message += String(sensors[i]->getAmps()) + " ";
  }
  Serial.println(message);
}

void serialEvent() {
  if (Serial.available() <= 0) return;

  const char message = Serial.read();

  if (message == 'q') {
    for (int i = 0; i < numSockets; i++) {
      relays[i]->off();
    }
    return;
  }

  if (message == 'r') {
    for (int i = 0; i < numSockets; i++) {
      relays[i]->on();
    }
    return;
  }

  if (isUpperCase(message)) {
    const int relayId = (message - 'A');
    if (0 <= relayId && relayId < 16) {
      relays[relayId]->on();
    }
  } else {
    const int relayId = (message - 'a');
    if (0 <= relayId && relayId < 16) {
      relays[relayId]->off();
    }
  }
}
