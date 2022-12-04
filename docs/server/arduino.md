
The Arduino sketch allows you to control a 16-relay board and read the values from 16 analog current sensors.

### Requirements

- Arduino Mega or compatible board
- 16-relay board
- 16 analog current sensors

### Installation

- Clone or download this repository.
- Open the `server.ino` file in the Arduino IDE.
- Install the required libraries (see below).
- Connect the relay board and sensors to the Arduino board according to the pin assignments in the code.
- Upload the sketch to the Arduino board.

### Libraries

This sketch requires the following libraries:

- `TimedAction.h`: used for creating and running multiple tasks.

### Usage

Once the sketch is uploaded to the Arduino board, you can control the relays and read the sensor values using the serial connection. The following commands are supported:

- `a` - `p`: toggle the corresponding relay (`a` corresponds to relay 0, `b` corresponds to relay 1, etc.).
- `q`: turn off all relays.
- `r`: turn on all relays.

The sensor values are printed to the serial connection twice per second, on a single line, separated by commas.

### Limitations

 A few limitations to keep in mind when using this code:

- The Arduino UNO board only has 2KB of SRAM, which means that it is not capable of running multiple tasks simultaneously. In order to run multiple tasks on an Arduino board, you will need to use a board with more SRAM, such as the Arduino Mega.
- The code assumes that the relays are on when the pin is LOW and off when it is HIGH. If your relay board uses a different configuration, you will need to modify the code accordingly.
- The code uses a hard-coded formula to calculate the power draw from the sensor values. This formula may not be accurate for all types of sensors, so you may need to modify it depending on your specific sensors.
- The code does not include any error handling or validation, so it may not be robust in the face of unexpected input or malfunctions. It is recommended to add error handling and validation to the code if you plan to use it in a production environment.