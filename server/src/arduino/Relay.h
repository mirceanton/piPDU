#ifndef RELAY_h
#define RELAY_h

#include <Arduino.h>

class Relay {
  public:
    Relay(int _pin);
    Relay(int _pin, bool defaultState);
    Relay(int _pin, int onSignal, int offSignal, bool defaultState);

    void on();
    void off();
    void toggle();

    void setOnSignal(int signal);
    void setOffSignal(int signal);

  private:
    bool state;
    int pin;

    int ON = HIGH;
    int OFF = LOW;
};

#endif