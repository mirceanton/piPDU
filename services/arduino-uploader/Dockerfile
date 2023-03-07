FROM ubuntu:20.04

# Install the required packages
RUN apt update && apt upgrade -y
RUN apt install curl make -y
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# Set up arduino-cli
RUN arduino-cli config init
RUN arduino-cli core install arduino:avr

# Set the root directory for the app
WORKDIR /arduino

# Copy over the files into the working directory
COPY src/* ./

# Start the router
CMD ["make", "all"]
