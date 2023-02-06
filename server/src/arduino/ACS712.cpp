#include "ACS712.h"

ACS712::ACS712(int _pin, int _mVperAmp) {
  pinMode(_pin, INPUT);
  pin = _pin;
  mVperAmp = _mVperAmp;
}

void ACS712::setmVperAmp(int _mVperAmp) {
  mVperAmp = _mVperAmp;
}

void ACS712::pollForMillis(int _millis) {
  int readValue;
  minValue = 1024;
  maxValue = 0;

  uint32_t start_time = millis();
  while((millis() - start_time) < _millis) {
    poll();
  }
}

void ACS712::poll() {
  int readValue = analogRead(pin);
  
  if (readValue > maxValue) {
    maxValue = readValue;
  }
  if (readValue < minValue) {
    minValue = readValue;
  }
}

double ACS712::getCurrent() {
  if (maxValue == 0 && minValue == 1024) {
    pollForMillis(1000);
  }
  double VPP = ((maxValue - minValue) * 5.0) / 1024.0;
  double VRMS = (VPP / 2.0) * 0.707;
  double IRMS = (VRMS * 1000) / mVperAmp;

  return IRMS;
}
