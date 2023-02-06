#include "Relay.h"
#include "ACS712.h"

const int numSockets = 16;

// ================================================================================================
// RELAY VARIABLES
// ================================================================================================
const int relayPins[numSockets] ={41, 42, 44, 49, 50, 52, 38, 43, 46, 51, 39, 40, 45, 47, 48, 53};
Relay *relays[numSockets];

// ================================================================================================
// SENSOR VARIABLES
// ================================================================================================
const int sensorPins[numSockets] = {A11, A10, A1/*??*/, A7, A6, A2, A14, A15, A5, A0, A9, A12, A13, A3, A4, A1};
ACS712 *sensors[numSockets];
const int mVperAmp[numSockets] = {145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145};
const int noiseLevel[numSockets] = {8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8};
const int sensorSamples = 500;

void serialThread() { // FIXME
  // Check if there are any characters available on the serial connection
  if (Serial.available() > 0) {
    // Read the next available character
    char c = Serial.read();

    // If the character is between 'a' and 'p', toggle the corresponding relay
    if (c >= 'a' && c <= 'p') {
      int relayNumber = c - 'a'; // Calculate the relay number
      relays[relayNumber]->toggle();
    }
    
    // If the character is 'q', turn OFF all relays
    if (c == 'q') {
      for (int i = 0; i < numSockets; i++) {
        relays[i]->off();
      }
    }
    
    // If the character is 'r', turn ON all relays
    if (c == 'r') {
      for (int i = 0; i < numSockets; i++) {
        relays[i]->on();
      }
    }
  }
}

void metricsThread() {
  for (int i = 0; i < sensorSamples; i++) {
    for (int j = 0; j < numSockets; j++) {
      sensors[j]->poll();
    }
  }

  for (int i = 0; i < numSockets; i++) {
    Serial.print("s");
    Serial.print(i);
    Serial.print(":");
    Serial.print( sensors[i]->getCurrent() );
    if (i < numSockets - 1) {
      Serial.print("\t");
    }
  }

  Serial.print("\r\n");
}

// ================================================================================================
// MAIN FUNCTIONS
// ================================================================================================
void setup() {
  // Initiate serial communication
  Serial.begin(9600);

  for (int i = 0; i < numSockets; i++) {
    relays[i] = new Relay(relayPins[i], true);
    sensors[i] = new ACS712(sensorPins[i], mVperAmp[i]);
  }
}

void loop() {
  metricsThread();
  serialThread();
}
