#include <Wire.h>
#include "Relay.h"
#include "ACS712.h"

const int numSockets = 16;

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

void onReceiveHandler() {
  if (!Wire.available()) return;

  const char message = Wire.read();
  Serial.println("Got message from i2c: " + String(message));

  if (message == 'q') {
    Serial.println("Turning off all relays...");
    for (int i = 0; i < numSockets; i++) {
      relays[i]->off();
    }
    return;
  }

  if (message == 'r') {
    Serial.println("Turning on all relays...");
    for (int i = 0; i < numSockets; i++) {
      relays[i]->on();
    }
    return;
  }

  const int relayId = (message - 'a');
  if (0 <= relayId && relayId < 16) {
    Serial.println("Toggling relay " + String(relayId));
    relays[relayId]->toggle();
    return;
  }

  Serial.println("Invalid relay ID: " + String(relayId) + " (" + message + ")");
}

void onRequestHandler() {
  String message = "";
  for (int i = 0; i < numSockets; i++) {
    message += String(sensors[i]->getAmps());
    message += ",";
  }
  message += "\n";

  char buffer[1024];
  message.toCharArray(buffer, message.length());
  Wire.write(buffer);
  Serial.println(buffer);
}

void setup() {
  Serial.begin(9600);
  Serial.println("Starting initialization");

  Serial.println("Joining the I2C bus...");
  Wire.begin(0x20);
  Serial.println("Setting I2C event handlers...");
  Wire.onReceive(onReceiveHandler);
  Wire.onRequest(onRequestHandler);

  Serial.println("Setting devices...");
  for (int i = 0; i < numSockets; i++) {
    relays[i] = new Relay(relayPins[i], true);
    sensors[i] = new ACS712(sensorPins[i], 145);
    sensors[i]->setNoiseFloor(0.1);
  }
}

void loop() {
  for (int j = 0; j < numSockets; j++) {
    sensors[j]->poll();
  }
}
