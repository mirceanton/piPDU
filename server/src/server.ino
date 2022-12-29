const int numRelays = 16;
const int numSensors = numRelays;
const int relayPins[numRelays] = {38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53};
const int sensorPins[numSensors] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15};

// The interval at which the tasks should be re-ran
const int metricsThreadInterval = 500;
const int serialThreadInterval = 500;

// The number of samples to collect to calculate an average value for the sensors
const int metricsSamples = 150;

// The amount of time in milliseconds to wait between 2 consequent measuremets
const int metricsDelay = 3;

// Array to store the state of each relay
int relayStates[numRelays] = {0};

// Delay between turning on each relay in milliseconds during setup
const int relayDelay = 100;

// This function sets all relay pins as outputs
// and turns them on with a delay between each
void setupRelays() {
  for (int i = 0; i < numRelays; i++) {
    pinMode(relayPins[i], OUTPUT);
    turnOnRelay(i);
    delay(relayDelay);
  }
}

// This function sets up all the sensor pins as inputs
void setupSensors() {
  for (int i = 0; i < numSensors; i++) {
    pinMode(sensorPins[i], INPUT);
  }
}

// This function turns on a specified relay
void turnOnRelay(int relayNumber) {
  // Make sure the relay number is valid
  if (relayNumber < 0 || relayNumber > numRelays) return;

  // Turn on the relay and update the state in the array
  digitalWrite(relayPins[relayNumber], LOW);
  relayStates[relayNumber] = LOW;
}

// This function turns off a specified relay
void turnOffRelay(int relayNumber) {
  // Make sure the relay number is valid
  if (relayNumber < 0 || relayNumber > numRelays) return;

  // Turn off the specified relay and update the state in the array
  digitalWrite(relayPins[relayNumber], HIGH);
  relayStates[relayNumber] = HIGH;
}

// This function toggles the state of a specified relay
void toggleRelay(int relayNumber) {
  // Make sure the relay number is valid
  if (relayNumber < 0 || relayNumber > numRelays) return;

  // Toggle the state of the specified relay
  if (relayStates[relayNumber] == LOW) turnOffRelay(relayNumber);
  else turnOnRelay(relayNumber);
}

// This function listens to the serial connection
// and takes action based on the received characters
void listenToSerial() {
  // Check if there are any characters available on the serial connection
  if (Serial.available() > 0) {
    // Read the next available character
    char c = Serial.read();

    // If the character is between 'a' and 'p', turn off the corresponding relay
    if (c >= 'a' && c <= 'p') {
      int relayNumber = c - 'a'; // Calculate the relay number
      turnOffRelay(relayNumber);
    }

    // If the character is between 'A' and 'P', turn on the corresponding relay
    if (c >= 'A' && c <= 'P') {
      int relayNumber = c - 'A'; // Calculate the relay number
      turnOnRelay(relayNumber);
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

// This function reads the values from all 16
// and prints them in a CSV list over the serial connection
void readSensors() {
  // Array to store the sensor values
  int sensorValues[numSensors] = {0};

  // Read the sensor values
  for (int i = 0; i < metricsSamples; i++) {
    for (int j = 0; j < numSensors; j++) {
      sensorValues[j] += analogRead(sensorPins[j]);
    }

    // Delay for 3 milliseconds before reading
    // the next value for the ADC to settle
    delay(metricsDelay);
  }

  // Calculate the average sensor value for each sensor
  for (int i = 0; i < numSensors; i++) {
    float averageValue = (float)sensorValues[i] / metricsSamples;
    float power = (0.0264 * averageValue) - 13.51;

    // Print the power draws to the serial monitor, separated by commas
    Serial.print(power);
    if (i < numSensors - 1) Serial.print(",");
  }
  // Add a newline character at the end
  Serial.println();
}

// Dedicated "thread" for the metrics collecting and exporting
TimedAction metricsThread = TimedAction(metricsThreadInterval, readSensors);

// Dedicated "thread" for listening to commands over serial
TimedAction serialThread = TimedAction(serialThreadInterval, listenToSerial);

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
