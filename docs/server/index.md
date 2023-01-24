# PiPDU Server

The piPDU server is a multi-part component of the piPDU project. It is build using an Arduino Mega and a Raspberry Pi.

The Raspberry pi hosts an API server written in Python. It listens for requests on paths under `/api/v1/sockets/<number>`. The API parses the number and sends it over a serial connection to an Arduino Mega.

The Arduino Mega interacts with the physical aspects of the project and serves 2 main functions. Firstly, it controls the 16 relay board based the commands received via the serial connection from the Raspberry. Secondly, it polls the 16 current sensors for readings and sends them back to the Pi via the serial connection.

Additionally, the Raspberry listens for messages on the serial connection, parses them and exposes them as a Prometheus endpoint.

<!-- TODO: add schematic and some diagrams or something -->
