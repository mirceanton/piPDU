#include "TimedAction.h"

#define ZEROS {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
#define MAXVAL {2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048}

// ================================================================================================
// RELAY VARIABLES
// ================================================================================================
const int numRelays = 16;
const int relayPins[numRelays] ={41, 42, 44, 49, 50, 52, 38, 43, 46, 51, 39, 40, 45, 47, 48, 53};
const int relayDelay = 100;
int relayStates[numRelays] = ZEROS;

// ================================================================================================
// SENSOR VARIABLES
// ================================================================================================
const int numSensors = numRelays;
const int sensorPins[numSensors] = {A11, A10, A1/*??*/, A7, A6, A2, A14, A15, A5, A0, A9, A12, A13, A3, A4, A1};
const int mVperAmp[numSensors] = {145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145};
const int noiseLevel[numSensors] = {8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8};
const int sensorSamples = 1000;

// ================================================================================================
// RELAY FUNCTIONS
// ================================================================================================
void setupRelays() {
  for (int i = 0; i < numRelays; i++) {
    pinMode(relayPins[i], OUTPUT);
    turnOnRelay(i);
    delay(relayDelay);
  }
}

void turnOnRelay(int relayNumber) {
  // Make sure the relay number is valid
  if (relayNumber < 0 || relayNumber > numRelays) return;

  // Turn on the relay and update the state in the array
  digitalWrite(relayPins[relayNumber], HIGH);
  relayStates[relayNumber] = 1;
}

void turnOffRelay(int relayNumber) {
  // Make sure the relay number is valid
  if (relayNumber < 0 || relayNumber > numRelays) return;

  // Turn off the specified relay and update the state in the array
  digitalWrite(relayPins[relayNumber], LOW);
  relayStates[relayNumber] = 0;
}

void toggleRelay(int relayNumber) {
  // Make sure the relay number is valid
  if (relayNumber < 0 || relayNumber > numRelays) return;

  if (relayStates[relayNumber] == 0) {
    return turnOnRelay(relayNumber);
  }
  return turnOffRelay(relayNumber);
}

void listenToSerial() { // FIXME
  // Check if there are any characters available on the serial connection
  if (Serial.available() > 0) {
    // Read the next available character
    char c = Serial.read();

    // If the character is between 'a' and 'p', toggle the corresponding relay
    if (c >= 'a' && c <= 'p') {
      int relayNumber = c - 'a'; // Calculate the relay number
      toggleRelay(relayNumber);
    }
    
    // If the character is 'q', turn OFF all relays
    if (c == 'q') {
      for (int i = 0; i < numRelays; i++) {
        turnOffRelay(i);
      }
    }
    
    // If the character is 'r', turn ON all relays
    if (c == 'r') {
      for (int i = 0; i < numRelays; i++) {
        turnOnRelay(i);
      }
    }
  }
}

// ================================================================================================
// SENSOR FUNCTIONS
// ================================================================================================
void setupSensors() {
  for (int i = 0; i < numSensors; i++) {
    pinMode(sensorPins[i], INPUT);
  }
}

void getVPPs(double *vpps) {
  int minValues[numSensors] = MAXVAL;
  int maxValues[numSensors] = ZEROS;
  int readValue = 0;

  uint32_t start_time = millis();
  while ( (millis() - start_time) < sensorSamples ) {
    for (int i = 0; i < numSensors; i++) {
      readValue = analogRead(sensorPins[i]);

      if (readValue > maxValues[i]) {
        maxValues[i] = readValue;
      }

      if (readValue < minValues[i]) {
        minValues[i] = readValue;
      }
    }
  }

  int delta = 0;
  for (int i = 0; i < numSensors; i++) {
    delta = maxValues[i] - minValues[i];
    vpps[i] = ( (delta > noiseLevel[i] ? delta : 0) * 5.0 ) / 1024.0;
  }
}

void readSensors(double *values) {
  double voltages[numSensors] = ZEROS;
  getVPPs(voltages);
  for (int i = 0; i < numSensors; i++) {
    values[i] = ( ((voltages[i] / 2.0) * 0.707) * 1000 ) / mVperAmp[i];
  }
}

void metricsThreadFunction() {
  double metrics[numSensors] = ZEROS;
  readSensors(metrics);

  for (int i = 0; i < numSensors; i++) {
    Serial.print("s");
    Serial.print(i);
    Serial.print(":");
    Serial.print(metrics[i]);
    if (i < numSensors - 1) {
      Serial.print("\t");
    }
  }

  Serial.print("\r\n");
}

// ================================================================================================
// THREADING SETUP
// ================================================================================================
const int metricsThreadInterval = 500;
const int serialThreadInterval = 50;
TimedAction metricsThread = TimedAction(metricsThreadInterval, metricsThreadFunction);
TimedAction serialThread = TimedAction(serialThreadInterval, listenToSerial);

// ================================================================================================
// MAIN FUNCTIONS
// ================================================================================================
void setup() {
  setupRelays();
  setupSensors();

  // Initiate serial communication
  Serial.begin(9600);
}

void loop() {
  metricsThread.check();
  serialThread.check();
}
