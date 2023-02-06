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
const int sensorPins[numSockets] = {A11, A10, A1/*??*/, A7, A6, A2, A14, A15, A5, A0, A9, A12, A13, A3, A4, A1};
ACS712 *sensors[numSockets];
const int sensorSamples = 500;

void handleMessage() {
  if (Wire.available()) {
    char c = Wire.read();
    Serial.print("Got message from i2c: ");
    Serial.println(c);
    
    // If the character is 'q', turn OFF all relays
    if (c == 'q') {
      for (int i = 0; i < numSockets; i++) {
        Serial.println("Turning off all relays...");
        relays[i]->off();
        return;
      }
    }
    
    // If the character is 'r', turn ON all relays
    if (c == 'r') {
      for (int i = 0; i < numSockets; i++) {
        Serial.println("Turning on all relays...");
        relays[i]->on();
        return;
      }
    }

    // If the character is between 'a' and 'p', toggle the corresponding relay
    if (c >= 'a' && c <= 'p') {
      Serial.print("Toggling relay ");
      Serial.println(c-'a');
      relays[ c - 'a' ]->toggle();
    }
  }
}


void setup() {
  // Initiate serial communication
  Serial.begin(9600);
  Serial.println("Starting initialization");

  Serial.println("Joining the I2C bus...");
  Wire.begin(0x20);
  Serial.println("Setting I2C event handler...");
  Wire.onReceive(handleMessage);

  Serial.println("Setting devices...");
  for (int i = 0; i < numSockets; i++) {
    relays[i] = new Relay(relayPins[i], true);
    sensors[i] = new ACS712(sensorPins[i], 145);
    sensors[i]->setNoiseFloor(0.1);
  }
  
  Serial.println("Starting to print sensor readings: ");
  for (int i = 0; i < numSockets; i++) {
    Serial.print("| S");
    Serial.print( i+1 );
    Serial.print("\t|");
  }
  Serial.print("\r\n");
}

void loop() {
  for (int i = 0; i < sensorSamples; i++) {
    for (int j = 0; j < numSockets; j++) {
      sensors[j]->poll();
    }
  }

  for (int i = 0; i < numSockets; i++) {
    Serial.print("| ");
    Serial.print( sensors[i]->getWatts() );
    Serial.print("\t");
  }
  Serial.print("\r\n");
}
