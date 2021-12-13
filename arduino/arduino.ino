#include <NewPing.h>
#include <Servo.h>

String command = "";
int value = 0;
boolean newCommand = false;

int sonarFrontValue = 0;
unsigned long sonarReadInterval = 100;
unsigned long sonarLastReadTime = 0;

Servo myServo1;

void setup() {
  setupDisplay();
  setupSerial();
  setupMotorsHW();
  setupServos();
}

void loop() {
  getCommand();
  if (newCommand) {
    newCommand = false;
    if (command == "sto") {
      motorsStop();
    }
    else if (command == "mot") {
      frontMotor(value);
      rearMotor(value);
    }
    else if (command == "lon") {
      ledOn();
    }
    else if (command == "lof") {
      ledOff();
    }
    else if (command == "ssr") {
      steeringServo(value);
    }
  }
  readSonar();
}

bool sonarFrontRead = false;

void readSonar() {
  if (sonarLastReadTime < millis() and ((sonarLastReadTime + sonarReadInterval) > millis()) and !sonarFrontRead) {
    sonarFrontValue = sonarFrontGetDistance();
    sonarFrontRead = true;
  } else if ((sonarLastReadTime + sonarReadInterval) < millis()) {
    sonarFrontRead = false;
    sonarLastReadTime = millis();
    sendData(String(sonarFrontValue));
  }
}
