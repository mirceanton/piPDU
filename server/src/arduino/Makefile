all: compile upload

compile:
	arduino-cli compile arduino.ino --fqbn arduino:avr:mega -v;

upload:
	arduino-cli upload arduino.ino --fqbn arduino:avr:mega -p /dev/ttyACM0 -v;

monitor:
	arduino-cli monitor -p /dev/ttyACM0 --config baudrate=921600;

debug: compile upload monitor

fix:
	sudo ln -s /lib/ld-linux-armhf.so.3 /lib/ld-linux.so.3;
