#ifndef ACS712_h
#define ACS712_h

#include <Arduino.h>

class ACS712 {
  public:
    ACS712(int _pin, int _mVperAmp);
    void setmVperAmp(int _mVperAmp);

    void pollForMillis(int _millis);
    void poll();
    double getCurrent();
    int getRaw();
private:
  int pin;
  int mVperAmp;

  int maxValue = 0;
  int minValue = 1024;
};

#endif